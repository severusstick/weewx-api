import weewx.restx
import weewx.manager
import weewx.engine
import Queue
import syslog
import sys
import urllib2
import urllib


class StdApi(weewx.restx.StdRESTful):

    def __init__(self, engine, config_dict):
        super(StdApi, self).__init__(engine, config_dict)

        site_dict = dict(weewx.restx.get_site_dict(config_dict,
                                                   'WeAPI',
                                                   'url',
                                                   'live_packets_route',
                                                   'minutely_archive_route'))

        if site_dict is None:  # return if restful API is disabled
            return

        # Get the database manager dictionary:
        site_dict['manager_dict'] = weewx.manager.get_manager_dict_from_config(
            config_dict, 'wx_binding')

        # Get archive update rate
        site_dict['archive_interval'] = dict(dict(config_dict).get('StdArchive')).get('archive_interval')

        site_dict.setdefault('latitude', engine.stn_info.latitude_f)
        site_dict.setdefault('longitude', engine.stn_info.longitude_f)
        site_dict.setdefault('station_type', config_dict['Station'].get(
            'station_type', 'Unknown'))

        self.archive_queue = Queue.Queue()

        self.archive_thread = WEAPIThread(self.archive_queue, **site_dict)
        self.archive_thread.start()

        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)  # Event binding
        self.bind(weewx.NEW_LOOP_PACKET, self.new_loop_packet)


        syslog.syslog(syslog.LOG_INFO, "restx: WEAPI: "
                                       "Data will be uploaded")

    def new_archive_record(self, event):
        packet = event.record
        packet["packet_type"] = "minutely"
        self.archive_queue.put(packet)

    def new_loop_packet(self, event):
        packet = event.packet
        packet["packet_type"] = "live"
        self.archive_queue.put(packet)


class WEAPIThread(weewx.restx.RESTThread):
    def __init__(self, queue, manager_dict,
                 url, live_packets_route, minutely_archive_route, archive_interval,
                 latitude, longitude, station_type,
                 post_interval=600, max_backlog=sys.maxint, stale=600,
                 log_success=True, log_failure=True,
                 timeout=10, max_tries=3, retry_wait=5, skip_upload=False):

        super(WEAPIThread, self).__init__(queue,
                                          protocol_name="WEAPI",
                                          essentials={},
                                          manager_dict=manager_dict,
                                          post_interval=None, max_backlog=sys.maxint, stale=None,
                                          log_success=True, log_failure=True,
                                          timeout=10, max_tries=3, retry_wait=5, retry_login=3600,
                                          softwaretype="weewx-%s" % weewx.__version__,
                                          skip_upload=False)

        self.server_url = url
        self.live_packets_route = live_packets_route
        self.minutely_archive_route = minutely_archive_route

    def process_record(self, record, dbmanager):
        """Default version of process_record.

        This version uses HTTP GETs to do the post, which should work for many
        protocols, but it can always be replaced by a specializing class."""

        if record["packet_type"] == "live":
            post_url = self.server_url + self.live_packets_route
        elif record["packet_type"] == "minutely":
            post_url = self.server_url + self.minutely_archive_route
        else:
            return

        # Get the full record by querying the database ...
        _full_record = self.get_record(record, dbmanager)

        syslog.syslog(syslog.LOG_INFO, "restx: WEAPI: "
                                       "Data posted to %s" % post_url)
        # ... check it ...
        self.check_this_record(_full_record)
        # ... get the Request obj to go with it...
        _request = self.get_request(post_url)
        #  ... get any POST payload...

        _request.add_data(urllib.urlencode(_full_record))
        _request.add_data(urllib.urlencode(self.post_interval))

        self.post_with_retries(_request)



