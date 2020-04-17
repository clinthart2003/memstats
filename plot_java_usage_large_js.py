import csv
import matplotlib.pyplot as plt, mpld3
import matplotlib.ticker as tkr
import matplotlib.dates as mdates
from mpld3 import plugins
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


def plot_topstats(file='results/memory/qa-gold01-JavaMem.csv', proc='Java'):

    array = []

    with open(file, 'r') as csvfile:

        # get number of columns
        for line in csvfile.readlines():
            array = line.split(',')
            first_item = array[0]

        num_columns = len(array)
        csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=',')
        ttime = [0]
        free = [1]
        used = [2]

        x = []
        y1 = []
        y2 = []

        # print x
        # print y1
        # print y2

        count = 0
        t = 0
        for row in reader:
            if count == 0:
                count += 1
            else:

                content = list(row[i] for i in free)
                print content
                y1.append(int(content[0].strip()))

                content = list(row[i] for i in used)
                y2.append(int(content[0].strip()))

                # content = list(row[i] for i in buff)
                # y3.append(content[0].strip())

                content = list(row[i] for i in ttime)
                try:
                    # x.append(datetime.strptime(content[0].split(' ')[1].strip(), "%H:%M:%S"))
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        # print y2

        y_format = tkr.FuncFormatter(func)

        fig = plt.figure()  # the first figure
        fig.set_size_inches(17, 8)
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.3)
        ax = plt.subplot(1, 1, 1)
        # ax.plot(x, y1)
        # ax.plot(x, y2)
        ax.yaxis.set_major_formatter(y_format)
        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax.set_xlim(auto=True)
        ax.xaxis.set_major_formatter(myFmt)

        l1 = ax.plot(x, y1)
        l2 = ax.plot(x, y2)



        # tt1 = plugins.PointLabelTooltip(l1[0], labels=ttvalues1)
        # tt2 = plugins.PointLabelTooltip(l2[0], labels=ttvalues2)
        ax.set_title('%s: %s ' % (host, proc))
        plt.ylabel('Memory (Bytes)')
        fig.autofmt_xdate()

        labels1 = ["Free", "Used"]
        line_collections1 = [l1, l2]
        plugins.connect(fig, plugins.InteractiveLegendPlugin(line_collections1, labels1))


        mpld3.save_html(fig, "results/memory/%s_%s_%s.html" % (host, proc, tstamp))

        plt.close()

for host in CONFIG.graphhost:

    plot_topstats(file='results/memory/%s-httpd.csv' % host, proc='JavaMem')

