import paramiko
from config import CONFIG
import time

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(CONFIG.server, username=CONFIG.username)

# use shell for running the script to make-object-set
channel = ssh.invoke_shell()

remotepath = '/var/log'
localpath = './files/mem_logs'
def get_files():

    sftp = ssh.open_sftp()
    for filename in sftp.listdir('/var/log'):
        if 'threatq-memory' in filename:
            print (filename)
            remotefile = remotepath + '/' + filename
            localfile = localpath + '/' + filename
            sftp.get(remotefile, localfile)

    sftp.close()


get_files()
