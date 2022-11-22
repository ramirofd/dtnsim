import matplotlib.pyplot as plt
import ast
import os

#OUTPUT
FILE_OUTPUT_PATH = os.getcwd() + "/results/meanDelayPerBundle.pdf"

#INPUT. Complete path will be computed as DIRECTORY/FILE_PATHS_C1[i]
DIRECTORY = os.getcwd() + "/.."
FILE_PATHS_C1 = [
"case0/results/METRIC=appBundleReceivedDelay:mean.txt",
"case1/results/METRIC=appBundleReceivedDelay:mean.txt",
"case2/results/METRIC=appBundleReceivedDelay:mean.txt",
]

#Calculate complete path
COMPLETE_PATHS_C1 = list(map(lambda x: DIRECTORY + "/" + x, FILE_PATHS_C1))

#Names of plotted functions

NAME_CURVAS_1 = ['Full' + ' Knowledge','Reduced' + ' Knowledge', 'Regionalized' + ' Knowledge']

#Color of ploted functions
COLOR_CURVAS_1 = ['black','blue','green']

#Style of plotted function
STYLE_CURVAS_1 = ['-v','-o','-s']

X_LABEL = "Bundles Sent"
Y_LABEL = "Mean Delay Per Bundle [s]"

def main():
    c1s = [getListFromFile(fname) for fname in COMPLETE_PATHS_C1]

    # plot results

    lines = []
    for c1,name1,color1,style1, in zip(c1s,NAME_CURVAS_1,COLOR_CURVAS_1,STYLE_CURVAS_1):
        line_up, = plt.plot([x[0] for x in c1],[y[1] for y in c1],style1, color=color1, label=name1,linewidth=1.0)
        lines.append(line_up)

    plt.legend(handles= lines)

    #plt.xlim([0,1700])
    #plt.ylim([0.4,1.05])
    plt.xlabel(X_LABEL, fontsize=16)
    plt.ylabel(Y_LABEL, fontsize=16)
    plt.grid(color='gray', linestyle='dashed')
    ax = plt.gca()
    #plt.tight_layout()
    #fig = plt.gcf()
    #fig.set_size_inches(10, 10)
    plt.savefig(FILE_OUTPUT_PATH)
    plt.clf()
    plt.cla()
    plt.close()
    #plt.show()

''''
Get a list from file reading first line only
'''
def getListFromFile(path):
    with open(path) as f:
        lines = f.readlines()

    return ast.literal_eval(lines[0])

main()
