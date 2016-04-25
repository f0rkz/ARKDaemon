import fnmatch
import os
import os.path
import platform
import subprocess
import sys
import tarfile
import urllib
import zipfile
from shutil import copytree, rmtree

from ARKDaemon.ZUnpack import ZUnpack


class SteamCmd(object):
    def __init__(self, appid, mod_id=False):
        self.os = os.name
        self.platform = platform.system()
        self.steamcmd_path = os.path.join('steamcmd')
        self.install_dir = os.path.join(os.getcwd(), 'ARK')
        self.appid = appid
        self.mod_id = mod_id
        if platform.system() == "Windows":
            self.steamcmd_download = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
            self.steamcmd_bin = os.path.join(self.steamcmd_path, 'steamcmd.exe')
            self.steamcmd_compressed = os.path.join(self.steamcmd_path, 'steamcmd.zip')
        else:
            self.steamcmd_download = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
            self.steamcmd_bin = os.path.join(self.steamcmd_path, 'steamcmd.sh')
            self.steamcmd_compressed = os.path.join(self.steamcmd_path, 'steamcmd.tar.gz')

    def extract_steamcmd(self, platform):
        result = {}
        if platform == "Windows":
            with zipfile.ZipFile(self.steamcmd_compressed, 'r') as z:
                z.extractall(self.steamcmd_path)
        else:
            with tarfile.open(self.steamcmd_compressed, 'r:gz') as z:
                z.extractall(self.steamcmd_path)

        result['error'] = False
        result['message'] = "Steamcmd installed to ./{}".format(self.steamcmd_path)

        return result

    def install_steamcmd(self, force=False):
        result = {}
        if os.path.exists(self.steamcmd_bin) and force is False:
            result['error'] = True
            result['message'] = "Steamcmd already installed. No need for reinstall."
        else:
            urllib.urlretrieve(self.steamcmd_download, self.steamcmd_compressed)
            extract = self.extract_steamcmd(self.platform)
            result['error'] = extract['error']
            result['message'] = extract['message']

        return result

    # Command will update/install gamefiles.
    def install_gamefiles(self):
        result = {}
        steamcmd_run = '{steamcmd_bin} ' \
                       '+@NoPromptForPassword 1 ' \
                       '+login anonymous ' \
                       '+force_install_dir {install_dir} ' \
                       '+app_update {my_appid} ' \
                       'validate ' \
                       '+quit ' \
                .format(steamcmd_bin=self.steamcmd_bin,
                        steamcmd_path=self.steamcmd_path,
                        install_dir=self.install_dir,
                        my_appid=self.appid,
                        )
        subprocess.call(steamcmd_run, shell=True)
        result['error'] = False
        result['message'] = "All files installed to {}".format(self.install_dir)

        return result

    def install_mod(self):
        result = {}
        steamcmd_run = '{steamcmd_bin} ' \
                       '+@NoPromptForPassword 1 ' \
                       '+login anonymous ' \
                       '+workshop_download_item {my_appid} {my_modid} ' \
                       '+quit' \
            .format(steamcmd_bin=self.steamcmd_bin,
                    steamcmd_path=self.steamcmd_path,
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
        if os.path.exists(post_install_path):
            rmtree(post_install_path, ignore_errors=True)

        for root, dirnames, filenames in os.walk(workshop_install_path):
            for filename in fnmatch.filter(filenames, '*.z'):
                this = ZUnpack(src_file=str(os.path.join(root, filename)),
                               dst_file=str(os.path.join(root, filename.split('.z')[0]))
                               )
                this.z_unpack()
                # Remove the old file:
                os.remove(os.path.join(root, filename))

            # We don't need the .z.uncompressed_size files.
            for filename in fnmatch.filter(filenames, '*.z.uncompressed_size'):
                os.remove(os.path.join(root, filename))

        # Copy the contents of the mod to the proper location
        copytree(workshop_install_path, post_install_path, symlinks=False)
        result['error'] = False
        result['message'] = "All operations completed. Mod ID: {} copied to: {}".format(self.mod_id, post_install_path)

        return result
