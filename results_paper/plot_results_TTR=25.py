import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from matplotlib.ticker import FixedFormatter, FixedLocator
import json

with open('results_TTR=25.json', 'r') as json_file:
    data = json.load(json_file)

l0 = '1LEO-1GS'
l1 = '1LEO-2GS'
l2 = '1LEO-5GS'
l3 = '1LEO-10GS'
l4 = '1LEO-1HAGS-1GS'
l5 = '1LEO-2HAGS-2GS'
l6 = '1LEO-3HAGS-3GS'
l7 = '1LEO-4HAGS-4GS'
l8 = '1LEO-5HAGS-5GS'

ttf_values = data['ttf_values']
results1 = []
results1.append(data['delivery_ratio'][l0])
results1.append(data['delivery_ratio'][l1])
results1.append(data['delivery_ratio'][l2])
results1.append(data['delivery_ratio'][l3])
results1.append(data['delivery_ratio'][l4])
results1.append(data['delivery_ratio'][l5])
results1.append(data['delivery_ratio'][l6])
results1.append(data['delivery_ratio'][l7])
results1.append(data['delivery_ratio'][l8])
results2 = []
results2.append(data['delivery_delay'][l0])
results2.append(data['delivery_delay'][l1])
results2.append(data['delivery_delay'][l2])
results2.append(data['delivery_delay'][l3])
results2.append(data['delivery_delay'][l4])
results2.append(data['delivery_delay'][l5])
results2.append(data['delivery_delay'][l6])
results2.append(data['delivery_delay'][l7])
results2.append(data['delivery_delay'][l8])

m0 = "s"
m1 = "o"

mar0 = 7
mar1 = 7

medgewidth = 2

TTF = [0.1,0.2,0.5,1,2,5,10,15,20,25,30,35,40]
TTR = 25

repetitions = list(range(0,100))

WIDTH = 8
HEIGHT = 5
LINEWIDTH = 0.4

import seaborn as sns
num_dark_colors = 10
num_light_colors = 5
# Generate lighter/luminous color palette
light_palette = sns.color_palette("bright", n_colors=num_light_colors)
# Generate darker color palette
dc = sns.color_palette("dark", n_colors=num_dark_colors)
dark_palette = [dc[0], dc[1], dc[2], dc[4]]
# Combine the two palettes
clr = dark_palette + light_palette

count_0 = len([value for value in ttf_values if value < 30])
count_1 = len([value for value in ttf_values if value < 10])
count_2 = len([value for value in ttf_values if value < 2])
count_3 = len([value for value in ttf_values if value < 1])
count_4 = len([value for value in ttf_values if value < 0.5])
count_5 = len([value for value in ttf_values if value < 0.5])
count_6 = len([value for value in ttf_values if value < 0.5])
count_7 = len([value for value in ttf_values if value < 0.5])
count_8 = len([value for value in ttf_values if value < 0.5])

fig, ax = plt.subplots(figsize=(WIDTH,HEIGHT))
sns.lineplot(x=ttf_values, y=results1[0], color=clr[0], marker=m0, label=l0, markersize=mar0, markeredgecolor=clr[0], markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)
sns.lineplot(x=ttf_values, y=results1[1], color=clr[1], marker=m0, label=l1, markersize=mar0, markeredgecolor=clr[1], markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)
sns.lineplot(x=ttf_values, y=results1[2], color=clr[2], marker=m0, label=l2, markersize=mar0, markeredgecolor=clr[2], markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)
sns.lineplot(x=ttf_values, y=results1[3], color=clr[3], marker=m0, label=l3, markersize=mar0, markeredgecolor=clr[3], markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)
sns.lineplot(x=ttf_values, y=results1[4], color=clr[4], marker=m1, label=l4, markersize=mar1, markeredgecolor=clr[4], ax=ax)
sns.lineplot(x=ttf_values, y=results1[5], color=clr[5], marker=m1, label=l5, markersize=mar1, markeredgecolor=clr[5], ax=ax)
sns.lineplot(x=ttf_values, y=results1[6], color=clr[6], marker=m1, label=l6, markersize=mar1, markeredgecolor=clr[6], ax=ax)
sns.lineplot(x=ttf_values, y=results1[7], color=clr[7], marker=m1, label=l7, markersize=mar1, markeredgecolor=clr[7], ax=ax)
sns.lineplot(x=ttf_values, y=results1[8], color=clr[8], marker=m1, label=l8, markersize=mar1, markeredgecolor=clr[8], ax=ax)
ax.set_xlabel("TCC [hours]", fontsize=13)
ax.set_ylabel("Delivery ratio [% of files generated]", fontsize=13)
plt.tight_layout()
plt.grid(linewidth=LINEWIDTH, zorder=0)
ax.legend(loc='lower right', prop={'size': 10})
plt.xscale('log')
plt.xticks(TTF, [str(val) for val in TTF])
plt.savefig("delivery_ratio_TCS=%s.pdf" % str(TTR))
plt.cla()
plt.clf()

fig, ax = plt.subplots(figsize=(WIDTH,HEIGHT))

cte = len(repetitions)
grey_color = "#CCCCCC"

sns.lineplot(x=ttf_values[:count_0+cte], y=results2[0][:count_0+cte], color=grey_color, marker=m0, markersize=mar0, markeredgecolor=grey_color, markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)
sns.lineplot(x=ttf_values[count_0:], y=results2[0][count_0:], color=clr[0], marker=m0, label=l0, markersize=mar0, markeredgecolor=clr[0], markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)

sns.lineplot(x=ttf_values[:count_1+cte], y=results2[1][:count_1+cte], color=grey_color, marker=m0, markersize=mar0, markeredgecolor=grey_color, markerfacecolor='none', ax=ax)
sns.lineplot(x=ttf_values[count_1:], y=results2[1][count_1:], color=clr[1], marker=m0, label=l1, markersize=mar0, markeredgecolor=clr[1], markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)

sns.lineplot(x=ttf_values[:count_2+cte], y=results2[2][:count_2+cte], color=grey_color, marker=m0, markersize=mar0, markeredgecolor=grey_color, markerfacecolor='none', ax=ax)
sns.lineplot(x=ttf_values[count_2:], y=results2[2][count_2:], color=clr[2], marker=m0, label=l2, markersize=mar0, markeredgecolor=clr[2], markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)

sns.lineplot(x=ttf_values[:count_3+cte], y=results2[3][:count_3+cte], color=grey_color, marker=m0, markersize=mar0, markeredgecolor=grey_color, markerfacecolor='none', ax=ax)
sns.lineplot(x=ttf_values[count_3:], y=results2[3][count_3:], color=clr[3], marker=m0, label=l3, markersize=mar0, markeredgecolor=clr[3], markerfacecolor='none', markeredgewidth=medgewidth, ax=ax)

sns.lineplot(x=ttf_values[:count_4+cte], y=results2[4][:count_4+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor=grey_color, ax=ax)
sns.lineplot(x=ttf_values[count_4:], y=results2[4][count_4:], color=clr[4], marker=m1, label=l4, markersize=mar1, markeredgecolor=clr[4], ax=ax)

sns.lineplot(x=ttf_values[:count_5+cte], y=results2[5][:count_5+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor=grey_color, ax=ax)
sns.lineplot(x=ttf_values[count_5:], y=results2[5][count_5:], color=clr[5], marker=m1, label=l5, markersize=mar1, markeredgecolor=clr[5], ax=ax)

sns.lineplot(x=ttf_values[:count_6+cte], y=results2[6][:count_6+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor=grey_color, ax=ax)
sns.lineplot(x=ttf_values[count_6:], y=results2[6][count_6:], color=clr[6], marker=m1, label=l6, markersize=mar1, markeredgecolor=clr[6], ax=ax)

sns.lineplot(x=ttf_values[:count_7+cte], y=results2[7][:count_7+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor=grey_color, ax=ax)
sns.lineplot(x=ttf_values[count_7:], y=results2[7][count_7:], color=clr[7], marker=m1, label=l7, markersize=mar1, markeredgecolor=clr[7], ax=ax)

sns.lineplot(x=ttf_values[:count_8+cte], y=results2[8][:count_8+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor=grey_color, ax=ax)
sns.lineplot(x=ttf_values[count_8:], y=results2[8][count_8:], color=clr[8], marker=m1, label=l8, markersize=mar1, markeredgecolor=clr[8], ax=ax)

ax.set_xlabel("TCC [hours]", fontsize=13)
ax.set_ylabel("Delivery delay [hours]", fontsize=13)
plt.tight_layout()
plt.grid(linewidth=LINEWIDTH, zorder=0)
ax.legend(loc='upper right',  prop={'size': 10})
plt.xscale('log')
plt.xticks(TTF, [str(val) for val in TTF])
plt.ylim(0,100)
plt.savefig("delivery_delay_TCS=%s.pdf" % str(TTR))
plt.cla()
plt.clf()

print("end")


