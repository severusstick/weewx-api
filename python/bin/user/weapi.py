import weewx.restx
import weewx.manager
import Queue
import syslog
import sys
import urllib2
import urllib


class StdApi(weewx.restx.StdRESTful):
    _server = None

    def __init__(self, engine, config_dict):
        super(StdApi, self).__init__(engine, config_dict)

        site_dict = weewx.restx.get_site_dict(config_dict, 'WeAPI', 'url')

        if site_dict is None:  # return if restful API is disabled
            return

        # Get the database manager dictionary:
        site_dict['manager_dict'] = weewx.manager.get_manager_dict_from_config(
            config_dict, 'wx_binding')

        site_dict.setdefault('latitude', engine.stn_info.latitude_f)
        site_dict.setdefault('longitude', engine.stn_info.longitude_f)
        site_dict.setdefault('station_type', config_dict['Station'].get(
            'station_type', 'Unknown'))

        self._server = site_dict['url']


        self.archive_queue = Queue.Queue()

        self.archive_thread = WEAPIThread(self.archive_queue, **site_dict)
        self.archive_thread.start()

        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)  # Wad'n das?

        syslog.syslog(syslog.LOG_INFO, "restx: WEAPI: "
                                       "Data will be uploaded")

    def new_archive_record(self, event):
        self.archive_queue.put(event.record)


class WEAPIThread(weewx.restx.RESTThread):
    def __init__(self, queue, manager_dict,
                 url,
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

    def process_record(self, record, dbmanager):
        """Default version of process_record.

        This version uses HTTP GETs to do the post, which should work for many
        protocols, but it can always be replaced by a specializing class."""

        # Get the full record by querying the database ...
        _full_record = self.get_record(record, dbmanager)

        syslog.syslog(syslog.LOG_INFO, "restx: WEAPI: "
                                       "Data posted to %s" % self.server_url)
        # ... check it ...
        self.check_this_record(_full_record)
        # ... get the Request obj to go with it...
        _request = self.get_request(self.server_url)
        #  ... get any POST payload...

        _request.add_data(urllib.urlencode(_full_record))

        self.post_with_retries(_request)



