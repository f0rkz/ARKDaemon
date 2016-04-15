import os
import platform
import shlex
import signal
import subprocess

import psutil

from ARKDaemon.ServerRcon import ServerRcon


class ArkServerApi(object):
    def __init__(self, config, safe=False):
        self.config = config
        self.pid_file = os.path.join('ark.pid')
        self.platform = platform.system()
        self.safe = safe

    def start(self):
        # Initiate the dictionary to return with server task information
        result = {}
        if os.path.isfile(self.pid_file):
            with open(self.pid_file, 'r') as pidfile:
                pid = int(pidfile.read())
            try:
                psutil.Process(pid)
                result['error'] = True
                result['message'] = 'Error: Server is currently running'
            except:
                result['error'] = False
                os.remove(self.pid_file)
                pid = ''

        # Check the server platform and error if an unsupported platform is running.
        if self.platform == "Windows":
            binary = os.path.join('ARK', 'ShooterGame', 'Binaries', 'Win64', 'ShooterGameServer.exe')
        elif self.platform == "Linux":
            binary = os.path.join('ARK', 'ShooterGame', 'Binaries', 'Linux', 'ShooterGameServer')
        else:
            result['error'] = True
            result['message'] = 'Error: Unsupported platform: {}'.format(self.platform)

        # Check the server password and format it for ARK
        if self.config['ARK']['serverpassword'] is not '':
            server_password = "={}".format(self.config['ARK']['serverpassword'])
        else:
            server_password = ''

        # Catch if battleye is enabled
        if self.config['ARK']['battleye']:
            battleye_enable = "-UseBattlEye "
        else:
            battleye_enable = ""

        # Make a comma seperated list of the mods from config
        try:
            if self.config['ARK']['mods']:
                my_mods = str(self.config['ARK']['mods']).strip('[]')
                my_mods = my_mods.replace("'", "")
                my_mods = my_mods.replace(" ", "")
        except KeyError:
            my_mods = ''

        # Catch a custom map mod id
        try:
            if self.config['ARK']['mapmodid']:
                map_mod_id = '-mapmodid={}'.format(self.config['ARK']['mapmodid'])
        except KeyError:
            map_mod_id = ''

        # Main wrapper depending on result['error']
        if result['error'] is False:
            # Form up the start command
            start_cmd = "{my_binary} " \
                        "{map}" \
                        "?GameModIds={mods}" \
                        "?Multihome={ip}" \
                        "?MaxPlayers={players}" \
                        "?Port={listen_port}" \
                        "?QueryPort={query_port}" \
                        "?RCONEnabled=True" \
                        "?RCONPort={rcon_port}" \
                        "?ServerAdminPassword={adminpass}" \
                        "?ServerPassword{serverpass}" \
                        "?listen " \
                        "{battleye}" \
                        "-server " \
                        "-log " \
                        "{mapid}" \
                .format(my_binary=binary,
                        map=self.config['ARK']['map'],
                        mods=my_mods,
                        ip=self.config['ARK']['ip'],
                        players=self.config['ARK']['players'],
                        listen_port=self.config['ARK']['gameserver_port'],
                        query_port=self.config['ARK']['query_port'],
                        rcon_port=self.config['ARK']['rcon_port'],
                        adminpass=self.config['ARK']['serveradminpassword'],
                        serverpass=server_password,
                        battleye=battleye_enable,
                        mapid=map_mod_id,
                        )

            # Start the server, you nut!
            if self.platform == "Windows":
                server_process = subprocess.Popen(start_cmd, shell=False)
            else:
                server_process = subprocess.Popen(shlex.split(start_cmd), shell=False)
            pid = server_process.pid
            with open(self.pid_file, 'w') as my_pid_file:
                my_pid_file.write('{}'.format(pid))

            result['message'] = "Server launched! Please allow 5 to 10 minutes for server to start"
            return result

        else:
            return result

    def stop(self):
        result = {}
        if not os.path.isfile(self.pid_file):
            result['error'] = True
            result['message'] = 'Server is not running or PID file is missing! No need to stop (or you broke something).'
            return result
        else:
            if self.safe:
                this = ServerRcon('127.0.0.1', int(self.config['ARK']['rcon_port']),
                                  self.config['ARK']['serveradminpassword'], 'saveworld')
                result['save_world'] = this.run_command()

            # Move forward to stop the server by PID.
            with open(self.pid_file, 'r') as pidfile:
                pid = int(pidfile.read())
            p = psutil.Process(pid)
            p.send_signal(signal.SIGTERM)
            os.remove(self.pid_file)
            pid = ''
            result['error'] = False
            result['message'] = 'Stopped'

            return result