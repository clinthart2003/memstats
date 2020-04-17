import csv
import plotly
import plotly.graph_objects as go
import matplotlib.dates as mdates
# import collections
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

        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='1 Min'))
        fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='5 Min'))
        fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name='15 Min'))
        fig.update_yaxes(title_text="Average % CPU")
        fig.update_layout(
            title_text='%s: Average CPU Usage' % host,
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

    plot_topstats(infile='results/memory/%s-load average.csv' % host, proc='Average Load')
