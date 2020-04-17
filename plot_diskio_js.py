import csv
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import matplotlib.ticker as tkr
from matplotlib.ticker import FormatStrFormatter
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


def plot_topstats(infile='TQ_Setup/results/memory/clint-test-load average.csv', proc='IOStat'):

    array = []

    with open(infile, 'r') as csvfile:

        for line in csvfile.readlines():
            # get number of columns
            array = line.split(',')
            first_item = array[0]

        # num_columns = len(array)
        csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=',')
        ttime = [0]
        rkb = [6]
        wkb = [7]
        utilp = [14]

        x = []
        y1 = []
        y2 = []
        y3 = []

        count = 0

        for row in reader:
            if count == 0:
                count += 1
            else:
                content = list(row[i] for i in rkb)
                y1.append(float(content[0].strip()))

                content = list(row[i] for i in wkb)
                y2.append(float(content[0].strip()))

                content = list(row[i] for i in utilp)
                y3.append(float(content[0].strip()))

                content = list(row[i] for i in ttime)
                try:
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        y_format = tkr.FuncFormatter(func)

        fig = plt.figure()  # the first figure
        ax1 = fig.add_subplot(2, 1, 1)
        l1 = ax1.plot(x, y1, marker='.')
        l2 = ax1.plot(x, y2, marker='.')
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax1.xaxis.set_major_formatter(myFmt)

        # format tootip values
        ttvalues1 = []
        ttvalues2 = []

        for i, s in enumerate(y1):
            ttvalues1.append(format(float(s), ','))

        for i, s in enumerate(y2):
            ttvalues2.append(format(float(s), ','))

        tt1 = plugins.PointLabelTooltip(l1[0], labels=ttvalues1)
        tt2 = plugins.PointLabelTooltip(l2[0], labels=ttvalues2)

        ax1.set_title('%s: %s Memory (KiB)' % (host, proc))
        plt.ylabel('Read/Write (KiB)')
        # fig.set_size_inches(18, 12)
        fig.set_size_inches(15, 8)
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        plt.xticks(rotation=45)
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.3)


        ax2 = fig.add_subplot(2, 1, 2)
        l3 = ax2.plot(x, y3, marker='.')
        tt3 = plugins.PointLabelTooltip(l3[0], labels=y3)
        ax2.yaxis.set_major_formatter(y_format)
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax2.xaxis.set_major_formatter(myFmt)
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        ax2.tick_params(axis='both', which='major', pad=20)

        ax2.set_title('%s: %s Disk Utilization' % (host, proc))
        plt.ylabel('Utilized (%)')
        plt.xticks(rotation=45)
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=1)

        labels1 = ["Read", "Write"]
        labels2 = ["% Util"]
        line_collections1 = [l1, l2]
        line_collections2 = [l3]
        plugins.connect(fig, plugins.InteractiveLegendPlugin(line_collections1, labels1, ax=ax1), tt1, tt2)
        plugins.connect(fig, plugins.InteractiveLegendPlugin(line_collections2, labels2, ax=ax2), tt3)

        mpld3.save_html(fig, "results/memory/%s_%s_%s.html" % (host, proc, tstamp))

        plt.close()

for host in CONFIG.graphhost:
    plot_topstats(infile='results/memory/%s-iostat.csv' % host, proc='IOStat')
