import ast
import os
import re
from socket import gaierror, error

import psutil
import requests

# External Modules to load
from ARKDaemon.SourceQuery import SourceQuery


class ServerQuery(object):
    def __init__(self, ip='127.0.0.1', port=27105, config=False):
        self.api = 'https://api.ark.bar/server/'
        self.ip = ip
        self.port = port
        self.pid_file = os.path.join('ark.pid')
        self.config = config

    def status(self):
        try:
            server = SourceQuery(self.ip, self.port)
            info = server.info()

            try:
                if self.config['ARK']['mods']:
                    mod_list = ast.literal_eval(config['ARK']['mods'])
            except KeyError:
                mod_list = False

            # Convert the OS to its full name
            if info['os'] == "w":
                my_os = "Windows"
            elif info['os'] == "l":
                my_os = "Linux"

            if not os.path.isfile(self.pid_file):
                sys_data = False
            else:
                with open(self.pid_file, 'r') as pidfile:
                    pid = int(pidfile.read())
                p = psutil.Process(pid=pid)
                sys_data = {
                    'cpu': p.cpu_percent(interval=1),
                    'mem': int(p.memory_percent()),
                    'threads': p.num_threads(),
                }

            # Form up the data array
            data = {
                'status': True,
                'hostname': info['hostname'].split(" - ")[0],
                'version': re.sub('[v()]', '', info['hostname'].split(" - ")[1]),
                'map': info['map'],
                'os': my_os,
                'players_cur': info['numplayers'],
                'players_max': info['maxplayers'],
            }
            if sys_data:
                data['system_info'] = sys_data
            else:
                data['system_info'] = False

            if mod_list:
                installed_mods = {}
                for mod in mod_list:
                    installed_mods[mod] = '{steam}{id}'.format(steam='https://steamcommunity.com/sharedfiles/filedetails/?id=', id=mod)

                data['installed_mods'] = installed_mods

        except (gaierror, error):
            data = {
                'status': False,
            }

        return data

    def remotestatus(self):
        request = requests.get('{api}{ip}/{port}'.format(api=self.api, ip=self.ip, port=self.port))
        return request.json()
