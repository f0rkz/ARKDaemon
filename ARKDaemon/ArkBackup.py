import os
import sys
import time
import tarfile
import fnmatch
from ARKDaemon.ServerQuery import ServerQuery
from ARKDaemon.ServerRcon import ServerRcon


class ArkBackup(object):
    def __init__(self, server_config):
        self.timestamp = time.strftime("%Y-%m-%d_%H.%M.%S")
        self.server_config = server_config
        self.backup_directory = os.path.join('ARK_BACKUPS')

    def do_backup(self):
        # Do a saveworld operation
        this = ServerQuery(ip='127.0.0.1', port=int(self.server_config['ARK']['query_port']))
        result = this.status()
        if result['status']:
            rcon = ServerRcon(ip='127.0.0.1',
                              port=int(self.server_config['ARK']['rcon_port']),
                              password=self.server_config['ARK']['serveradminpassword'],
                              ark_command='saveworld')
            print rcon.run_command()

        # Get a list of files to backup
        files = []
        for root, dirnames, filenames in os.walk('.'):
            for filename in fnmatch.filter(filenames, '*.arkprofile'):
                files.append(filename)
            for filename in fnmatch.filter(filenames, '*.arktribe'):
                files.append(filename)
            for filename in fnmatch.filter(filenames, '{}.ark'.format(self.server_config['ARK']['map'])):
                files.append(filename)

        print files

        # Make a tar file of the backup content
        #tar = tarfile.open(os.path.join(self.backup_directory,
        #                                'ARK_BACKUP-{}.tar.gz'.format(self.timestamp)
        #                                )
        #                   )

    def restore_backup(self):
        pass
