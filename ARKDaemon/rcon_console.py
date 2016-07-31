from ARKDaemon.ServerRcon import ServerRcon

class RconConsole(object):
    def __init__(self, config):
        self.config = config

    def start(self):
        # Main loop for rcon console
        print "Starting rcon-console. Please enter 'stop' or ^c to stop console."
        while True:
            print "rcon-console#" ,
            user_input = raw_input()
            if user_input == 'stop':
                break
            if user_input:
                reply = self.process_cmd(user_input)
                print reply


    def process_cmd(self, rcon_cmd):
        this = ServerRcon('127.0.0.1', int(self.config['ARK']['rcon_port']),
                          self.config['ARK']['serveradminpassword'], rcon_cmd)
        this.run_command()