import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from matplotlib.ticker import FixedFormatter, FixedLocator
import json


# results["data"] = (xss, values)
def get_delivery_ratio(INPUT_PATH, scenarios, xs, repetitions, TTR):
    results = {}

    for scenario in scenarios:

        xss = []
        values = []

        for x in xs:
            for rep in repetitions:
                input_path = INPUT_PATH + scenario + "General-TTF=%sh,TTR=%sh-#%d.sca" % (str(x), str(TTR), rep)
                print(input_path)

                xss.append(x)

                conn = sqlite3.connect(input_path)
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()

                cur.execute("SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='%s'"%("appBundleSent:count"))
                rows1 = cur.fetchall()
                tx_packets = 0 if (rows1[0]["result"] == None) else rows1[0]["result"]

                cur.execute("SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='%s'"%("appBundleReceived:count"))
                rows1 = cur.fetchall()
                rx_packets = 0 if (rows1[0]["result"] == None) else rows1[0]["result"]

                delivery_ratio = float(rx_packets) / float(tx_packets) * 100
                values.append(delivery_ratio)

        results[scenario] = (xss, values)
    return results

# results["data"] = (xss, values)
def get_delivery_delay(INPUT_PATH, scenarios, xs, repetitions, TTR):
    results = {}

    for scenario in scenarios:

        xss = []
        values = []

        for x in xs:
            for rep in repetitions:
                input_path = INPUT_PATH + scenario + "General-TTF=%sh,TTR=%sh-#%d.sca" % (str(x), str(TTR), rep)
                print(input_path)

                xss.append(x)

                conn = sqlite3.connect(input_path)
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()

                query = "SELECT AVG(scalarValue) AS result FROM scalar WHERE scalarName='%s'" % "appBundleReceivedDelay:mean"
                cur.execute(query)
                rows1 = cur.fetchall()
                mean_delay = 0 if (rows1[0]["result"] == None) else rows1[0]["result"] / 3600
                values.append(mean_delay)

        results[scenario] = (xss, values)
    return results

# results["data"] = (xss, avg_values, max_values)
def get_buffer_occupancy(INPUT_PATH, scenarios, xs, repetitions, node):
    results = {}

    for scenario in scenarios:

        xss = []
        values_avg = []
        values_max = []

        for x in xs:
            for rep in repetitions:
                input_path = INPUT_PATH + scenario + "General-TTF=%sh-#%d.sca" % (str(x), rep)
                print(input_path)

                xss.append(x)

                conn = sqlite3.connect(input_path)
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                
                query_total_packets = "SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='%s'" % "appBundleSent:count"
                cur.execute(query_total_packets)
                rows0 = cur.fetchall()
                value_total_packets = 0 if (rows0[0]["result"] == None) else rows0[0]["result"]
                
                query_avg = "SELECT AVG(scalarValue) AS result FROM scalar WHERE scalarName='%s'" % "sdrBundleStored:timeavg"
                query_avg += " AND moduleName='dtnsim.node[%s].dtn'" % node
                cur.execute(query_avg)
                rows1 = cur.fetchall()
                value_avg = 0 if (rows1[0]["result"] == None) else rows1[0]["result"]
                values_avg.append(value_avg/value_total_packets * 100)

                query_max = "SELECT AVG(scalarValue) AS result FROM scalar WHERE scalarName='%s'" % "sdrBundleStored:max"
                query_max += " AND moduleName='dtnsim.node[%s].dtn'" % node
                cur.execute(query_max)
                rows2 = cur.fetchall()
                value_max = 0 if (rows2[0]["result"] == None) else rows2[0]["result"]
                values_max.append(value_max/value_total_packets * 100)

        results[scenario] = (xss, values_avg, values_max)
    return results

INPUT_PATH = os.getcwd() + "/"

scenarios = [
'../1LEO_1GS/results/',
'../1LEO_2GS/results/',
'../1LEO_5GS/results/',
'../1LEO_10GS/results/',
'../1LEO_1HAP_1GS/results/',
'../1LEO_2HAP_2GS/results/',
'../1LEO_3HAP_3GS/results/',
'../1LEO_4HAP_4GS/results/',
'../1LEO_5HAP_5GS/results/',
]

l0 = '1LEO-1GS'
l1 = '1LEO-2GS'
l2 = '1LEO-5GS'
l3 = '1LEO-10GS'
l4 = '1LEO-1HAGS-1GS'
l5 = '1LEO-2HAGS-2GS'
l6 = '1LEO-3HAGS-3GS'
l7 = '1LEO-4HAGS-4GS'
l8 = '1LEO-5HAGS-5GS'

m0 = "s"
m1 = "o"
m2 = "v"
m3 = "D"
m4 = "p"
m5 = "p"
m6 = "p"

mar0 = 7
mar1 = 7
mar2 = 7
mar3 = 7
mar4 = 9
mar5 = 9
mar6 = 9

TTF = [0.1,0.2,0.5,1,2,5,10,15,20,25,30,35,40]
TTR = 15

#TTF = list(range(100,1100,100))
repetitions = list(range(0,100))
results1 = get_delivery_ratio(INPUT_PATH, scenarios, TTF, repetitions, TTR)
results2 = get_delivery_delay(INPUT_PATH, scenarios, TTF, repetitions, TTR)
#results3 = get_buffer_occupancy(INPUT_PATH, ['../1LEO_1HAP_1GS/results/'], TTF, repetitions, "11")

WIDTH = 10
HEIGHT = 8
LINEWIDTH = 0.4

import seaborn as sns
clr = sns.color_palette(None, 9)
clr[3], clr[4] = clr[4], clr[3]
clr[1], clr[2] = clr[2], clr[1]
clr[0], clr[1] = clr[1], clr[0]

count_0 = len([value for value in results1[scenarios[0]][0] if value < 20])
count_1 = len([value for value in results1[scenarios[1]][0] if value < 10])
count_2 = len([value for value in results1[scenarios[2]][0] if value < 2])
count_3 = len([value for value in results1[scenarios[3]][0] if value < 0.5])
count_4 = len([value for value in results1[scenarios[4]][0] if value < 0.5])
count_5 = len([value for value in results1[scenarios[5]][0] if value < 0.2])
count_6 = len([value for value in results1[scenarios[6]][0] if value < 0.1])
count_7 = len([value for value in results1[scenarios[7]][0] if value < 0.1])
count_8 = len([value for value in results1[scenarios[8]][0] if value < 0.1])


fig, ax = plt.subplots(figsize=(WIDTH,HEIGHT))
sns.lineplot(x=results1[scenarios[0]][0], y=results1[scenarios[0]][1], color=clr[0], marker=m0, label=l0, markersize=mar0, markeredgecolor="none", ax=ax)
sns.lineplot(x=results1[scenarios[1]][0], y=results1[scenarios[1]][1], color=clr[1], marker=m0, label=l1, markersize=mar0, markeredgecolor="none", ax=ax)
sns.lineplot(x=results1[scenarios[2]][0], y=results1[scenarios[2]][1], color=clr[2], marker=m0, label=l2, markersize=mar0, markeredgecolor="none", ax=ax)
sns.lineplot(x=results1[scenarios[3]][0], y=results1[scenarios[3]][1], color=clr[3], marker=m0, label=l3, markersize=mar0, markeredgecolor="none", ax=ax)
sns.lineplot(x=results1[scenarios[4]][0], y=results1[scenarios[4]][1], color=clr[4], marker=m1, label=l4, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results1[scenarios[5]][0], y=results1[scenarios[5]][1], color=clr[5], marker=m1, label=l5, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results1[scenarios[6]][0], y=results1[scenarios[6]][1], color=clr[6], marker=m1, label=l6, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results1[scenarios[7]][0], y=results1[scenarios[7]][1], color=clr[7], marker=m1, label=l7, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results1[scenarios[8]][0], y=results1[scenarios[8]][1], color=clr[8], marker=m1, label=l8, markersize=mar1, markeredgecolor="none", ax=ax)
ax.set_xlabel("TTF [hours]", fontsize=13)
ax.set_ylabel("Delivery ratio [% of packets generated]", fontsize=13)
plt.tight_layout()
plt.grid(linewidth=LINEWIDTH, zorder=0)
ax.legend(loc='lower right', prop={'size': 10})
plt.xscale('log')
plt.xticks(TTF, [str(val) for val in TTF])
plt.savefig("delivery_ratio_TTR=%s.png" % str(TTR))
plt.cla()
plt.clf()

fig, ax = plt.subplots(figsize=(WIDTH,HEIGHT))

cte = len(repetitions)
grey_color = "#CCCCCC"

sns.lineplot(x=results2[scenarios[0]][0][:count_0+cte], y=results2[scenarios[0]][1][:count_0+cte], color=grey_color, marker=m0, markersize=mar0, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[0]][0][count_0:], y=results2[scenarios[0]][1][count_0:], color=clr[0], marker=m0, label=l0, markersize=mar0, markeredgecolor="none", ax=ax)

sns.lineplot(x=results2[scenarios[1]][0][:count_1+cte], y=results2[scenarios[1]][1][:count_1+cte], color=grey_color, marker=m0, markersize=mar0, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[1]][0][count_1:], y=results2[scenarios[1]][1][count_1:], color=clr[1], marker=m0, label=l1, markersize=mar0, markeredgecolor="none", ax=ax)

sns.lineplot(x=results2[scenarios[2]][0][:count_2+cte], y=results2[scenarios[2]][1][:count_2+cte], color=grey_color, marker=m0, markersize=mar0, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[2]][0][count_2:], y=results2[scenarios[2]][1][count_2:], color=clr[2], marker=m0, label=l2, markersize=mar0, markeredgecolor="none", ax=ax)

sns.lineplot(x=results2[scenarios[3]][0][:count_3+cte], y=results2[scenarios[3]][1][:count_3+cte], color=grey_color, marker=m0, markersize=mar0, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[3]][0][count_3:], y=results2[scenarios[3]][1][count_3:], color=clr[3], marker=m0, label=l3, markersize=mar0, markeredgecolor="none", ax=ax)

sns.lineplot(x=results2[scenarios[4]][0][:count_4+cte], y=results2[scenarios[4]][1][:count_4+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[4]][0][count_4:], y=results2[scenarios[4]][1][count_4:], color=clr[4], marker=m1, label=l4, markersize=mar1, markeredgecolor="none", ax=ax)

sns.lineplot(x=results2[scenarios[5]][0][:count_5+cte], y=results2[scenarios[5]][1][:count_5+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[5]][0][count_5:], y=results2[scenarios[5]][1][count_5:], color=clr[5], marker=m1, label=l5, markersize=mar1, markeredgecolor="none", ax=ax)

sns.lineplot(x=results2[scenarios[6]][0][:count_6+cte], y=results2[scenarios[6]][1][:count_6+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[6]][0][count_6:], y=results2[scenarios[6]][1][count_6:], color=clr[6], marker=m1, label=l6, markersize=mar1, markeredgecolor="none", ax=ax)

sns.lineplot(x=results2[scenarios[7]][0][:count_7+cte], y=results2[scenarios[7]][1][:count_7+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[7]][0][count_7:], y=results2[scenarios[7]][1][count_7:], color=clr[7], marker=m1, label=l7, markersize=mar1, markeredgecolor="none", ax=ax)

sns.lineplot(x=results2[scenarios[8]][0][:count_8+cte], y=results2[scenarios[8]][1][:count_8+cte], color=grey_color, marker=m1, markersize=mar1, markeredgecolor="none", ax=ax)
sns.lineplot(x=results2[scenarios[8]][0][count_8:], y=results2[scenarios[8]][1][count_8:], color=clr[8], marker=m1, label=l8, markersize=mar1, markeredgecolor="none", ax=ax)

ax.set_xlabel("TTF [hours]", fontsize=13)
ax.set_ylabel("Mean Delivery Delay [hours]", fontsize=13)
plt.tight_layout()
plt.grid(linewidth=LINEWIDTH, zorder=0)
ax.legend(loc='upper right',  prop={'size': 10})
plt.xscale('log')
plt.xticks(TTF, [str(val) for val in TTF])
plt.ylim(0,100)
plt.savefig("delivery_delay_TTR=%s.png" % str(TTR))
plt.cla()
plt.clf()

# fig, ax = plt.subplots(figsize=(WIDTH,HEIGHT))
# sns.lineplot(x=results3[scenarios[4]][0], y=results3[scenarios[4]][2], color=clr[4], marker=m4, label="max", markersize=mar4, markeredgecolor="none", ax=ax)
# sns.lineplot(x=results3[scenarios[4]][0], y=results3[scenarios[4]][1], color=clr[4], marker=m4, linestyle='--', label="mean", markersize=mar4, markeredgecolor="none", ax=ax)
# ax.set_xlabel("TTF [hours]", fontsize=13)
# ax.set_ylabel("Buffer Occupancy [% of packets generated]", fontsize=13)
# plt.tight_layout()
# plt.grid(linewidth=LINEWIDTH, zorder=0)
# ax.legend(loc='upper right', prop={'size': 10})
# plt.savefig("buffer_occupancy.png")
# plt.cla()
# plt.clf()

data = {
    "ttf_values": results1[scenarios[0]][0],
    "delivery_ratio": {
    '1LEO-1GS': results1[scenarios[0]][1],
    '1LEO-2GS': results1[scenarios[1]][1],
    '1LEO-5GS': results1[scenarios[2]][1],
    '1LEO-10GS': results1[scenarios[3]][1],
    '1LEO-1HAGS-1GS': results1[scenarios[4]][1],
    '1LEO-2HAGS-2GS': results1[scenarios[5]][1],
    '1LEO-3HAGS-3GS': results1[scenarios[6]][1],
    '1LEO-4HAGS-4GS': results1[scenarios[7]][1],
    '1LEO-5HAGS-5GS': results1[scenarios[8]][1],
    },
    "delivery_delay": {
        '1LEO-1GS': results2[scenarios[0]][1],
        '1LEO-2GS': results2[scenarios[1]][1],
        '1LEO-5GS': results2[scenarios[2]][1],
        '1LEO-10GS': results2[scenarios[3]][1],
        '1LEO-1HAGS-1GS': results2[scenarios[4]][1],
        '1LEO-2HAGS-2GS': results2[scenarios[5]][1],
        '1LEO-3HAGS-3GS': results2[scenarios[6]][1],
        '1LEO-4HAGS-4GS': results2[scenarios[7]][1],
        '1LEO-5HAGS-5GS': results2[scenarios[8]][1],
    }
}

with open('results_TTR=15.json', 'w') as json_file:
    json.dump(data, json_file)

print("end")


