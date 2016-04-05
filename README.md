# ARKDaemon: A Python Tool for ARK Dedicated Servers
---
This tool provides a suite of management tools for your Windows or Linux ARK: Survival Evolved Dedicated Server.

Please read over the README.md file thoroughly as important information is included here.

This tool is currently in development. Please submit issues if any come up!

# Installation
---
##Prerequisites
In order to run this script the following needs to be installed:
###Windows
 - python2.7 or higher: https://www.python.org/downloads/
 - pip (should be included in the python installer)
 - Some sort of git integrated with cmd. [I use the program here](https://git-scm.com/download/win).

* Make sure python is configured in Windows PATH Environment

###Linux
 - lib32gcc1: `sudo apt-get install lib32gcc1`
 - python2.7 or higher: `sudo apt-get install python`
 - pip: `sudo apt-get install python-pip`

####Linux System Configuration

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

For more information, [check this link](http://ark.gamepedia.com/Dedicated_Server_Setup).

# Program Structure
---
```
ARKDaemon
| ARKDaemon.py: The main script
|____/ARK: Gameserver files contained here. Installed by script. Empty by default.
|____/ARK_BACKUPS: Backup directory.
|____/ARKDaemon: Modules for ARKDaemon
|____/steamcmd: Steamcmd files
|____/templates: Template files for configurations
```
