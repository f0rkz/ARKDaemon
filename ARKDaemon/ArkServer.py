import os
import platform
import shlex
import signal
import subprocess
import sys

import psutil

from ARKDaemon.ServerRcon import ServerRcon


class ArkServer(object):
    def __init__(self, config):
        self.config = config
        self.pid_file = os.path.join('ark.pid')
        self.platform = platform.system()

    def start(self):
        """
            subprocess create the process, record the PID of the process and write to a PID file.
            Only issue I can think of is if the server is forcefully closed by the OS
            and the server isn't actually running.
            Maybe I need to add a check in the status module to delete the PID file if the server
            is not running... Will have to test and find out.
        """
        if os.path.isfile(self.pid_file):
            # Get a list of active PID's and see if the PID in the file exists. If not, delete the PID file.
            with open(self.pid_file, 'r') as pidfile:
                pid = int(pidfile.read())
            try:
                psutil.Process(pid)
                sys.exit('ARK is running. Shut the server down with --stop before starting it.')
            except psutil.NoSuchProcess:
                os.remove(self.pid_file)
                pid = ''

        # Get the correct binary to start the server
        if self.platform == "Windows":
            binary = os.path.join('ARK', 'ShooterGame', 'Binaries', 'Win64', 'ShooterGameServer.exe')
        elif self.platform == "Linux":
            binary = os.path.join('ARK', 'ShooterGame', 'Binaries', 'Linux', 'ShooterGameServer')
        else:
            sys.exit("You are running on an unsupported platform: {}".format(self.platform))

        # Format the password command so we can spit it out properly
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

        # Get the start command formed.
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
                    "?SessionName={sessionname}" \
                    "?listen " \
                    "{battleye}" \
                    "-server "\
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
                    sessionname=self.config['ARK']['sessionname'],
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
        print "Server launched! Please allow 5 to 10 minutes for server to start"

    def stop(self, safe=False):
        if not os.path.isfile(self.pid_file):
            sys.exit("Server is not running or PID file is missing! No need to stop (or you broke something).")
        else:
            # Check if the safe flag is set! If set, run the saveworld operation before screwing with the server.
            # Read the contents of the PID file and kill the process by PID.
            if safe:
                this = ServerRcon(self.config['ARK']['ip'], int(self.config['ARK']['rcon_port']),
                                  self.config['ARK']['ServerAdminPassword'], 'saveworld')
                this.run_command()

            # Move forward to stop the server by PID. PID file defined as self.pid_file
            with open(self.pid_file, 'r') as pidfile:
                pid = int(pidfile.read())

            print "Killing process with PID: {}".format(pid)
            p = psutil.Process(pid)
            p.send_signal(signal.SIGTERM)
            os.remove(self.pid_file)
            pid = ''
            print "All stop operations are complete."
