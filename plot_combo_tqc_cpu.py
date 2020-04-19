import csv
import matplotlib.pyplot as plt
import mpld3
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


def plot_combo(csvfiles, host):

    x1 = []
    y1 = []
    x2 = []
    y2 = []
    x3 = []
    y3 = []
    x4 = []
    y4 = []

    array = []

    file_number = 1
    for file in (csvfiles):
        x = []
        y = []
        with open(file[0], 'r') as csvfile:

            if file_number == 1:
                for line in csvfile.readlines():
                    # get number of columns
                    array = line.split(',')
                    first_item = array[0]

                # num_columns = len(array)
                csvfile.seek(0)

                reader = csv.reader(csvfile, delimiter=',')
                ttime = [0]
                cpu = [1]


                count = 0
                for row in reader:
                    if count == 0:
                        count += 1
                    else:
                        content = list(row[i] for i in cpu)
                        y.append(float(content[0].strip()))

                        content = list(row[i] for i in ttime)
                        try:
                            x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                        except Exception as e:
                            x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))
            else:

                for line in csvfile.readlines():
                    # get number of columns
                    array = line.split(',')
                    first_item = array[0]

                # num_columns = len(array)
                csvfile.seek(0)

                reader = csv.reader(csvfile, delimiter=',')
                ttime = [0]
                cpu = [9]

                count = 0
                for row in reader:
                    if count == 0:
                        count += 1
                    else:
                        content = list(row[i] for i in cpu)
                        y.append(float(content[0].strip()))

                        content = list(row[i] for i in ttime)
                        try:
                            x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                        except Exception as e:
                            x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        if file_number == 4:
            y4 = y
            x4 = x
            # print file_number
        elif file_number == 3:
            y3 = y
            x3 = x
            # print file_number
            file_number += 1
        elif file_number == 2:
            y2 = y
            x2 = x
            # print file_number
            file_number += 1
        else:
            y1 = y
            x1 = x
            # print file_number
            file_number += 1

    y_format = tkr.FuncFormatter(func)

    fig = plt.figure()  # the first figure
    ax = fig.add_subplot(1, 1, 1)
    l1 = ax.plot(x1, y1, marker='.')
    l2 = ax.plot(x2, y2, marker='.')
    l3 = ax.plot(x3, y3, marker='.')
    l4 = ax.plot(x4, y4, marker='.')
    ax.yaxis.set_major_formatter(y_format)
    myfmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
    ax.xaxis.set_major_formatter(myfmt)


    # format tootip values
    ttvalues1 = []
    ttvalues2 = []
    ttvalues3 = []
    ttvalues4 = []

    for i, s in enumerate(y1):
        ttvalues1.append(format(int(s), ','))
    for i, s in enumerate(y2):
        ttvalues2.append(format(int(s), ','))
    for i, s in enumerate(y3):
        ttvalues3.append(format(int(s), ','))
    for i, s in enumerate(y4):
        ttvalues4.append(format(int(s), ','))

    tt1 = plugins.PointLabelTooltip(l1[0], labels=ttvalues1)
    tt2 = plugins.PointLabelTooltip(l2[0], labels=ttvalues2)
    tt3 = plugins.PointLabelTooltip(l3[0], labels=ttvalues3)
    tt4 = plugins.PointLabelTooltip(l4[0], labels=ttvalues4)

    ax.set_title('%s: %s ' % (host, "CPU Utilization Compare"))
    plt.ylabel('% Utilized')
    fig.set_size_inches(20, 7)
    plt.xticks(rotation=45)


    labels1 = ["Avg CPU", "TQController", "TQ-Supervisord", "Dynamo"]
    line_collections1 = [l1, l2, l3, l4]
    plugins.connect(fig, plugins.InteractiveLegendPlugin(line_collections1, labels1, ax=ax), tt1, tt2, tt3, tt4)

    mpld3.save_html(fig, "results/memory/%s_%s_%s.html" % (host, "proc-cpu", tstamp))

    plt.close()

for host in CONFIG.graphhost:

    csvfiles = [['results/memory/%s-load average.csv' % host, 'Average Load'],
                ['results/memory/%s-tqcontroller.csv' % host, 'tqcontroller'],
                ['results/memory/%s-tq-supervisord.csv' % host, 'tq-supervisor'],
                ['results/memory/%s-dynamo.csv' % host, 'dynamo']
                ]
    plot_combo(csvfiles, host)
