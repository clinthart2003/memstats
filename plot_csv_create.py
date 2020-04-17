import paramiko
from config import CONFIG
import datetime
import csv
import sys, os
import logging
script = os.path.basename(sys.argv[0])
logging.basicConfig(filename='./files/test_logs/%s.log' % script, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('test')

remotepath = "/var/log"
tstamp = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M")


def printlog(memorylog, grepname, tvalue, header):
    outfile = 'results/memory/%s-%s.csv' % (host, grepname)
    listfile = []
    with open(outfile, 'w') as f:
        x = [line.split() for line in memorylog]

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

        for i, line in zip(tvalue, x):
            # Convert GiB and TiB to KiB
            if ('m' in line[4]) or ('g' in line[4]) or ('t' in line[4]) or ('p' in line[4]):
                if 'm' in line[4]:
                    value = line[4].split('m')[0]
                    value = float(value) * 1024
                    line[4] = int(value)
                elif 'g' in line[4]:
                    value = line[4].split('g')[0]
                    value = float(value) * 1024 * 1024
                    line[4] = int(value)
                elif 't' in line[4]:
                    value = line[4].split('t')[0]
                    value = float(value) * 1024 * 1024 * 1024
                    line[4] = int(value)
                elif 'p' in line[4]:
                    value = line[4].split('p')[0]
                    value = float(value) * 1024 * 1024 * 1024 * 1024
                    line[6] = int(value)

            # Convert GiB and TiB to KiB
            if ('m' in line[5]) or ('g' in line[5]) or ('t' in line[5]) or ('p' in line[5]):
                if 'm' in line[5]:
                    value = line[5].split('m')[0]
                    value = float(value) * 1024
                    line[5] = int(value)
                elif 'g' in line[5]:
                    value = line[5].split('g')[0]
                    value = float(value) * 1024 * 1024
                    line[5] = int(value)
                elif 't' in line[5]:
                    value = line[5].split('t')[0]
                    value = float(value) * 1024 * 1024 * 1024
                    line[5] = int(value)
                elif 'p' in line[5]:
                    value = line[5].split('t')[0]
                    value = float(value) * 1024 * 1024 * 1024 * 1024
                    line[6] = int(value)

            # Convert GiB and TiB to KiB
            if ('m' in line[6]) or ('g' in line[6]) or ('t' in line[6]) or ('p' in line[6]):
                if 'm' in line[6]:
                    value = line[6].split('m')[0]
                    value = float(value) * 1024
                    line[6] = int(value)
                elif 'g' in line[6]:
                    value = line[6].split('g')[0]
                    value = float(value) * 1024 * 1024
                    line[6] = int(value)
                elif 't' in line[6]:
                    value = line[6].split('t')[0]
                    value = float(value) * 1024 * 1024 * 1024
                    line[6] = int(value)
                elif 'p' in line[6]:
                    value = line[6].split('t')[0]
                    value = float(value) * 1024 * 1024 * 1024 * 1024
                    line[6] = int(value)

        for i, line in zip(tvalue, x):
            line.insert(0, i)
            listfile.append(line)
        # listfile.insert(0, header)
        wr = csv.writer(f)
        temp = []
        for line in listfile:
            if (line[0] is None) or ('"' in line[0]) or ('"' in line) or (len(line[0]) == 0) or ('bash' in line[1]):
                print(line)
            else:
                temp.append(line)
        tmp = sorted(temp, key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))
        tmp.insert(0, header)
        for line in tmp:
            if (line[0] is None) or ('"' in line[0]) or ('"' in line) or (len(line[0]) == 0) or ('bash' in line[1]):
                print(line)
            else:
                # wr = csv.writer(f)
                wr.writerow(line)
        # return tvalue time stamps to the original state
        tvalue = orig_tvalue
    f.close()


def printlog2(memorylog, grepname, tvalue, header):
    outfile = 'results/memory/%s-%s.csv' % (host, grepname)
    listfile = []
    with open(outfile, 'w') as f:
        x = [line.split(',') for line in memorylog]

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

        for i, line in zip(tvalue, x):
            # print i
            line.insert(0, i)
            listfile.append(line)
        # listfile.insert(0, header)
        wr = csv.writer(f)
        temp = []
        for line in listfile:
            if (line[0] is None) or ('"' in line[0]) or ('"' in line) or (len(line[0]) == 0) or ('bash' in line[1]):
                print(line)
            else:
                temp.append(line)
        tmp = sorted(temp, key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))
        tmp.insert(0, header)
        for line in tmp:
            if (line[0] is None) or ('"' in line[0]) or ('"' in line) or (len(line[0]) == 0) or ('bash' in line[1]):
                print(line)
            else:
                # wr = csv.writer(f)
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
                # line = ','.join(line.split())
                line = ','.join(line.split(',,'))
                # print(line)
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
            line = line.split('DATE:')[1]
            # line = ','.join(line.split())
            # line = line.split(',')[0]
            # print line
            memorylog.append(line.strip('\n'))

    return memorylog

for host in CONFIG.graphhost:

    connection = False

    print(host)

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=CONFIG.username)
        connection = True
    except Exception as e:
        print("ssh connection to %s failed, skipping data collect attempts" % host)

    if connection is True:

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "tqcontroller"' % (remotepath, host)
            tqcontroller = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(tqcontroller, 'tqcontroller', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "supervisord" | grep threatq' % (remotepath, host)
            tqcontroller = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(tqcontroller, 'tq-supervisord', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "dynamo"' % (remotepath, host)
            dynamo = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(dynamo, 'dynamo', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "systemd-journal"' % (remotepath, host)
            journald = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(journald, 'systemd-journald', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "mysqld"' % (remotepath, host)
            mysql = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(mysql, 'mysqld', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "solr" | grep "java"' % (remotepath, host)
            solrmem = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(solrmem, 'solr', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "sda"' % (remotepath, host)
            iostats = grep_memory(cmd, "NONE")
            if len(iostats) < 1:
                cmd = r'cat %s/threatq-memory-%s.log | grep "vda"' % (remotepath, host)
                iostats = grep_memory(cmd, "NONE")
            header = ["Time",  "Device:", "rrqm/s",  "wrqm/s",  "r/s",   "w/s",  "rkB/s",  "wkB/s", "avgrq-sz", "avgqu-sz",   "await", "r_await", "w_await",  "svctm",  "%util"]
            printlog(iostats, 'iostat', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "KiB Mem :"' % (remotepath, host)
            mem = grep_memory2(cmd, "NONE")
            header = ["time", "Total", " ", "Free", " ", "Used", " ", "Buff/Cache"]
            printlog2(mem, 'KiB Mem', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "load average:"' % (remotepath, host)
            loadaverage = grep_memory3(cmd, "NONE")
            header = ['Time',    '1 Minute',   '5min',   '15min']
            printlog2(loadaverage, 'load average', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "proc,apache"' % (remotepath, host)
            httpd = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog2(httpd, 'httpd', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "memcached"' % (remotepath, host)
            memcached = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(memcached, 'memcached', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "port 11211"' % (remotepath, host)
            p11211 = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(p11211, '11211', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "port 5672"' % (remotepath, host)
            p5672 = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog(p5672, '5672', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

        try:
            cmd = r'cat %s/threatq-memory-%s.log | grep "DATE:"' % (remotepath, host)
            tvalue = grep_time(cmd)
            cmd = r'cat %s/threatq-memory-%s.log | grep "worker" | grep "artisan"' % (remotepath, host)
            worker = grep_memory(cmd, "NONE")
            header = ["time",  "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            printlog2(worker, 'worker', tvalue, header)

        except Exception as e:
            print("Error generating graph for: %s " % host)

    ssh.close()
