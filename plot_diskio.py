import csv
import matplotlib.pyplot as plt, mpld3
import matplotlib.ticker as tkr
import matplotlib.dates as mdates
from datetime import datetime
from config import CONFIG


def func(x, pos):  # format function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))


def plot_topstats(infile='rkbults/memory/clint-test-mysqld.csv', proc='mysqld'):

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
                y1.append(content[0].strip())

                content = list(row[i] for i in wkb)
                y2.append(content[0].strip())

                content = list(row[i] for i in utilp)
                y3.append(content[0].strip())

                content = list(row[i] for i in ttime)
                try:
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        y_format = tkr.FuncFormatter(func)

        fig = plt.figure()  # the first figure
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(x, y1)
        ax1.plot(x, y2)
        plt.ylabel('Read/Write (KiB)')
        ax1.yaxis.set_major_formatter(y_format)
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax1.xaxis.set_major_formatter(myFmt)
        plt.xticks(rotation=45)
        ax1.set_title('%s: %s Disk IO' % (CONFIG.graphhost, proc))
        ax1.legend(["Read (kb)", "Write (kb)"], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(x, y3)
        ax2.yaxis.set_major_formatter(y_format)
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax2.xaxis.set_major_formatter(myFmt)
        plt.xticks(rotation=45)
        ax2.set_title('%s: %s Disk Utilization' % (CONFIG.graphhost, proc))
        plt.ylabel('Utilized (%)')
        ax2.legend(["% Utilized"], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        fig.set_size_inches(18, 30)
        plt.subplots_adjust(top=0.9, bottom=0.5, left=0.1, right=0.9, hspace=0.4)
        #fig.autofmt_xdate()

        plt.savefig("results/memory/%s_%s.svg" % (CONFIG.graphhost, proc), bbox_inches="tight", format="svg")
        plt.savefig("results/memory/%s_%s.png" % (CONFIG.graphhost, proc), bbox_inches="tight", format="png")

        plt.close()


plot_topstats(infile='results/memory/%s-iostat.csv' % CONFIG.graphhost, proc='IOStat')

"""
csvfiles = [
            ['results/memory/%s-iostat.csv' % CONFIG.graphhost, 'tqcontroller']
            ]

for process in csvfiles:

    try:
        plot_topstats(file=process[0], proc=process[1])
    except Exception as e:
        print ("There was an error generating: %s " % process[0])
"""