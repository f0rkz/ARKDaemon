import sys
import os
import time

import ConfigParser
import ast
import argparse
from colorama import init, Fore, Style
init()

# Classes from project
from ARKDaemon.SteamCmd import SteamCmd
from ARKDaemon.ServerQuery import ServerQuery
from ARKDaemon.ServerRcon import ServerRcon

# from ARKDaemon.ArkBackup import ArkBackup
# from ARKDaemon.ConfigureArk import ConfigureArk

# List of Appids capable in this tool:
# 376030 ark dedi server
# 445400 ark survival of the fittest dedi server

# ARGParse Items to route the application
argparser = argparse.ArgumentParser(description="ARKDaemon: A Python Tool for ARK Dedicated Servers")
argparser.add_argument("-s", "--install_steamcmd", help="Install Steamcmd. (Required)", action="store_true")
argparser.add_argument("-i", "--install_ark", help="Install the gameserver files.", action="store_true")
argparser.add_argument("-c", "--configure", help="Run the configuration tool.", action="store_true")
argparser.add_argument("-u", "--update", help="Update the gameserver files.", action="store_true")
argparser.add_argument("--status", help="Get the local server's status", action="store_true")
argparser.add_argument("--remote_status", metavar=('ip/host', 'port'), nargs='*',
                       help="Run a status on gameserver. Accepts two values: --remote_status ip/host port")
argparser.add_argument("--start", help="Start the server", action="store_true")
argparser.add_argument("--stop", help="Stop the server", action="store_true")
argparser.add_argument("--safe", help="Save the server world before doing update/stop/etc. actions",
                       action="store_true")
argparser.add_argument("--save_world", help="Run the saveworld command. This may cause intermittent lag!",
                       action="store_true")
argparser.add_argument("-f", "--force", help="Force the operation without abandon.", action="store_true")
argparser.add_argument("--install_mod", nargs = '?', metavar='mod_id', help="Installs a mod. Example: ARKDaemon.py install_mod 655581765")
argparser.add_argument("--update_mods", help="Runs an update/install of all mods listed in sever.conf", action="store_true")
argparser.add_argument("-b", "--backup", help="Backs up ARK world data.")
argparser.add_argument("--debug", help="Debug flag for more output.", action="store_true")
args = argparser.parse_args()

parser = ConfigParser.RawConfigParser()
if os.path.isfile(os.path.join('server.conf')):
    parser.read(os.path.join('server.conf'))
    server_config = parser._sections
    if server_config['ARK']['mods']:
        mod_list = ast.literal_eval(server_config['ARK']['mods'])
else:
    print "It looks like you do not have a server.conf." \
          "I recommend copying server.conf_EXAMPLE to server.conf and editing it to your needs."

if args.debug:
    DEBUG = True
else:
    DEBUG = False

# Spit out the configuration dictionary
if DEBUG and server_config:
    print 'I am loading the following configuration:'
    print 'APPID: {}'.format(server_config['ARK']['appid'])
    print 'Session Name: {}'.format(server_config['ARK']['sessionname'])
    if server_config['ARK']['serverpassword'] == '':
        print 'No join password.'
    else:
        print 'Join password: {}'.format(server_config['ARK']['serverpassword'])
    print 'Server Admin Password: {}'.format(server_config['ARK']['serveradminpassword'])
    print 'Map: {}'.format(server_config['ARK']['map'])
    print 'Mods: {}'.format(mod_list)

if args.install_steamcmd:
    print "Checking and installing steamcmd."
    this = SteamCmd(appid=False)
    if args.force:
        this.install_steamcmd(force=True)
    else:
        this.install_steamcmd()

elif args.install_ark:
    if server_config['ARK']['appid'] == '376030':
        appid = '376030'
        print "Installing ARK files. This will take a while. I suggest making some tea."
        time.sleep(5)
        this = SteamCmd(appid=appid)
        this.install_gamefiles()

    elif server_config['ARK']['appid'] == '445400':
        appid = '445400'
        print "Installing ARK files. This will take a while. I suggest making some tea."
        time.sleep(5)
        this = SteamCmd(appid=appid)
        this.install_gamefiles()

    else:
        sys.exit('Something is wrong with your configuration. I expected appid 376030 or 445400, but received {}')\
            .format(server_config['ARK']['appid'])

elif args.configure:
    print "Configure!"

elif args.update:
    this = ServerQuery(ip='127.0.0.1', port=27015)
    result = this.status()
    if result['status']:
        sys.exit("Server is currently online! Stop the server first.")
    else:
        print "Running update for ARK! Appid: {}".format(server_config['ARK']['appid'])
        update = SteamCmd(appid=server_config['ARK']['appid'])
        update.install_gamefiles()

elif args.start:
    print "Start"

elif args.stop:
    print "STAHP"

elif args.save_world:
    this = ServerQuery(ip='127.0.0.1', port=27015)
    result = this.status()
    if result['status']:
        rcon = ServerRcon(ip='127.0.0.1', port=32330, password=server_config['ARK']['ServerAdminPassword'],
                          ark_command='saveworld')
    else:
        sys.exit("Server did not respond to a simple query. It may be offline!")

elif args.install_mod:
    this = SteamCmd(appid=server_config['ARK']['appid'], mod_id=args.install_mod[0])
    this.install_mod()

elif args.update_mods:
    print "Update mods!"

elif args.backup:
    print "Backup!"

elif args.remote_status:
    if len(args.remote_status) > 2 or len(args.remote_status) < 2:
        sys.exit("Improper values given. Please supply: [ip] [port]")
    elif len(args.remote_status) == 2:
        this = ServerQuery(ip=args.remote_status[0], port=args.remote_status[1])
        result = this.remotestatus()
        if result['status']:
            print("Status: " + Fore.GREEN + "Online" + Style.RESET_ALL)
            print "Server Name: {}".format(result['server']['name'])
            print "Server Version: {}".format(result['server']['version'])
            print "Server Map: {}".format(result['server']['map'])
            print "Server Environment: {}".format(result['server']['environment'])
            print "Players: {} / {}".format(result['server']['playerCount'], result['server']['playerMax'])
        else:
            print("Status: " + Fore.RED + "Offline" + Style.RESET_ALL)
            print "Possible issue with returned data, the server does not exist, or the server is offline."

elif args.status:
    this = ServerQuery(ip='127.0.0.1', port=27015)
    result = this.status()
    if result['status']:
        print("Status: " + Fore.GREEN + "Online" + Style.RESET_ALL)
        print "Server Name: {}".format(result['hostname'])
        print "Server Version: {}".format(result['version'])
        print "Server Map: {}".format(result['map'])
        print "Server Environment: {}".format(result['os'])
        print "Players: {} / {}".format(result['players_cur'], result['players_max'])
    else:
        print("Status: " + Fore.RED + "Offline" + Style.RESET_ALL)
        print "Possible issue with returned data, the server does not exist, or the server is offline."

else:
    sys.exit("No options given. Use --help for more information.")

