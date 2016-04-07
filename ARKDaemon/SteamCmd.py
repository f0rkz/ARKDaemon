import os
import os.path
import platform
import subprocess
import tarfile
import urllib
import zipfile


class SteamCmd(object):
    def __init__(self, appid):
        # type: (object) -> object
        self.os = os.name
        self.platform = platform.system()
        self.steamcmd_download_linux = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
        self.steamcmd_download_windows = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
        self.steamcmd_path = os.path.join('steamcmd')
        self.install_dir = os.path.join(os.getcwd(), 'ARK')
        self.appid = appid

    def install_steamcmd(self, force=False):
        # Installs steamcmd for windows
        if self.platform == "Windows":
            if os.path.exists(os.path.join(self.steamcmd_path, 'steamcmd.exe')) and force == False:
                print "Steamcmd already installed. No need for reinstall."
            else:
                urllib.urlretrieve(self.steamcmd_download_windows, os.path.join(self.steamcmd_path, 'steamcmd.zip'))
                with zipfile.ZipFile(os.path.join(self.steamcmd_path, 'steamcmd.zip'), "r") as z:
                    z.extractall(self.steamcmd_path)
                print "Steamcmd installed to ./{}".format(self.steamcmd_path)

        # Installs steamcmd for Linux
        elif self.platform == "Linux":
            if os.path.exists(os.path.join(self.steamcmd_path, 'steamcmd.sh')):
                print "Steamcmd already installed. No need for a reinstall."
            else:
                urllib.urlretrieve(self.steamcmd_download_linux,
                                   os.path.join(self.steamcmd_path, 'steamcmd_linux.tar.gz'))
                with tarfile.open(os.path.join(self.steamcmd_path, 'steamcmd_linux.tar.gz'), 'r:gz') as z:
                    z.extractall(self.steamcmd_path)
        else:
            sys_exit("Unsupported system. I detected {}.".format(self.platform))

    def install_gamefiles(self):
        if self.platform == "Windows":
            steamcmd_run = '{steamcmd_path}\steamcmd.exe ' \
                           '+login anonymous ' \
                           '+force_install_dir {install_dir} ' \
                           '+app_update {my_appid} ' \
                           'validate ' \
                           '+quit ' \
                .format(steamcmd_path=self.steamcmd_path,
                        install_dir=self.install_dir,
                        my_appid=self.appid,
                        )
            subprocess.call(steamcmd_run, shell=True)

        elif self.platform == "Linux":
            steamcmd_run = '{steamcmd_path}/steamcmd.sh ' \
                           '+login anonymous ' \
                           '+force_install_dir {install_dir} ' \
                           '+app_update {my_appid} ' \
                           'validate ' \
                           '+quit ' \
                .format(steamcmd_path=self.steamcmd_path,
                        base_dir=self.base_dir,
                        install_dir=self.install_dir,
                        my_appid=self.appid,
                        )
            subprocess.call(steamcmd_run, shell=True)

        else:
            sys_exit("Unsupported system. I detected {}.".format(self.platform))

    def update_gamefiles(self):
        if self.platform == "Windows":
            steamcmd_run = '{steamcmd_path}/steamcmd.exe ' \
                           '+login anonymous ' \
                           '+force_install_dir {install_dir} ' \
                           '+app_update {my_appid} ' \
                           'validate ' \
                           '+quit ' \
                .format(steamcmd_path=self.steamcmd_path,
                        base_dir=self.base_dir,
                        install_dir=self.install_dir,
                        my_appid=self.appid,
                        )
            subprocess.call(steamcmd_run, shell=True)

        elif self.platform == "Linux":
            steamcmd_run = '{steamcmd_path}/steamcmd.sh ' \
                           '+login anonymous ' \
                           '+force_install_dir {install_dir} ' \
                           '+app_update {my_appid} ' \
                           'validate ' \
                           '+quit ' \
                .format(steamcmd_path=self.steamcmd_path,
                        base_dir=self.base_dir,
                        install_dir=self.install_dir,
                        my_appid=self.appid,
                        )
            subprocess.call(steamcmd_run, shell=True)

    def install_mod(self):
        if self.platform == "Windows":
            pass
        elif self.platform == "Linux":
            pass
