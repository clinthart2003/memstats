import csv
import matplotlib.pyplot as plt, mpld3
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
from mpld3 import plugins
from datetime import datetime
from config import CONFIG
import locale
locale.setlocale(locale.LC_ALL, '')
import sys, os
import logging
script = os.path.basename(sys.argv[0])
logging.basicConfig(filename='./files/test_logs/%s.log' % script, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger('test')


tstamp = datetime.now().strftime("%Y-%m-%d")

def plot_topstats(infile='TQ_Setup/results/memory/clint-test-load average.csv', proc='Averge Load'):

    array = []

    with open(infile, 'r') as csvfile:

        # get number of columns
        for line in csvfile.readlines():
            array = line.split(',')
            first_item = array[0]

        num_columns = len(array)
        csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=',')
        included_col0 = [0]
        included_col1 = [1]
        included_col2 = [2]
        included_col3 = [3]
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
                content = list(row[i] for i in included_col1)
                y1.append((float(content[0].strip())))
                content = list(row[i] for i in included_col2)
                y2.append((float(content[0].strip())))
                content = list(row[i] for i in included_col3)
                y3.append((float(content[0].strip())))
                content = list(row[i] for i in included_col0)
                # print content[0].strip()
                try:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))
                except Exception as e:
                    print ('Error with line: %d' % (count + 1))
                count += 1


        fig, ax = plt.subplots(1)  # the first figure
        fig.set_size_inches(15, 8)
        # ax = plt.subplot()

        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax.xaxis.set_major_formatter(myFmt)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        # print y1
        l1 = ax.plot(x, y1, marker='.')
        tt1 = plugins.PointLabelTooltip(l1[0], labels=y1)

        l2 = ax.plot(x, y2, marker='.')
        tt2 = plugins.PointLabelTooltip(l2[0], labels=y2)

        l3 = ax.plot(x, y3, marker='.')
        tt3 = plugins.PointLabelTooltip(l3[0], labels=y3)

        labels = ["1 Min", "5 Min", "15 Min"]

        line_collections = [l1, l2, l3]
        plugins.connect(fig, plugins.InteractiveLegendPlugin(line_collections, labels), tt1, tt2, tt3)

        plt.title('%s: Average CPU Load' % host)
        plt.ylabel('CPU (%)')
        plt.xticks(rotation=45)

        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.3)

        mpld3.save_html(fig, "results/memory/%s_%s_%s.html" % (host, proc, tstamp))

        plt.close()

for host in CONFIG.graphhost:

    plot_topstats(infile='results/memory/%s-load average.csv' % host, proc='Average Load')

"""
csvfiles = [
            ['results/memory/%s-load average.csv' % CONFIG.graphhost, proc='Average Load']
            ]

for process in csvfiles:

    try:
        plot_topstats(file=process[0], proc=process[1])
    except Exception as e:
        print ("There was an error generating: %s " % process[0])
"""
