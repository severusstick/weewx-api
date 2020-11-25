import weewx.restx
import weewx.manager
import weewx.engine
import queue
import syslog
import sys
#import urllib2
from urllib.parse import urlencode
import urllib3

# Python 2/3 compatiblity shims
import six
#from six.moves import urllib

#from six.moves import http_client
#from six.moves import queue


class StdApi(weewx.restx.StdRESTful):

    def __init__(self, engine, config_dict):
        super(StdApi, self).__init__(engine, config_dict)

        site_dict = dict(weewx.restx.get_site_dict(config_dict,
                                                   'WeAPI',
                                                   'url',
                                                   'api_token',
                                                   'live_packets_route',
                                                   'minutely_archive_route'))

        if site_dict is None:  # return if restful API is disabled
            return

        # Get the database manager dictionary:
        site_dict['manager_dict'] = weewx.manager.get_manager_dict_from_config(
            config_dict, 'wx_binding')

        # Get archive update rate
        self.archive_interval = dict(dict(config_dict).get('StdArchive')).get('archive_interval')

        self.api_token = site_dict["api_token"]

        site_dict.setdefault('latitude', engine.stn_info.latitude_f)
        site_dict.setdefault('longitude', engine.stn_info.longitude_f)
        site_dict.setdefault('station_type', config_dict['Station'].get(
            'station_type', 'Unknown'))

        self.archive_queue = queue.Queue()

        self.archive_thread = WEAPIThread(self.archive_queue, **site_dict)
        self.archive_thread.start()

        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)  # Event binding
#        self.bind(weewx.NEW_LOOP_PACKET, self.new_loop_packet)

        syslog.syslog(syslog.LOG_INFO, "restx: WEAPI: "
                                       "Data will be uploaded")

    def new_archive_record(self, event):
        packet = event.record
        packet["packet_type"] = "minutely"
        packet["update_rate"] = self.archive_interval
        packet["api_token"] = self.api_token
        self.archive_queue.put(packet)

    def new_loop_packet(self, event):
        packet = event.packet
        packet["packet_type"] = "live"
        packet["update_rate"] = "live"
        packet["api_token"] = self.api_token
        self.archive_queue.put(packet)


class WEAPIThread(weewx.restx.RESTThread):
    def __init__(self, queue, manager_dict,
                 url, api_token, live_packets_route, skip_x_live_packets, minutely_archive_route,
                 latitude, longitude, station_type,
                 post_interval=600, max_backlog=six.MAXSIZE, stale=600,
                 log_success=True, log_failure=True,
                 timeout=10, max_tries=3, retry_wait=5, skip_upload=False):

        super(WEAPIThread, self).__init__(queue,
                                          protocol_name="WEAPI",
                                          essentials={},
                                          manager_dict=manager_dict,
                                          post_interval=None, max_backlog=six.MAXSIZE, stale=None,
                                          log_success=True, log_failure=True,
                                          timeout=10, max_tries=3, retry_wait=5, retry_login=3600,
                                          softwaretype="weewx-%s" % weewx.__version__,
                                          skip_upload=False)

        self.server_url = url
        self.live_packets_route = live_packets_route
        self.minutely_archive_route = minutely_archive_route
        self.skip_x_live_packets = skip_x_live_packets
        self.skip_x_live_packets_counter = 0

    def post_request(self, request, data=None):
        """Post a request object. This version does not catch any HTTP
        exceptions.

        Specializing versions can can catch any unusual exceptions that might
        get raised by their protocol.

        request: An instance of urllib.request.Request

        data: If given, the request will be done as a POST. Otherwise,
        as a GET. [optional]
        """
        # Data might be a unicode string. Encode it first.
        data_bytes = six.ensure_binary(data) if data is not None else None
        _response = urllib.request.urlopen(request, data=data_bytes, timeout=self.timeout)
        return _response

    def process_record(self, record, dbmanager):
        """Default version of process_record.

        This version uses HTTP GETs to do the post, which should work for many
        protocols, but it can always be replaced by a specializing class."""

        if record["packet_type"] == "live":

            post_url = self.server_url + self.live_packets_route
            _full_record = record
        elif record["packet_type"] == "minutely":
            post_url = self.server_url + self.minutely_archive_route

            # Get the full record by querying the database ...
            _full_record = self.get_record(record, dbmanager)
        else:
            syslog.syslog(syslog.LOG_INFO, "restx: WEAPI: "
                                           "En Error encored by finding the route")
            return

        syslog.syslog(syslog.LOG_INFO, "restx: WEAPI: "
                                       "Data posted to %s" % post_url)
        # ... check it ...
        self.check_this_record(_full_record)

        # ... then, finally, post it
        self.send_post_request(_full_record, post_url)

    def send_post_request(self, data, url):
        http = urllib3.PoolManager()

        http.request(
            'POST',
            url,
            fields=data,
            headers={"User-Agent": "weewx/%s" % weewx.__version__},
            #retries=self.max_tries
            #retries=5 # TODO: Use self.max_tries
        )


