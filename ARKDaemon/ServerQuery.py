import re
from socket import gaierror, error

import requests
# External Modules to load
from ARKDaemon.SourceQuery import SourceQuery


class ServerQuery(object):
    def __init__(self, ip='127.0.0.1', port=27105):
        self.api = 'https://api.ark.bar/server/'
        self.ip = ip
        self.port = port

    def status(self):
        try:
            server = SourceQuery(self.ip, self.port)
            info = server.info()
            data = {
                'status': True,
                'hostname': info['hostname'].split(" - ")[0],
                'version': re.sub('[v()]', '', info['hostname'].split(" - ")[1]),
                'map': info['map'],
                'os': info['os'],
                'players_cur': info['numplayers'],
                'players_max': info['maxplayers'],
            }
        except (gaierror, error):
            data = {
                'status': False,
            }

        return data

    def remotestatus(self):
        request = requests.get('{api}{ip}/{port}'.format(api=self.api, ip=self.ip, port=self.port))
        return request.json()
