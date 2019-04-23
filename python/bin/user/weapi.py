from weewx.restx import StdRESTful, get_site_dict
import weewx.manager

class StdApi(StdRESTful):

    _server = None

    def __init__(self, engine, config_dict):

        super(StdApi, self).__init__(engine, config_dict)

        site_dict = get_site_dict(config_dict, 'WeAPI', 'url')

        if site_dict is None:  # return if restful API is disabled
            return

        self._server = site_dict['url']
