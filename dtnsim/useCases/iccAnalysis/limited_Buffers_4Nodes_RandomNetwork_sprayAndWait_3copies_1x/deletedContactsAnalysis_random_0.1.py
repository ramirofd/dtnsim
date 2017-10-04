'''
This script process a sample generated by DTNSIM and and computes plots for the followings metrics:
    -> Received Bundles in total
    -> Bundles Rerouted in total (amount of times that nodes re-route bundles)
    -> Hop counts in total (amount of hops that deliver bundles do in their path to destination)

All metrics will be ploted vs proportion of deleted contacts.

Arguments
    -> repetitions: Amount of repetitions for each contact plan. If for a contact plan there aren't more than one runs
                    it should be setted to 1.
    -> deletedContact: Maximun number of deleted contact. Input data must be contain a file for each case in [0
                       to deletedContact].

    -> INPUT_PATH: Path to folder that contains input files.
    -> OUTPUT_PATH: Path to folder in which script will write results.

Also, there is the following convention for input files (stored in INPUT_PATH/):

    dtnsim-faultsAware=%IS FAULT AWARE%,deleteNContacts=%NUMBER OF DELETED CONTACTS%-#%RUN NUMBER%.sca

The varriable parts in string are marked with %%. They are:
    -> %IS FAULT AWARE%
    -> %NUMBER OF DELETED CONTACTS%
    -> %RUN NUMBER%

OUTPUT:


"%s/METRIC=%s-FAULTAWARE=%s-MAX_DELETED_CONTACTS=%d-.txt"%(OUTPUT_PATH,metric[0],aware,MAX_DELETED_CONTACTS)

'''


#Received packet after a random atack, deleted contact/ number of contact
import sqlite3
import matplotlib.pyplot as plt
from functools import reduce
import sys
import os

INPUT_PATH = os.getcwd() + "/resultsRandom"
OUTPUT_PATH = os.getcwd() + "/results/results_random/0.1"

PERCENTAGE = 0.1
density = PERCENTAGE
CP_RANGE = range(10)
MAX_DELETED_CONTACTS = int(round(PERCENTAGE * 12) * 10)
AMOUNT_OF_REPETITIONS = 10
STEP=int(round(PERCENTAGE * 12))

#[(metric, x-axis label)]
METRICS = [("appBundleReceived:count","Delivered Bundles"),("deliveryRatio","Delivery Ratio"), ("dtnBundleSentToCom:count","Transmitted bundles"), ("appBundleReceivedDelay:mean","Mean Delay per Bundle"), ("appBundleReceivedHops:mean","Mean Hops per Bundle")]

def main():
    for metric in METRICS:
            cmp_graph_data = []
            for aware in ["false"]:
                f_avg_by_rep = []
                for cp in CP_RANGE:

                    if(metric[0] == "deliveryRatio"):
                        f_avg_by_rep.append(receivedPacketAv2("%s/dtnsim-CP=contactPlan#2f%1.1f#_%d,faultsAware=%s"%(INPUT_PATH, density, cp,aware),MAX_DELETED_CONTACTS,AMOUNT_OF_REPETITIONS))
                    elif( (metric[0] == "appBundleReceivedDelay:mean") or (metric[0] == "appBundleReceivedHops:mean") ):
                        f_avg_by_rep.append(receivedPacketAv3("%s/dtnsim-CP=contactPlan#2f%1.1f#_%d,faultsAware=%s" % (INPUT_PATH, density, cp, aware),MAX_DELETED_CONTACTS, AMOUNT_OF_REPETITIONS,metric[0]))
                    else:
                        #compute average function for all repetitions of a contact plan (one contac plan average- CONTACT PLAN AVERAGE)
                        f_avg_by_rep.append(receivedPacketAv("%s/dtnsim-CP=contactPlan#2f%1.1f#_%d,faultsAware=%s"%(INPUT_PATH, density, cp,aware),MAX_DELETED_CONTACTS,AMOUNT_OF_REPETITIONS,metric[0]))

                #compute average function for all contact plans (all contact plans average - DENSITY AVERAGE)
                graph_data = promList(f_avg_by_rep)
                cmp_graph_data.append(graph_data)

                # save function
                text_file = open("%s/METRIC=%s-DENSITY=%1.1f-AMOUNT_CONTACT_PLANS=%d-FAULTAWARE=%s-MAX_DELETED_CONTACTS=%d.txt"%(OUTPUT_PATH,metric[0],density,len(CP_RANGE),aware,MAX_DELETED_CONTACTS),"w")
                text_file.write(str(graph_data))
                text_file.close()

                # plot results
                plt.plot([x[0] for x in graph_data], [y[1] for y in graph_data], '--o')
                plt.xlabel('Number of deleted contacts')
                plt.ylabel(metric[1])
                plt.grid(color='gray', linestyle='dashed')
                # xint = range(0, max_deleted_contacts + 1)
                # plt.xticks(xint)
                plt.savefig("%s/METRIC=%s-DENSITY=%1.1f-AMOUNT_CONTACT_PLANS=%d-FAULTAWARE=%s-MAX_DELETED_CONTACTS=%d.png"%(OUTPUT_PATH,metric[0],density,len(CP_RANGE),aware,MAX_DELETED_CONTACTS))
                plt.clf()
                plt.cla()
                plt.close()

            # plot compared results
            #name_c1 = "CGR-MODEL-FaultsAware"
            name_c2 = "SprayAndWait-2"
            line_up, = plt.plot([x[0] for x in cmp_graph_data[0]], [y[1] for y in cmp_graph_data[0]], '--x', label=name_c2)
            #line_down, = plt.plot([x[0] for x in cmp_graph_data[1]], [y[1] for y in cmp_graph_data[1]], '--x', label=name_c2)
            plt.legend(handles=[line_up])
            plt.xlabel('deleted contacts/ total contacts')
            plt.ylabel(metric[1])
            plt.grid(color='gray', linestyle='dashed')
            plt.savefig(
                "%s/CMP-METRIC=%s-MAX_DELETED_CONTACTS=%d.png"
                 %(OUTPUT_PATH, metric[0], MAX_DELETED_CONTACTS))
            plt.clf()
            plt.cla()
            plt.close()


#Tengo que calcular para un contact plan para todas las repeticiones
def receivedPacketAv(input_path, max_deleted_contacts, amount_of_repetitions,metric):
    graph_data = []
    for d in range(0,max_deleted_contacts + 1, STEP):
        received_packet = 0
        for i in range(amount_of_repetitions):
            # Connect to database
            print("%s,deleteNContacts=%d-#%d.sca" % (input_path, d, i))
            conn = sqlite3.connect("%s,deleteNContacts=%d-#%d.sca" % (input_path, d, i))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # execute sql query to get bundles received by all nodes
            cur.execute("SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='%s'"%(metric))
            rows0 = cur.fetchall()
            received_packet += 0 if (rows0[0]["result"] == None) else rows0[0]["result"]

        cur.execute("SELECT MAX(scalarValue) AS result FROM scalar WHERE scalarName='contactsNumber:sum'")
        rows0 = cur.fetchall()
        contact_number = rows0[0]["result"]

        proportion = d / float(contact_number)
        graph_data.append((proportion,received_packet / float(amount_of_repetitions)))

    return  graph_data

#Tengo que calcular para un contact plan para todas las repeticiones
def receivedPacketAv2(input_path, max_deleted_contacts, amount_of_repetitions):
    graph_data = []
    for d in range(0,max_deleted_contacts + 1, STEP):
        received_packet = 0
        for i in range(amount_of_repetitions):
            # Connect to database
            print("%s,deleteNContacts=%d-#%d.sca" % (input_path, d, i))
            conn = sqlite3.connect("%s,deleteNContacts=%d-#%d.sca" % (input_path, d, i))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # execute sql query to get bundles received by all nodes
            cur.execute("SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='%s'"%("appBundleReceived:count"))
            rows0 = cur.fetchall()
            rx_packet = 0 if (rows0[0]["result"] == None) else rows0[0]["result"]

            cur.execute("SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='%s'"%("appBundleSent:count"))
            rows1 = cur.fetchall()
            tx_packet = 0 if (rows1[0]["result"] == None) else rows1[0]["result"]
            received_packet += float(rx_packet) / float(tx_packet)

        cur.execute("SELECT MAX(scalarValue) AS result FROM scalar WHERE scalarName='contactsNumber:sum'")
        rows0 = cur.fetchall()
        contact_number = rows0[0]["result"]

        proportion = d / float(contact_number)
        graph_data.append((proportion,received_packet / float(amount_of_repetitions)))

    return  graph_data

def receivedPacketAv3(input_path, max_deleted_contacts, amount_of_repetitions,metric):
    graph_data = []
    for d in range(0,max_deleted_contacts + 1, STEP):
        received_packet = 0
        for i in range(amount_of_repetitions):
            # Connect to database
            print("%s,deleteNContacts=%d-#%d.sca" % (input_path, d, i))
            conn = sqlite3.connect("%s,deleteNContacts=%d-#%d.sca" % (input_path, d, i))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # execute sql query to get bundles received by all nodes
            cur.execute("SELECT AVG(scalarValue) AS result FROM scalar WHERE scalarName='%s'"%(metric))
            rows0 = cur.fetchall()
            received_packet += 0 if (rows0[0]["result"] == None) else rows0[0]["result"]

        cur.execute("SELECT MAX(scalarValue) AS result FROM scalar WHERE scalarName='contactsNumber:sum'")
        rows0 = cur.fetchall()
        contact_number = rows0[0]["result"]

        proportion = d / float(contact_number)
        graph_data.append((proportion,received_packet / float(amount_of_repetitions)))

    return  graph_data

'''
Given a list of list of pairs: [[(x0,y0),...] , [(xn,yn),....]]
returns a unique list compute as average of above functions
'''
def promList(llist):
    assert len(llist) == len(CP_RANGE), "error amount of contact plans"
    assert len(list(filter(lambda l: len(l) != len(range(0,MAX_DELETED_CONTACTS + 1,STEP)), llist))) == 0, "error MAX_DELETED_CONTACTS"

    llist = [list(map(lambda f: f[x], llist)) for x in range(len(range(0,MAX_DELETED_CONTACTS + 1,STEP)))]
    llist = list(map(lambda l: reduce(lambda x,y: (x[0] + y[0],x[1] + y[1]),l), llist))
    return [(x[0]/float(len(CP_RANGE)), x[1]/float(len(CP_RANGE))) for x in llist]


main()


