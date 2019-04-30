import weewx.restx
import weewx.manager
import Queue
import syslog
import sys


class StdApi(weewx.restx.StdRESTful):
    _server = None

    def __init__(self, engine, config_dict):
        super(StdApi, self).__init__(engine, config_dict)

        site_dict = weewx.restx.get_site_dict(config_dict, 'WeAPI', 'url')

        if site_dict is None:  # return if restful API is disabled
            return

        site_dict.setdefault('latitude', engine.stn_info.latitude_f)
        site_dict.setdefault('longitude', engine.stn_info.longitude_f)
        site_dict.setdefault('language', 'de')

        self._server = site_dict['url']

        # Get the database manager dictionary:
        site_dict['manager_dict'] = weewx.manager.get_manager_dict_from_config(
            config_dict, 'wx_binding')

        self.archive_queue = Queue.Queue()

        self.archive_thread = WEAPIThread(self.archive_queue, **site_dict)
        self.archive_thread.start()

        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)  # Wad'n das?

        syslog.syslog(syslog.LOG_INFO, "restx: WEAPI: "
                                       "Data will be uploaded")

    def new_archive_record(self, event):
        self.archive_queue.put(event.record)


class WEAPIThread(weewx.restx.RESTThread):
    def __init__(self,
                 queue,
                 manager_dict,
                 url,
                 station,
                 post_interval=None, max_backlog=sys.maxint, stale=None,
                 log_success=True, log_failure=True,
                 timeout=10, max_tries=3, retry_wait=5, retry_login=3600,
                 skip_upload=False):

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


