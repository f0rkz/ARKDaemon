import fnmatch
import os
import platform
import tarfile
import time

from ARKDaemon.ServerQuery import ServerQuery
from ARKDaemon.ServerRcon import ServerRcon


class ArkBackup(object):
    def __init__(self, config):
        self.timestamp = time.strftime("%Y-%m-%d_%H.%M.%S")
        self.config = config
        self.platform = platform.system()
        self.backup_directory = os.path.join('ARK_BACKUPS')
        self.ark_saved_dir = os.path.join('ARK', 'ShooterGame', 'Saved')
        self.ark_config_dir_windows = os.path.join('ARK', 'ShooterGame', 'Saved', 'Config', 'WindowsServer')
        self.ark_config_dir_linux = os.path.join('ARK', 'ShooterGame', 'Saved', 'Config', 'LinuxServer')

    def do_backup(self):
        # Do a saveworld operation
        result = {}
        this = ServerQuery(ip='127.0.0.1', port=int(self.config['ARK']['query_port']))
        query = this.status()
        if query['status']:
            rcon = ServerRcon(ip='127.0.0.1',
                              port=int(self.config['ARK']['rcon_port']),
                              password=self.config['ARK']['serveradminpassword'],
                              ark_command='saveworld')
            print rcon.run_command()

        # Get a list of files to backup
        files = []
        for root, dirnames, filenames in os.walk(self.ark_saved_dir):
            # Backup arkprofiles
            for filename in fnmatch.filter(filenames, '*.arkprofile'):
                files.append(os.path.join('SavedArks', filename))
            # Backup tribes
            for filename in fnmatch.filter(filenames, '*.arktribe'):
                files.append(os.path.join('SavedArks', filename))
            # Backup the map file
            for filename in fnmatch.filter(filenames, '{}.ark'.format(self.config['ARK']['map'])):
                files.append(os.path.join('SavedArks', filename))

        if self.platform == 'Windows':
            for root,dirnames,filenames in os.walk(self.ark_config_dir_windows):
                # Backup GameUserSettings.ini
                for filename in fnmatch.filter(filenames, 'GameUserSettings.ini'):
                    files.append(os.path.join('Config', 'WindowsServer', filename))
                # Backup Game.ini
                for filename in fnmatch.filter(filenames, 'Game.ini'):
                    files.append(os.path.join('Config', 'WindowsServer', filename))

        elif self.platform == 'Linux':
            for root, dirnames, filenames in os.walk(self.ark_config_dir_linux):
                # Backup GameUserSettings.ini
                for filename in fnmatch.filter(filenames, 'GameUserSettings.ini'):
                    files.append(os.path.join('Config', 'LinuxServer', filename))
                # Backup Game.ini
                for filename in fnmatch.filter(filenames, 'Game.ini'):
                    files.append(os.path.join('Config', 'LinuxServer', filename))

        # Make a tar file of the backup content
        tar = tarfile.open(os.path.join(self.backup_directory, 'ARK_BACKUP-{}.tar.gz'.format(self.timestamp)), 'w:gz')
        for file in files:
            tar.add(os.path.join(self.ark_saved_dir, file))
        tar.close()

        result['status'] = True
        result['backup'] = file

        return result


    def restore_backup(self):
        pass
