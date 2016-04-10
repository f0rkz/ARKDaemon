# ARKDaemon: A Python Tool for ARK Dedicated Servers

This tool provides a suite of management tools for your Windows or Linux ARK: Survival Evolved Dedicated Server.

Please read over the README.md file thoroughly as important information is included here.

This tool is currently in development. Please submit issues if any come up!

# News

4/10/2016: [Commit c72f655](https://github.com/f0rkz/ARKDaemon/tree/c72f655cfa2b8427907e046f66a9783dc3438caa) Version 0.01 ready for production.

##Currently known issues and untested features:
* Backup is still not ready for production. Will work on that branch soon!
* Complete map changes from TheIsland may cause your server not to operate. Still need a lot more testing
* Mod install should work but it is currently untested.

# Installation

##Prerequisites
In order to run this script the following needs to be installed:
###Windows
 - python2.7 or higher: https://www.python.org/downloads/
 - pip (should be included in the python installer)
 - Some sort of git integrated with cmd. [I use the program here](https://git-scm.com/download/win).

* Make sure python is configured in Windows PATH Environment

You may also run into an issue with installing package requirements. If you get this error while running:
`pip install -r requirements.txt`:

`error: Microsoft Visual C++ 9.0 is required (Unable to find vcvarsall.bat). Get it from http://aka.ms/vcpython27`

Follow the link and install the msi Microsoft so kindly provided.

###Linux
 - lib32gcc1: `sudo apt-get install lib32gcc1`
 - python2.7 or higher: `sudo apt-get install python python-dev`
 - pip: `sudo apt-get install python-pip`

####Linux System Configuration

ARK Recommends the following settings in your Linux environment. [Click here for more information](http://ark.gamepedia.com/Dedicated_Server_Setup).


Add the following to `/etc/sysctl.conf`

`fs.file-max=100000`

Then run:

`sysctl -p /etc/sysctl.conf`

Add the following to `/etc/security/limits.conf`

      *               soft    nofile          1000000
      *               hard    nofile          1000000

Add the following to `/etc/pam.d/common-session`

`session required pam_limits.so`

You may need to reboot to make sure all of these settings took hold.

## Script Installation

###Step 1:
Clone the [github repository](https://github.com/f0rkz/ARKDaemon):

`git clone https://github.com/f0rkz/ARKDaemon.git`

This will create the directory ARKDaemon. This directory will contain steamcmd, ARK's gamefiles, and everything you
need to run ARK: Dedicated Server.

###Step 2:
Install the python requirements by the usual methods.

`pip install -r requirements.txt`

You may need to run this as root (or administrator for you Windows folks) if you are not using an environment.

##Install steamcmd
Steamcmd is required to install and update gameserver files and mods. In order to initiate steamcmd run the following
command:

`python ARKDaemon.py --install_steamcmd`

##Install ARK
Now you need to init your ARK install. Run the following (it will take a while...)

`python ARKDaemon.py --install_ark`


# Configuration
Configuration for the base server settings is stored in the server.conf file. The provided `server.conf_EXAMPLE` file is
enough information to get your instance running. Copy the `server.conf_EXAMPLE` to `server.conf` and configure your common
ARK settings here.

This file will change over time as the application evolves. Will attempt to notify in commit messages if new options are
added.

#Operating the Server

##Starting the server
`python ARKDaemon.py --start`

##Stopping the server
`python ARKDaemon.py --stop`

##Saving the World File
This will run the saveworld command on the server (needs to be running).

`python ARKDaemon.py --save_world`

##Server Backup
* Currently under production.

##Local Status
`python ARKDaemon.py --status`

# Program Structure

```
ARKDaemon
| ARKDaemon.py: The main script
|____/ARK: Gameserver files contained here. Installed by script. Empty by default.
|____/ARK_BACKUPS: Backup directory.
|____/ARKDaemon: Modules for ARKDaemon
|____/steamcmd: Steamcmd files
|____/templates: Template files for configurations
```
