import csv
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
                y1.append(float(content[0].strip())/1000)

                content = list(row[i] for i in wkb)
                y2.append(float(content[0].strip())/1000)

                content = list(row[i] for i in utilp)
                y3.append(float(content[0].strip()))

                content = list(row[i] for i in ttime)
                try:
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        # y_format = tkr.FuncFormatter(func)

        fig = make_subplots(rows=2, cols=1,
                            subplot_titles=("Disk Usage (MiB/sec", "Percent Disk Utilized"))
        fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Read'), row=1, col=1)
        fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Write'), row=1, col=1)
        fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name='% Used'), row=2, col=1)


        fig.update_yaxes(title_text="Read & Write MiB/sec", row=1, col=1)
        fig.update_yaxes(title_text="% CPU Used", row=2, col=1)

        fig.update_layout(
            title_text='%s: %s Disk Utilization (MiB/sec)' % (host, proc),
            font=dict(
                family="Courier New, monospace",
                size=15,
                color="#7f7f7f"),
            height=800,
            width=1000
        )

        # fig.show()
        plotly.offline.plot(fig, filename="results/memory/%s_%s_%s.html" % (host, proc, tstamp), auto_open=False)


for host in CONFIG.graphhost:
    plot_topstats(infile='results/memory/%s-iostat.csv' % host, proc='IOStat')
