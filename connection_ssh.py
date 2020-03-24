'''
Connection by ssh to server, and download log from server to local directory.
Checking work status supervisor.
'''
# -*- coding: utf-8 -*-
import os

import paramiko

import config
import logger


class ConnectToFirstServer():
    def __init__(self):
        self.ssh_host = config.FIRST_SSH_HOST
        self.ssh_port = config.FIRST_SSH_PORT
        self.username = config.FIRST_SSH_USERNAME
        self.password = config.FIRST_SSH_PASSWORD
        self.path_server_log = config.PATH_SERVER_LOG
        self.local_logs_directory = config.LOCAL_LOGS_DIRECTORY
    
    def connect_ssh(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ssh_host, 
                        port=self.ssh_port, 
                        username=self.username, 
                        password=self.password)
        except:
            logger.create('Произошла ошибка при попытке'
                          ' соединения с сервером по SSH')
            return
        return ssh


    def download_pattern(self, path):
        try:
            ssh = self.connect_ssh()
            sftp = ssh.open_sftp()
            sftp.get(os.path.join(*path), os.path.join(os.getcwd(), 
                                                    self.local_logs_directory, 
                                                    path[-1]))
            ssh.close()
        except:
            logger.create('Произошла ошибка при попытке'
                          ' загрузки файла по SFTP')

    def download_log(self):
        self.download_pattern(self.path_server_log)

    
    def check_supervisor(self):
        try:
            
            ssh = self.connect_ssh()
            self.supervisor_count = 0
            stdin, stdout, stderr = ssh.exec_command(
                                                'service supervisor status')
            data = (stdout.read() + stderr.read()).decode('utf-8')
            for item in config.SUPERVISOR_LIST:
                if item in data:
                    self.supervisor_count += 1
            ssh.close()
            return self.supervisor_count
        except:
            logger.create('Произошла ошибка при'
                          ' попытке проверки статуса supervisor')

class ConnectToSecondServer(ConnectToFirstServer):
    def __init__(self):
        self.ssh_host = config.SECOND_SSH_HOST
        self.ssh_port = config.SECOND_SSH_PORT
        self.username = config.SECOND_SSH_USERNAME
        self.password = config.SECOND_SSH_PASSWORD
        self.local_logs_directory = config.LOCAL_LOGS_DIRECTORY
        
        self.path_trassir_log = config.PATH_TRASSIR_LOG
        self.path_video_progress_log = config.PATH_VIDEO_PROGRESS_LOG
    
    def download_trassir_log(self):
        self.download_pattern(self.path_trassir_log)
    
    def download_video_progress_log(self):
        self.download_pattern(self.path_video_progress_log)
        
        
if __name__ == '__main__':
    ConnectToFirstServer().download_log()