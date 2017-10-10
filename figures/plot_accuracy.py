#! /usr/bin/env python3
from matplotlib import rcParams
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# settings
sns.set_style("ticks")
rcParams['font.family'] = 'serif'
pal = {'max':'#0000FF', 'maxsubtree':'#FF0000', 'avgsubtree':'#00FF00'}
handles = [Patch(color=pal['max'],label='Max'), Patch(color=pal['maxsubtree'],label='Max (Subtree)'), Patch(color=pal['avgsubtree'],label='Average (Subtree)')]

# moving average
def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

# read data from CSV file with columns: Rep, TP, TN, FP, FN, Precision, Recall
def read_data(f):
    data = {}
    for line in open(f).read().strip().splitlines()[1:]:
        parts = line.split(',')
        if parts[0] not in data:
            data[parts[0]] = {'Precision':[],'Recall':[]}
        data[parts[0]]['Precision'].append(float(parts[-2]))
        data[parts[0]]['Recall'].append(float(parts[-1]))
    for rep in data:
        data[rep]['Recall'],data[rep]['Precision'] = zip(*sorted(zip(data[rep]['Recall'], data[rep]['Precision'])))
    return data

# read data
data_max = read_data('accuracy.8.clusters.max.csv')
data_maxsubtree = read_data('accuracy.8.clusters.maxsubtree.csv')
data_avgsubtree = read_data('accuracy.8.clusters.avgsubtree.csv')

# plot
fig = plt.figure()
axes = plt.gca()
axes.set_xlim([0,1])
axes.set_ylim([0,1])
x = []; y = []
for rep in data_max:
    x += data_max[rep]['Recall']
    y += data_max[rep]['Precision']
x,y = zip(*sorted(zip(x,y)))
y_avg = movingaverage(y, 50)
plt.plot(x,y_avg,color=pal['max'])
x = []; y = []
for rep in data_maxsubtree:
    x += data_maxsubtree[rep]['Recall']
    y += data_maxsubtree[rep]['Precision']
x,y = zip(*sorted(zip(x,y)))
y_avg = movingaverage(y, 50)
plt.plot(x,y_avg,color=pal['maxsubtree'])
x = []; y = []
for rep in data_avgsubtree:
    x += data_avgsubtree[rep]['Recall']
    y += data_avgsubtree[rep]['Precision']
x,y = zip(*sorted(zip(x,y)))
y_avg = movingaverage(y, 50)
plt.plot(x,y_avg,color=pal['avgsubtree'])
legend = plt.legend(handles=handles,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., frameon=True)
sns.plt.xlabel('Recall')
sns.plt.ylabel('Precision')
sns.plt.title('Precision vs. Recall (8 Clusters)')
sns.plt.show()
fig.savefig('precision_vs_recall.pdf', format='pdf', bbox_extra_artists=(legend,), bbox_inches='tight')
plt.close()