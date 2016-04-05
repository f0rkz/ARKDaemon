import requests
import json

class ServerQuery(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.api = 'https://api.ark.bar/server/'

    def GetStatus(self):
        request = requests.get('{api}{ip}/{port}'.format(api=self.api, ip=self.ip, port=self.port))
        return request.json()