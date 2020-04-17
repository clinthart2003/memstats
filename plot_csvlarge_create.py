# Used to graph weeks or months worth of metric data.  Used in conjunction with plot_csvload_larg_js.py
# and getlogs.py.   Simply change the config.py graphhost list to a have the first server in the list
# you want graphed.

from config import CONFIG
import csv
import sys, os, subprocess, glob, datetime
from paramiko import SSHClient
import paramiko
from config import CONFIG
from scp import SCPClient
import logging
script = os.path.basename(sys.argv[0])
logging.basicConfig(filename='./files/test_logs/%s.log' % script, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('test')

# Global variables
remotepath = "./files/mem_logs"
tstamp = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M")
host = CONFIG.graphhost[0]


def printlog2(memorylog, grepname, tvalue, header):
    outfile = 'results/memory/%s-%s.csv' % (host, grepname)
    listfile = []
    with open(outfile, 'w') as f:
        x = [line.split(',') for line in memorylog]

        # Look at the difference between the number of timestamps and the
        # number of records that were collected
        print grepname
        print "Total grepped lines: %s" % len(x)
        print "Total Time Values: %s" % len(tvalue)
        orig_tvalue = tvalue
        if len(x) < len(tvalue):
            while len(x) != len(tvalue):
                tvalue.pop()
        print "Adjusted size of tvalue: %s" % len(tvalue)
        print ("")

        for line in x:
            for num, cell in enumerate(line):
                # print cell
                if '+' in cell:
                    line[num] = cell.replace('+', '0')
        for line in x:
            for num, cell in enumerate(line):
                # print cell
                if 'free' in cell:
                    line[num] = cell.replace('free', '')
        for line in x:
            for num, cell in enumerate(line):
                if ' used' in cell:
                    line[num] = cell.replace('used', '')
        for line in x:
            for num, cell in enumerate(line):
                if 'buff/cache' in cell:
                    line[num] = cell.replace('buff/cache', '')
            # print line

        for i, line in map(None, tvalue, x):
            # print i
            line.insert(0, i)
            listfile.append(line)
        # listfile.insert(0, header)
        wr = csv.writer(f)
        temp = []
        for line in listfile:
            if (line[0] is None) or ('"' in line[0])or ('"' in line) or (len(line[0]) == 0) or ('bash' in line[1]):
                print line
            else:
                temp.append(line)
        tmp = sorted(temp, key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))
        tmp.insert(0, header)
        for line in tmp:
            if (line[0] is None) or ('"' in line[0])or ('"' in line) or (len(line[0]) == 0) or ('bash' in line[1]):
                print line
            else:
                # wr = csv.writer(f)
                wr.writerow(line)
        # return tvalue time stamps to the original state
        tvalue = orig_tvalue
    f.close()

def grep_memory(cmd, skipstring):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""

    memorylog = []
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in output.stdout:
        if skipstring in line:
            continue
        else:
            memorylog.append(line.strip('\n'))

    return memorylog

def grep_memory2(cmd, skipstring):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""

    memorylog = []
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in output.stdout:
        if skipstring in line:
               continue
        else:
            line = ''.join(line.split('KiB Mem : '))
            line = ','.join(line.split('total,'))
            # line = ','.join(line.split())
            line = ','.join(line.split(',,'))
            # print (line)
            memorylog.append(line.strip('\n'))

    return memorylog

def grep_memory3(cmd, skipstring):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""
    memorylog = []
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in output.stdout:
        if skipstring in line:
            continue
        else:
            line = line.split('load average:')[1]
            # print line.strip()
            memorylog.append(line.strip('\n'))
    return memorylog


def getlogs():

    with SSHClient() as ssh:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('%s.threatq.com' % CONFIG.graphhost[0], username=CONFIG.username)
        with SCPClient(ssh.get_transport(), sanitize=lambda x: x) as scp:
            scp.get(remote_path='/var/log/threatq-memory-*.log', local_path='./results/memory')


def grep_time(cmd):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""

    memorylog = []
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    # print stdout
    for line in output.stdout:
        # print line
        line = line.split('DATE:')[1].strip()
        # print line
        memorylog.append(line.strip('\n'))

    return memorylog


""" Start script execution here """

getlogs()
tvalue = []
loadaverage = []
memory = []
javam = []

# filelist = glob.glob('./files/mem_logs/threatq-memory-%s*.log' % host)
filelist = glob.glob('./results/memory/threatq-memory-%s*.log' % host)

for file in filelist:
    # Collect DateTime
    cmd = r'cat %s | grep "DATE:"' % file
    temp = grep_time(cmd)
    for x in temp:
        tvalue.append(x)

    # Collect CPU Load Average
    cmd = r'cat %s | grep "load average:"' % file
    temp = grep_memory3(cmd, "NONE")
    for x in temp:
        loadaverage.append(x)

    # Collect System Memory
    cmd = r'cat %s | grep "KiB Mem :"' % file
    temp2 = grep_memory2(cmd, "NONE")
    for x in temp2:
        memory.append(x)

    #Java Memory
    cmd = r'cat %s | grep "proc,apache"' % file
    temp2 = grep_memory(cmd, "NONE")
    for x in temp2:
        javam.append(x)

header = ['Time', '1 Minute', '5min', '15min']
printlog2(loadaverage, 'load average', tvalue, header)
print ("done")

header = ["time", "Total", " ", "Free", " ", "Used", " ", "Buff/Cache"]
printlog2(memory, 'KiB Mem', tvalue, header)
print ("done")

header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
printlog2(httpd, 'httpd', tvalue, header)
print ("done")