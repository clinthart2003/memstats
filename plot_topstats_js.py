import csv
import matplotlib.pyplot as plt, mpld3
from mpld3 import plugins
import matplotlib.ticker as tkr
import matplotlib.dates as mdates
from datetime import datetime
from config import CONFIG
import locale
locale.setlocale(locale.LC_ALL, '')

tstamp = datetime.now().strftime("%Y-%m-%d")

def func(x, pos):  # format function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))


def plot_topstats(file='TQ_Setup/results/memory/clint-test-systemd-journald.csv', proc='mysqld'):

    array = []

    with open(file, 'r') as csvfile:

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
                y1.append(int(content[0].strip()))

                content = list(row[i] for i in share)
                y2.append(int(content[0].strip()))

                content = list(row[i] for i in cpu)
                y3.append(float(content[0].strip()))

                content = list(row[i] for i in memp)
                y4.append(float(content[0].strip()))

                content = list(row[i] for i in ttime)
                try:
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        y_format = tkr.FuncFormatter(func)

        fig = plt.figure()  # the first figure
        ax1 = fig.add_subplot(2,1,1)
        l1 = ax1.plot(x, y1, marker='.')
        l2 = ax1.plot(x, y2, marker='.')
        ax1.yaxis.set_major_formatter(y_format)
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax1.xaxis.set_major_formatter(myFmt)


        # format tootip values
        ttvalues1 = []
        ttvalues2 = []

        for i, s in enumerate(y1):
            ttvalues1.append(format(int(s), ','))

        for i, s in enumerate(y2):
            ttvalues2.append(format(int(s), ','))

        tt1 = plugins.PointLabelTooltip(l1[0], labels=ttvalues1)
        tt2 = plugins.PointLabelTooltip(l2[0], labels=ttvalues2)

        ax1.set_title('%s: %s Memory (Kib)' % (host, proc))
        plt.ylabel('Memory (KiB)')
        fig.set_size_inches(15, 8)
        plt.xticks(rotation=45)
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.4)


        ax2 = fig.add_subplot(2, 1, 2)
        l3 = ax2.plot(x, y3, marker='.')
        tt3 = plugins.PointLabelTooltip(l3[0], labels=y3)
        l4 = ax2.plot(x, y4, marker='.')
        tt4 = plugins.PointLabelTooltip(l4[0], labels=y4)
        ax2.yaxis.set_major_formatter(y_format)
        ax2.xaxis.set_major_formatter(myFmt)
        ax2.set_title('%s: %s CPU Usage' % (host, proc))
        plt.ylabel('CPU %')
        plt.xticks(rotation=45)

        labels1 = ["RES", "SHA"]
        labels2 = ["CPU %", "Mem %"]
        line_collections1 = [l1, l2]
        line_collections2 = [l3, l4]
        plugins.connect(fig, plugins.InteractiveLegendPlugin(line_collections1, labels1, ax=ax1), tt1, tt2)
        plugins.connect(fig, plugins.InteractiveLegendPlugin(line_collections2, labels2, ax=ax2), tt3, tt4)

        mpld3.save_html(fig, "results/memory/%s_%s_%s.html" % (host, proc, tstamp))

        plt.close()


# plot_topstats(file='results/memory/%s-mysqld.csv' % CONFIG.graphhost, proc='mysqld')


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
