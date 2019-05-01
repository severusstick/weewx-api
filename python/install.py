# weapi installer

from weecfg.extension import ExtensionInstaller


def loader():
    return WeapiInstaller()


class WeapiInstaller(ExtensionInstaller):
    def __init__(self):
        super(WeapiInstaller, self).__init__(
            version="0.0.1",
            name='weapi',
            description='Nothing to say here yet',
            author="LimitlessGreen, severusstick",
            restful_services=['user.weapi.StdApi'],
            config={
                'StdRESTful': {
                    'WeAPI': {
                        'enable': 'false',
                        'url': 'http://127.0.0.1'
                    }
                }
            },
            files=[('bin/user', ['bin/user/weapi.py'])]
        )
