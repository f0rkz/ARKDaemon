import ARKDaemon.SourceRcon as rcon


class ServerRcon(object):
    def __init__(self, ip, port, password, ark_command):
        self.ip = ip
        self.port = port
        self.password = password
        self.ark_command = ark_command

    def run_command(self):
        try:
            print "Opening RCON connection with the server. Timeout set to 10 seconds. Please be patient..."
            server = rcon.SourceRcon(self.ip, self.port, self.password, timeout=10)
            result = server.rcon(self.ark_command)
            return result
        except:
            print 'Unable to connect to RCON!'
