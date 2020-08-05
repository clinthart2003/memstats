import paramiko
from config import CONFIG
import datetime
import csv
import sys, os, re
import itertools
import logging
script = os.path.basename(sys.argv[0])
logging.basicConfig(filename='./files/test_logs/%s.log' % script, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('test')

remotepath = "/var/log"
tstamp = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M")


def printlog(free, usedmem, grepname, tvalue, header):
    outfile = 'results/memory/%s-%s.csv' % (host, grepname)
    listfile = []
    finallist = []
    with open(outfile, 'w') as f:
        x = [line.split() for line in free]
        y = [line.split() for line in usedmem]

        # Look at the difference between the number of timestamps and the
        # number of records that were collected
        print(grepname)
        print("Total grepped lines: %s" % len(x))
        print("Total Time Values: %s" % len(tvalue))
        orig_tvalue = tvalue
        if len(x) < len(tvalue):
            while len(x) != len(tvalue):
                tvalue.pop()
        print("Adjusted size of tvalue: %s" % len(tvalue))
        print("")
        print()

        for i, line in zip(tvalue, x):
            line.insert(0, i)
            listfile.append(line)

        for i, line in zip (y, listfile):
            line.append(i[0])
            finallist.append(line)

        # for i in finallist:
            # print i

        wr = csv.writer(f)
        temp = []
        for line in finallist:
            if (line[0] is None) or ('"' in line[0]) or ('"' in line) or (len(line[0]) == 0) or ('bash' in line[1]):
                print(line)
            else:
                temp.append(line)
        # tmp = sorted(temp, key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))
        temp.insert(0, header)
        for line in temp:
            if (line[0] is None) or ('"' in line[0]) or ('"' in line) or (len(line[0]) == 0) or ('bash' in line[1]):
                print(line)
            else:
                # wr = csv.writer(f)
                #print line
                wr.writerow(line)
        # return tvalue time stamps to the original state
        tvalue = orig_tvalue
    f.close()


def grep_memory(cmd, skipstring):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""

    memorylog = []
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        for line in stdout.readlines():
            if skipstring in line:
                continue
            if "MB" in line:
                continue
            else:
                freemem = re.sub(r"\W", "", line.strip())
                if "free" in freemem:
                    memory = freemem.split('free')
                if "used" in freemem:
                    memory = freemem.split('used')
                memorylog.append(memory[1])

    return memorylog


def grep_time(cmd):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""

    memorylog = []
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        for line in stdout.readlines():
            line = line.split('DATE:')[1]
            # line = ','.join(line.split())
            # line = line.split(',')[0]
            # print line
            memorylog.append(line.strip('\n'))

    return memorylog

for host in CONFIG.graphhost:
    print(host)

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=CONFIG.username)

    cmd = r'cat %s/threatq-memory-%s-jvm.log | grep "DATE:"' % (remotepath, host)
    tvalue = grep_time(cmd)
    print(len(tvalue))
    cmd = r'cat %s/threatq-memory-%s-jvm.log | grep "\"free\":"' % (remotepath, host)
    free = grep_memory(cmd, "GB")
    print(len(free))
    cmd = r'cat %s/threatq-memory-%s-jvm.log | grep "\"used\":"' % (remotepath, host)
    usedmem = grep_memory (cmd, "GB")
    print(len(usedmem))
    header = ["time",  "Free Mem", "Used Mem"]
    printlog(free, usedmem, "JavaMem", tvalue, header)

    ssh.close()
