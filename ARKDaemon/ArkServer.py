import os
import platform
import psutil
import subprocess
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
                pid = pidfile.read()
            try:
                p = psutil.Process(pid)
                sys.exit('ARK is running. Shut the server down with --stop before starting it.')
            except:
                os.remove(self.pid_file)
                pid = ''

        # Get the correct binary to start the server
        if self.platform is "Windows":
            binary = os.path.join('ARK', 'ShooterGame', 'Binaries', 'Win64', 'ShooterGameServer.exe')
        elif self.platform is "Linux":
            binary = os.path.join('ARK', 'ShooterGame', 'Binaries', 'Linux', 'ShooterGameServer')
        else:
            sys.exit("You are running on an unsupported platform: {}".format(self.platform))

        # Format the password command so we can spit it out properly
        if self.config['ARK']['serverpassword'] is not '':
            server_password = "={}".format(self.config['ARK']['serverpassword'])
        else:
            server_password = ''

        # Make a comma seperated list of the mods from config
        try:
            if self.config['ARK']['mods']:
                my_mods = ",".join(self.config['ARK']['mods'])
        except(KeyError):
            my_mods = ''

        # Get the start command formed.
        start_cmd = "{my_binary} " \
                    "{map}" \
                    "?GameModIds={mods}" \
                    "?MaxPlayers={players}" \
                    "?Port=7777" \
                    "?QueryPort=27015" \
                    "?RCONEnabled=True" \
                    "?RCONPort=32330" \
                    "?ServerAdminPassword={adminpass}" \
                    "?ServerPassword{serverpass}" \
                    "?SessionName={sessionname}" \
                    "?listen"\
            .format(my_binary=binary,
                    map=self.config['ARK']['map'],
                    mods=my_mods,
                    players=self.config['ARK']['players'],
                    adminpass=self.config['ARK']['serveradminpassword'],
                    serverpass=server_password,
                    sessionname=self.config['ARK']['sessionname'],
                    )
        # Start the server, you nut!
        server_process = subprocess.call(start_cmd, shell=False)
        pid = server_process.pid
        with open(self.pid_file, 'w') as file:
            file.write(pid)
        print "Server launched! Please allow 5 to 10 minutes for server to start"

    def stop(self, safe=False):
        if not os.path.isfile(self.pid_file):
            sys.exit("Server is not running or PID file is missing! No need to stop (or you broke something).")
        else:
            # Check if the safe flag is set! If set, run the saveworld operation before screwing with the server.
            # Read the contents of the PID file and kill the process by PID.
            if safe:
                this = ServerRcon('127.0.0.1', 32330, self.config['ARK']['ServerAdminPassword'], 'saveworld')
                this.run_command()

            # Move forward to stop the server by PID. PID file defined as self.pid_file
            with open(self.pid_file, 'r') as pidfile:
                pid = pidfile.read()

            print "Killing process with PID: {}".format(pid)
            p = psutil.Process(pid)
            p.terminate()
            os.remove(self.pid_file)
            pid = ''
            print "All stop operations are complete."
