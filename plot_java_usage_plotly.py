import csv
import plotly
import plotly.graph_objects as go
from datetime import datetime
from TQ_Setup.config import CONFIG

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
                y1.append(float(content[0].strip())/1000/1000/1000)

                content = list(row[i] for i in used)
                y2.append(float(content[0].strip())/1000/1000/1000)

                content = list(row[i] for i in ttime)
                try:
                    # x.append(datetime.strptime(content[0].split(' ')[1].strip(), "%H:%M:%S"))
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        # print y2

        # myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        # ax.xaxis.set_major_formatter(myFmt)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Free'))
        fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Used'))
        fig.update_yaxes(title_text="Java Memorty in GiB")
        fig.update_layout(
            title_text='%s: Java Memory (GiB)' % (host),
            font=dict(
                family="Courier New, monospace",
                size=15,
                color="#7f7f7f"),
            height=700,
            width=1200
                        )

        # fig.show()
        plotly.offline.plot(fig, filename="results/memory/%s_%s_%s.html" % (host, proc, tstamp), auto_open=False)


for host in CONFIG.graphhost:

    try:
        plot_topstats(file='results/memory/%s-JavaMem.csv' % host, proc='JavaMem')
    except Exception as e:
        # print ("Error generating graph for: %s " % host)
        print (e)

