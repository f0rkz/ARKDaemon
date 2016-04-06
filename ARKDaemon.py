import sys
import os.path

#import ConfigParser
#import sqlite3
import argparse
import subprocess

# Classes from project
from ARKDaemon.SteamCmd import SteamCmd
from ARKDaemon.ConfigureArk import ConfigureArk
from ARKDaemon.ServerQuery import ServerQuery

# 376030 ark dedi server
# 445400 ark survival of the fittest dedi server

# ARGParse Items to route the application
argparser = argparse.ArgumentParser(description="ARKDaemon: A Python Tool for ARK Dedicated Servers")
argparser.add_argument("-s", "--install_steamcmd", help="Install Steamcmd. (Required)", action="store_true")
argparser.add_argument("-i", "--install_ark", help="Install the gameserver files.", action="store_true")
argparser.add_argument("-c", "--configure", help="Run the configuration tool.", action="store_true")
argparser.add_argument("-u", "--update", help="Update the gameserver files.", action="store_true")
argparser.add_argument("--status", nargs = '?', const=('127.0.0.1', 27015), help="Get the local server's status")
argparser.add_argument("--remote_status", nargs = '*', help="Run a status on gameserver. Accepts two values: --remote_status server port")
argparser.add_argument("--start", help="Start the server", action="store_true")
argparser.add_argument("--stop", help="Stop the server", action="store_true")
argparser.add_argument("--safe", help="Save the server world before doing update/stop/etc. actions", action="store_true")
argparser.add_argument("-f", "--force", help="Force the operation without abandon.", action="store_true")
argparser.add_argument("--install_mod", help="Installs a mod. Example: ARKDaemon.py install_mod 655581765")
argparser.add_argument("-b", "--backup", help="Backs up ARK world data.")
args = argparser.parse_args()

if args.install_steamcmd:
    print "Checking and installing steamcmd."
    this = SteamCmd(appid=False)
    if args.force:
        this.install_steamcmd(force=True)
    else:
        this.install_steamcmd()

if args.install_ark and not args.start and not args.stop and not args.update:
    # Loop to get the game type from the user.
    while True:
        user_input = raw_input("ARK Classic (c) or Survival of the Fittest (s)? [c/s]: ")
        user_input = user_input.lower()
        if user_input == 'c' or user_input == '':
            appid = '376030'
            break
        elif user_input == 's':
            appid = '445400'
            break
        else:
            print "Invalid option: {}. Expecting C/c or S/s.".format(user_input)

    print "Installing ARK files. This will take a while. I suggest making some tea."
    sleep(1)
    this = SteamCmd(appid=appid)
    this.install_ark()

if args.configure and not args.start and not args.stop and not args.update:
    print "Configure!"

if args.update:
    print "Update!"

if args.start:
    print "Start"

if args.stop:
    print "STAHP"

if args.install_mod:
    print "Install mod!"

if args.backup:
    print "Backup!"

if args.remote_status:
    if len(args.remote_status) > 2 or len(args.remote_status) < 2:
        sys.exit("Improper values given. Please supply: [ip] [port]")
    elif len(args.remote_status) == 2:
        this = ServerQuery(ip=args.remote_status[0], port=args.remote_status[1])
        result = this.remotestatus()
        if result['status'] == True:
            print "Status: Online"
            print "Server Name: {}".format(result['server']['name'])
            print "Server Version: {}".format(result['server']['version'])
            print "Server Map: {}".format(result['server']['map'])
            print "Server Environment: {}".format(result['server']['environment'])
            print "Players: {} / {}".format(result['server']['playerCount'], result['server']['playerMax'])
        else:
            print "Status: Offline"
            print "Possible issue with returned data, the server does not exist, or the server is offline."

if args.status:
    this = ServerQuery()
    result = this.status()
    if result['status'] == True:
        print "Status: Online"
        print "Server Name: {}".format(result['hostname'])
        print "Server Version: {}".format(result['version'])
        print "Server Map: {}".format(result['map'])
        print "Server Environment: {}".format(result['os'])
        print "Players: {} / {}".format(result['players_cur'], result['players_max'])
    else:
        print "Status: Offline"
        print "Possible issue with returned data, the server does not exist, or the server is offline."

# Test steamcmd install
#install = SteamCmd('376030')
#install.install_steamcmd()
#install.install_gamefiles('376030')
