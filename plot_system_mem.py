import csv
import matplotlib.pyplot as plt, mpld3
import matplotlib.ticker as tkr
import matplotlib.dates as mdates
from datetime import datetime
from config import CONFIG
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

def func(x, pos):  # format function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

def plot_topstats(infile='results/memory/%s-KiB Mem.csv' % CONFIG.graphhost, proc='KiB Mem'):

    array = []

    with open(infile, 'r') as csvfile:

        # get number of columns
        for line in csvfile.readlines():
            array = line.split(',')
            first_item = array[0]

        num_columns = len(array)
        csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=',')
        ttime = [0]
        free = [3]
        used = [5]
        buff = [7]
        x = []
        y1 = []
        y2 = []
        y3 = []

        count = 0
        t = 0
        for row in reader:
            if count == 0:
                count += 1
            else:
                content = list(row[i] for i in free)
                y1.append(content[0].strip())

                content = list(row[i] for i in used)
                y2.append(int(content[0].strip()))

                content = list(row[i] for i in buff)
                y3.append(content[0].strip())

                content = list(row[i] for i in ttime)
                try:
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        # print y2

        y4 = [int(a) + int(b) for a, b in zip(y1, y3)]

        # print y4

        y_format = tkr.FuncFormatter(func)

        fig = plt.figure()  # the first figure
        ax = plt.subplot(1, 1, 1)
        ax.plot(x, y2)
        ax.plot(x, y4)
        ax.yaxis.set_major_formatter(y_format)
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax.xaxis.set_major_formatter(myFmt)


        plt.legend(["Used", "Free + Buff/Cache"], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax.set_title('%s: %s Disk IO' % (CONFIG.graphhost, proc))
        plt.ylabel('Memory (KiB)')
        fig.autofmt_xdate()

        fig.set_size_inches(12, 6)
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.05, right=0.9, hspace=0.4)

        plt.savefig("results/memory/%s_%s.svg" % (CONFIG.graphhost, proc), bbox_inches="tight", format="svg")
        plt.savefig("results/memory/%s_%s.png" % (CONFIG.graphhost, proc), bbox_inches="tight", format="png")

        plt.close()

plot_topstats(infile='results/memory/%s-KiB Mem.csv' % CONFIG.graphhost, proc='KiB Mem')

"""
csvfiles = [
            ['results/memory/%s-KiB Mem.csv' % CONFIG.graphhost, 'KiB Mem']
            ]

for process in csvfiles:

    try:
        plot_topstats(infile=process[0], proc=process[1])
    except Exception as e:
        print ("There was an error generating: %s " % process[0])
"""