import paramiko
from config import CONFIG
import datetime
import csv
import itertools

remotepath = "/var/log"
tstamp = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M")


ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(CONFIG.server, username=CONFIG.username)


def printlog(memorylog, grepname, tvalue, header):
    outfile = 'results/memory/%s-%s-%s.csv' % (CONFIG.hostname, grepname, tstamp)
    listfile = []
    with open(outfile, 'w') as f:
        x = [line.split() for line in memorylog]

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

        for i,line in map(None, tvalue, x):
            # Convert GiB and TiB to KiB
            if ('g' in line[5]) or ('t' in line[5]):
                if 'g' in line[5]:
                    value = line[5].split('g')[0]
                    value = float(value) * 1024 * 1024
                    line[5] = int(value)

                elif 't' in line[5]:
                    value = line[5].split('t')[0]
                    value = float(value) * 1024 * 1024 * 1024
                    line[5] = int(value)

            # Convert GiB and TiB to KiB
            if ('g' in line[4]) or ('t' in line[4]):
                if 'g' in line[4]:
                    value = line[4].split('g')[0]
                    value = float(value) * 1024 * 1024
                    line[4] = int(value)

                elif 't' in line[4]:
                    value = line[4].split('t')[0]
                    value = float(value) * 1024 * 1024 * 1024
                    line[4] = int(value)

            # Convert GiB and TiB to KiB
            if ('g' in line[6]) or ('t' in line[6]):

                if 'g' in line[6]:
                    value = line[6].split('g')[0]
                    value = float(value) * 1024 * 1024
                    line[6] = int(value)
                elif 't' in line[6]:
                    value = line[6].split('t')[0]
                    value = float(value) * 1024 * 1024 * 1024
                    line[6] = int(value)

        for i, line in map(None, tvalue, x):
            line.insert(0, i)
            listfile.append(line)
        listfile.insert(0, header)
        for line in listfile:
            wr = csv.writer(f)
            wr.writerow(line)
        #return tvalue time stamps to the original state
        tvalue = orig_tvalue
    f.close()


def printlog2(memorylog, grepname, tvalue, header):
    outfile = 'results/memory/%s-%s-%s.csv' % (CONFIG.hostname, grepname, tstamp)
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
            if '+' in line[0]:
                line[0] = line[0].replace('+', '0')

            if len(line) > 4:
                if '+' in line[5]:
                    line[5] = line[5].replace('+', '0,')

        for i,line in map(None, tvalue,x):
            line.insert(0, i)
            listfile.append(line)
        listfile.insert(0, header)
        for line in listfile:
            wr = csv.writer(f)
            wr.writerow(line)
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
            else:
                memorylog.append(line.strip('\n'))

    return memorylog


def grep_memory2(cmd, skipstring):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""

    memorylog = []
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        for line in stdout.readlines():
            if skipstring in line:
                continue
            else:
                line = ''.join(line.split('KiB Mem : '))
                line = ','.join(line.split('total,'))
                line = ','.join(line.split())
                line = ','.join(line.split(',,'))
                print (line)
                memorylog.append(line.strip('\n'))

    return memorylog


def grep_memory3(cmd, skipstring):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""

    memorylog = []
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        for line in stdout.readlines():
            if skipstring in line:
                continue
            else:
                line = line.split('load average:')[1]
                memorylog.append(line.strip('\n'))
    return memorylog


def grep_time(cmd):
    """ skipsring is used to exclude any data that may alreayd be in other greps"""

    memorylog = []
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        for line in stdout.readlines():
            line = line.split ('top - ')[1]
            line = ','.join(line.split())
            line = line.split(',')[0]
            memorylog.append(line.strip('\n'))

    return memorylog

"""
depricated for ssh accessing directly from server 
def grep_memoryfile(infile, grepstring, skipstring):
    memorylog = []
    with open(infile, 'r') as f:
        for line in f.readlines():
            if grepstring in line:
                if skipstring in line:
                    continue
                else:
                    memorylog.append(line.strip('\n'))
            else:
                continue

    return memorylog
"""


def main():

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "tqcontroller"' % (remotepath, CONFIG.hostname)
    tqcontroller = grep_memory(cmd, "NONE")
    header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
    printlog(tqcontroller, 'tqcontroller', tvalue, header)

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "/opt/threatq/python/bin/dynamo"' % (remotepath, CONFIG.hostname)
    dynamo = grep_memory(cmd, "NONE")
    header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
    printlog(dynamo, 'dynamo', tvalue, header)

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "systemd-journald"' % (remotepath, CONFIG.hostname)
    dynamo = grep_memory(cmd, "NONE")
    header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
    printlog(dynamo, 'systemd-journald', tvalue, header)

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "mysqld"' % (remotepath, CONFIG.hostname)
    mysql = grep_memory(cmd, "NONE")
    header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
    printlog(mysql, 'mysqld', tvalue, header)

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "java -server"' % (remotepath, CONFIG.hostname)
    solrmem = grep_memory(cmd, "NONE")
    header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
    printlog(solrmem, 'solr', tvalue, header)

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "sda"' % (remotepath, CONFIG.hostname)
    iostats = grep_memory(cmd, "NONE")
    header = ["Time",  "Device:", "rrqm/s",  "wrqm/s",  "r/s",   "w/s",  "rkB/s",  "wkB/s", "avgrq-sz", "avgqu-sz",   "await", "r_await", "w_await",  "svctm",  "%util"]
    printlog(iostats, 'iostat', tvalue, header)

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "KiB Mem :"' % (remotepath, CONFIG.hostname)
    mem = grep_memory2(cmd, "NONE")
    header =["time", "Total", " ", "Free", " ", "Used", " ", "Buff/Cache"]
    printlog2(mem, 'KiB Mem', tvalue, header)

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "load average:"' % (remotepath, CONFIG.hostname)
    loadaverage = grep_memory3(cmd, "NONE")
    header =['Time',    '1 Minute',   '5min',   '15min']
    printlog2(loadaverage, 'load average', tvalue, header)


    # Get Feed stats out of files
    """
    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "DeepSightAdvancedIPReputationAttackXMLF"' % (remotepath, CONFIG.hostname)
    feeds = grep_memory(cmd, 'tqcontroller')
    header = ['time', 'PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND']
    printlog(feeds, 'DeepSightAdvancedIP', tvalue, header)

    cmd = r'cat %s/threatq-memory-%s.log | grep "top - "' % (remotepath, CONFIG.hostname)
    tvalue = grep_time(cmd)
    cmd = r'cat %s/threatq-memory-%s.log | grep "erlang/erts-5.10.4/bin/beam.smp"' % (remotepath, CONFIG.hostname)
    feeds = grep_memory(cmd, 'tqcontroller')
    header = ['time', 'PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND']
    printlog(feeds, 'beam.smp', tvalue, header)
    """

if __name__ == "__main__":


    main()

    ssh.close()