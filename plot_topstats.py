import csv
import matplotlib.pyplot as plt, mpld3
import matplotlib.ticker as tkr
import matplotlib.dates as mdates
from datetime import datetime
from config import CONFIG

tstamp = datetime.now().strftime("%Y-%m-%d")

def func(x, pos):  # format function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

array = []


def plot_topstats(infile='results/memory/clint-test-mysqld.csv', proc='mysqld'):

    with open(infile, 'r') as csvfile:

        for line in csvfile.readlines():
            # get number of columns
            array = line.split(',')
            first_item = array[0]

        # num_columns = len(array)
        csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=',')
        ttime = [0]
        res = [6]
        share = [7]
        cpu = [9]
        memp = [10]
        x = []
        y1 = []
        y2 = []
        y3 = []
        y4 = []

        count = 0

        for row in reader:
            if count == 0:
                count += 1
            else:
                content = list(row[i] for i in res)
                y1.append(content[0].strip())

                content = list(row[i] for i in share)
                y2.append(int(content[0].strip()))

                content = list(row[i] for i in cpu)
                y3.append(content[0].strip())

                content = list(row[i] for i in memp)
                y4.append(content[0].strip())

                content = list(row[i] for i in ttime)
                try:
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        y_format = tkr.FuncFormatter(func)

        fig = plt.figure()  # the first figure
        # fig.suptitle(page_title, fontsize="x-large")
        ax1 = fig.add_subplot(2,1,1)
        ax1.plot(x, y1)
        ax1.plot(x, y2)
        plt.ylabel('Memory (KiB)')
        ax1.yaxis.set_major_formatter(y_format)
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax1.xaxis.set_major_formatter(myFmt)
        plt.xticks(rotation=45)
        plt.subplots_adjust(top=0.9, bottom=0.5, left=0.1, right=0.9, hspace=0.4)
        ax1.set_title('%s: %s Memory (Kib)' % (CONFIG.graphhost, proc))
        ax1.legend(["Reserved", "Shared"], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        ax2 = fig.add_subplot(2,1,2)
        ax2.plot(x, y3)
        ax2.plot(x, y4)
        ax2.yaxis.set_major_formatter(y_format)
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax2.xaxis.set_major_formatter(myFmt)
        plt.xticks(rotation=45)
        ax2.set_title('%s: %s CPU Usage' % (CONFIG.graphhost, proc))
        plt.ylabel('CPU %')
        ax2.legend(["CPU %", "Mem %"], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        #ax2.autofmt_xdate()
        fig.set_size_inches(18, 30)
        plt.subplots_adjust(top=0.9, bottom=0.5, left=0.1, right=0.9, hspace=0.4)

        mpld3.save_html(fig, "results/memory/%s_%s_%s.html" % (host, proc, tstamp))

        plt.close()


# plot_topstats(infile='results/memory/%s-mysqld.csv' % CONFIG.graphhost, proc='mysqld')




for host in CONFIG.graphhost:

    csvfiles = [['results/memory/%s-mysqld.csv' % host, 'mysqld'],
                ['results/memory/%s-solr.csv' % host, 'solr'],
                ['results/memory/%s-systemd-journald.csv' % host, 'systemd-journald'],
                ['results/memory/%s-dynamo.csv' % host, 'dynamo'],
                ['results/memory/%s-tqcontroller.csv' % host, 'tqcontroller'],
                ['results/memory/%s-tq-supervisord.csv' % host, 'tq-supervisor'],
                ['results/memory/%s-httpd.csv' % host, 'httpd'],
                ['results/memory/%s-worker.csv' % host, 'worker'],
                ['results/memory/%s-memcached.csv' % host, 'memcached'],
                ['results/memory/%s-11211.csv' % host, 'container_11211'],
                ['results/memory/%s-5672.csv' % host, 'container_5672']
                ]

    for process in csvfiles:

        try:
            plot_topstats(file=process[0], proc=process[1])
        except Exception as e:
            print ("There was an error generating: %s " % process[0])
