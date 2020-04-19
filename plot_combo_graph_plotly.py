import csv
import plotly.graph_objects as go
import plotly
from datetime import datetime
from config import CONFIG
import locale
locale.setlocale(locale.LC_ALL, '')

tstamp = datetime.now().strftime("%Y-%m-%d")

x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
x4 = []
y4 = []
x5 = []
y5 = []

def func(x, pos):  # format function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))


def plot_combo(csvfiles, host):

    array = []

    file_number = 1
    for file in (csvfiles):
        x = []
        y = []
        with open(file[0], 'r') as csvfile:

            for line in csvfile.readlines():
                # get number of columns
                array = line.split(',')
                first_item = array[0]

            # num_columns = len(array)
            csvfile.seek(0)

            reader = csv.reader(csvfile, delimiter=',')
            ttime = [0]
            res = [6]

            count = 0
            for row in reader:
                if count == 0:
                    count += 1
                else:
                    content = list(row[i] for i in res)
                    y.append(float(content[0].strip())/1000/1000)

                    content = list(row[i] for i in ttime)
                    try:
                        x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                    except Exception as e:
                        x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        csvfile.close()
        if file_number == 5:
            y5 = y
            file_number += 1
        elif file_number == 4:
            y4 = y
            file_number += 1
        elif file_number == 3:
            y3 = y
            file_number += 1
        elif file_number == 2:
            y2 = y
            file_number += 1
        else:
            y1 = y
            file_number += 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Solr'))
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='MySQL'))
    fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name='Journald'))
    fig.add_trace(go.Scatter(x=x, y=y4, mode='lines', name='Dynamo'))
    fig.add_trace(go.Scatter(x=x, y=y5, mode='lines', name='tqcontroller'))

    fig.update_yaxes(title_text="Usage in GiB")
    fig.update_layout(
        title_text='%s: Process Memory Usage (GiB)' % (host),
        font=dict(
            family="Courier New, monospace",
            size=15,
            color="#7f7f7f"),
        height=700,
        width=1200
    )

    plotly.offline.plot(fig, filename="results/memory/%s_%s_%s.html" % (host, "proc-mem", tstamp), auto_open=False)

for host in CONFIG.graphhost:

    csvfiles = [['results/memory/%s-mysqld.csv' % host, 'mysqld'],
                ['results/memory/%s-solr.csv' % host, 'solr'],
                ['results/memory/%s-systemd-journald.csv' % host, 'systemd-journald'],
                ['results/memory/%s-dynamo.csv' % host, 'dynamo'],
                ['results/memory/%s-tqcontroller.csv' % host, 'tqcontroller']
                ]

    plot_combo(csvfiles, host)
