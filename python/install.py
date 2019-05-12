# weapi installer

import configobj
from weecfg.extension import ExtensionInstaller
from StringIO import StringIO


weapi_config = """
    [StdRESTful]
            
        [[WeAPI]]
            # Config section for the WeAPI extension
            
            enable = true
            
            # Please don't forget the "/" at the end or the url,
            # it will be concatenated with the routes
            url = http://127.0.0.1:9000/api/
            
            # == Config the routes here === #
            
            # Route for live packets (weewx loop packets)            
            live_packets_route = live_packets
            # Skip x packets between posts to reduce bandwidth
            skip_x_live_packets = 3
            
            # Route for the weewx archive record (every 5 minutes depended to the archive_interval)
            minutely_archive_route = weather_per_minute
"""

weapi_config_dict = configobj.ConfigObj(StringIO(weapi_config))

def loader():
    return WeapiInstaller()


class WeapiInstaller(ExtensionInstaller):
    def __init__(self):
        super(WeapiInstaller, self).__init__(
            version="0.0.2",
            name='weapi',
            description='Nothing to say here yet',
            author="LimitlessGreen, severusstick",
            restful_services=['user.weapi.StdApi'],
            config=weapi_config_dict,
            files=[('bin/user', ['bin/user/weapi.py'])]
        )
