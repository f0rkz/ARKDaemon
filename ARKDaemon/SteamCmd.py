import os
import os.path
import platform
import subprocess
import sys
import tarfile
import urllib
import zipfile
import fnmatch
from shutil import copytree, rmtree
from ARKDaemon.ZUnpack import ZUnpack


class SteamCmd(object):
    def __init__(self, appid, mod_id=False):
        # type: (object) -> object
        self.os = os.name
        self.platform = platform.system()
        self.steamcmd_download_linux = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
        self.steamcmd_download_windows = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
        self.steamcmd_path = os.path.join('steamcmd')
        self.install_dir = os.path.join(os.getcwd(), 'ARK')
        self.appid = appid
        self.mod_id = mod_id

    def install_steamcmd(self, force=False):
        # Installs steamcmd for windows
        if self.platform == "Windows":
            if os.path.exists(os.path.join(self.steamcmd_path, 'steamcmd.exe')) and force is False:
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
            sys.exit("Unsupported system. I detected {}.".format(self.platform))

    # Command will update/install gamefiles.
    def install_gamefiles(self):
        if self.platform == "Windows":
            steamcmd_run = '{steamcmd_path}\steamcmd.exe ' \
                           '+@NoPromptForPassword 1 ' \
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
                           '+@NoPromptForPassword 1 ' \
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

        else:
            sys.exit("Unsupported system. I detected {}.".format(self.platform))

    def install_mod(self):
        if self.platform == "Windows":
            steamcmd_run = '{steamcmd_path}\steamcmd.exe ' \
                           '+@NoPromptForPassword 1 ' \
                           '+login anonymous ' \
                           '+workshop_download_item {my_appid} {my_modid} ' \
                           '+quit' \
                .format(steamcmd_path=self.steamcmd_path,
                        my_appid=self.appid,
                        my_modid=self.mod_id)
            subprocess.call(steamcmd_run, shell=True)
            workshop_install_path = os.path.join(self.steamcmd_path,
                                                 'steamapps',
                                                 'workshop',
                                                 'content',
                                                 self.appid,
                                                 self.mod_id,
                                                 'WindowsNoEditor'
                                                 )
            post_install_path = os.path.join(self.install_dir,
                                             'ShooterGame',
                                             'Content',
                                             'Mods',
                                             self.mod_id
                                             )
            # Delete the current mod directory if any exists.
            if os.path.exists(post_install_path):
                print "Deleting current mod contents and replacing it."
                rmtree(post_install_path, ignore_errors=True)

            # Go through the .z and .z.uncompressed_size files, extract them, and delete the source .z* file
            #matches = []
            for root,dirnames,filenames in os.walk(workshop_install_path):
                for filename in fnmatch.filter(filenames, '*.z'):
                    #matches.append(os.path.join(root, filename))
                    this = ZUnpack(src_file=str(os.path.join(root, filename)),
                                   dst_file=str(os.path.join(root, filename.split('.z')[0]))
                                   )
                    this.z_unpack()
                    # Remove the old file:
                    os.remove(os.path.join(root, filename))

                #for filename in fnmatch.filter(filenames, '*.z.uncompressed_size'):
                #    #matches.append(os.path.join(root, filename))
                #    this = ZUnpack(src_file=str(os.path.join(root, filename)),
                #                   dst_file=str(os.path.join(root, filename.split('.z')[0]))
                #                   )
                #    this.z_unpack()
                #    # Remove the old file:
                #    os.remove(os.path.join(root, filename))

            # Copy the contents of the mod to the proper location
            print "Copying mod contents to ARK"
            copytree(workshop_install_path, post_install_path, symlinks=False)
            print "All operations completed. Mod ID: {} copied to: {}".format(self.mod_id, post_install_path)

        elif self.platform == "Linux":
            steamcmd_run = '{steamcmd_path}/steamcmd.sh ' \
                           '+@NoPromptForPassword 1 ' \
                           '+login anonymous ' \
                           '+workshop_download_item {my_appid} {my_modid} ' \
                           '+quit' \
                .format(steamcmd_path=self.steamcmd_path,
                        my_appid=self.appid,
                        my_modid=self.mod_id)
            subprocess.call(steamcmd_run, shell=True)
            workshop_install_path = os.path.join(self.steamcmd_path,
                                                 'steamapps',
                                                 'workshop',
                                                 'content',
                                                 self.appid,
                                                 self.mod_id,
                                                 'WindowsNoEditor'
                                                 )
            post_install_path = os.path.join(self.install_dir,
                                             'ShooterGame',
                                             'Content',
                                             'Mods',
                                             self.mod_id
                                             )
            # Delete the current mod directory if any exists.
            if os.path.exists(post_install_path):
                print "Deleting current mod contents and replacing it."
                rmtree(post_install_path, ignore_errors=True)

            # Go through the .z and .z.uncompressed_size files, extract them, and delete the source .z* file
            # matches = []
            for root, dirnames, filenames in os.walk(workshop_install_path):
                for filename in fnmatch.filter(filenames, '*.z'):
                    # matches.append(os.path.join(root, filename))
                    this = ZUnpack(src_file=str(os.path.join(root, filename)),
                                   dst_file=str(os.path.join(root, filename.split('.z')[0]))
                                   )
                    this.z_unpack()
                    # Remove the old file:
                    os.remove(os.path.join(root, filename))

                #for filename in fnmatch.filter(filenames, '*.z.uncompressed_size'):
                #    # matches.append(os.path.join(root, filename))
                #    this = ZUnpack(src_file=str(os.path.join(root, filename)),
                #                   dst_file=str(os.path.join(root, filename.split('.z')[0]))
                #                   )
                #    this.z_unpack()
                #    # Remove the old file:
                #    os.remove(os.path.join(root, filename))

            # Copy the contents of the mod to the proper location
            print "Copying mod contents to ARK"
            copytree(workshop_install_path, post_install_path, symlinks=False)
            print "All operations completed. Mod ID: {} copied to: {}".format(self.mod_id, post_install_path)
