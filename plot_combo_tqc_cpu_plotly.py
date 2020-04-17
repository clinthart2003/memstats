import csv
import plotly.graph_objects as go
import plotly
from datetime import datetime
from TQ_Setup.config import CONFIG
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

    # labels1 = ["Avg CPU", "TQController", "TQ-Supervisord", "Dynamo"]

    # print (y1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='1 Min Avg Load'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='TQController'))
    fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name='TQ-Supervisord'))
    fig.add_trace(go.Scatter(x=x, y=y4, mode='lines', name='Dynamo'))

    fig.update_yaxes(title_text="CPU Utilization %")
    fig.update_layout(
        title_text='%s: CPU Utilization Compare' % (host),
        font=dict(
            family="Courier New, monospace",
            size=15,
            color="#7f7f7f"),
        height=700,
        width=1200
    )

    plotly.offline.plot(fig, filename="results/memory/%s_%s_%s.html" % (host, "proc-cpu", tstamp), auto_open=False)

for host in CONFIG.graphhost:

    csvfiles = [['results/memory/%s-load average.csv' % host, 'Average Load'],
                ['results/memory/%s-tqcontroller.csv' % host, 'tqcontroller'],
                ['results/memory/%s-tq-supervisord.csv' % host, 'tq-supervisor'],
                ['results/memory/%s-dynamo.csv' % host, 'dynamo']
                ]
    plot_combo(csvfiles, host)
