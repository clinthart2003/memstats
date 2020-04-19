import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from config import CONFIG

def plot_topstats(file='TQ_Setup/results/memory/clint-test-load average.csv', proc='Averge Load'):

    array = []

    with open(file, 'r') as csvfile:

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
                y1.append(content[0].strip())
                content = list(row[i] for i in included_col2)
                y2.append(content[0].strip())
                content = list(row[i] for i in included_col3)
                y3.append(content[0].strip())
                content = list(row[i] for i in included_col0)
                try:
                    x.append(datetime.strptime(content[0].strip(), "%m-%d-%Y %H:%M:%S"))
                except Exception as e:
                    x.append(datetime.strptime(content[0].strip(), "%Y-%m-%d %H:%M:%S"))

        fig, ax = plt.subplots()
        ax.plot(x, y1, label="1 Minute")
        ax.plot(x, y2, label="5 Minute")
        ax.plot(x, y3, label="5 Minute")

        labels = ["1 Minute", "5 Minute", "15 Minute"]

        myFmt = mdates.DateFormatter('%m-%d-%Y %H:%M:%S')
        ax.xaxis.set_major_formatter(myFmt)

        ax.legend(fancybox=True)
        plt.subplots_adjust(right=.8)

        plt.title('Average CPU Load')
        plt.ylabel('CPU (%)')
        plt.xticks(rotation=45)

        fig.set_size_inches(15, 9)
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.3)

        # print label and save here to avoid double labels in html
        plt.legend(labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.1)
        plt.savefig("results/memory/%s_%s.svg" % (CONFIG.graphhost, proc), bbox_inches="tight", format="svg")
        plt.savefig("results/memory/%s_%s.png" % (CONFIG.graphhost, proc), bbox_inches="tight", format="png")

        plt.close()


# plot_topstats(file='results/memory/clint-test-load average.csv', proc='Averge Load')


csvfiles = [
            ['results/memory/%s-load average.csv' % CONFIG.graphhost, 'Average Load']
            ]

for process in csvfiles:

    try:
        plot_topstats(file=process[0], proc=process[1])
    except Exception as e:
        print ("There was an error generating: %s " % process[0])

