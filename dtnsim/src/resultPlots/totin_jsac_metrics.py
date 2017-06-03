'''
This script process a sample generated by DTNSIM and and computes plots for the followings metrics:

            -> ("appBundleSent:count","bundles sent")
            -> ("appBundleReceived:count", "bundles received count")
            -> ("appBundleReceivedDelay", "bundles received delay")
            -> ("dtnBundleSentToCom:count", "bundles sent to Com")
            -> ("dtnBundleSentToApp:count", "bundles sends to app"),
            -> ("dtnBundleReceivedFromCom:count", "bundles received from Com")
            -> ("dtnBundleReceivedFromApp:count", "bundles received from App")
            -> ("dtnBundleReRouted:count", "blundles re-routed")
            -> ("routeCgrDijkstraCalls:sum", "calls to CgrDijkstra")
            -> ("routeCgrDijkstraLoops:sum", "Cgr Dijkstra loops"),
            -> ("routeCgrRouteTableEntriesCreated:max", "CGR table entries")
            -> ("routeCgrRouteTableEntriesExplored:max","CGR table entries explored")

By each configuration given by these parameters: ROUTING_TYPE,VOLUME_AWARE,EXTENSION_BLOCK,CONTACT_PLAN and RETURN_TO_SENDER.
All metrics will be ploted vs number of bundles generated. And metrics are calculated as plus of metric value for each node in the network.


Arguments
    -> INPUT_PATH: Path to folder that contains input files.
    -> OUTPUT_PATH: Path to folder in which script will write results.

    -> DENSITY_RANGE: A range of float values for wich CPs have been generated.
    -> CP: Amount of contact plans
    -> repetitions: Amount of repetitions for each contact plan. If for a contact plan there aren't more than one runs
                    it should be setted to 1.
    -> deletedContact: Maximun number of deleted contact. Input data must be contain a file for each case in [0
                       to deletedContact].

Also, there is the following convention for input files (stored in INPUT_PATH/):

    General-routingType=routeListType#3a%ROUTING_TYPE%,volumeAware#3a%VOLUME_AWARE%,extensionBlock#3a%EXTENSION_BLOCK%,contactPlan#3a%CONTACT_PLAN%,returnToSender=%RETURN_TO_SENDER%,bundlesNumber=%BUNDLES_GENERATED%-#0

The variable parts in string are marked with %%. They are:
    -> %ROUTING_TYPE%
    -> %VOLUME_AWARE%
    -> %EXTENSION_BLOCK%
    -> %CONTACT_PLAN%
    -> %RETURN_TO_SENDER%
    -> %BUNDLES_GENERATED%

OUTPUT will be in OUTPUT_PATH/, with following convention:
    -> Metric=%METRIC%,%CASE-DESCRIPTION%.txt will contain function number of generated bundles -> value of metric
    -> Metric=%METRIC%,%CASE-DESCRIPTION%.png will contain funtion plot

        where
            %METRIC% is the metric plotted
            %CASE-DESCRIPTION% is the case plotted description in the following form:
                General-routingType=%s,volumeAware=%s,extensionBlock=%s,contactPlan=%s,returnToSender=%s,bundlesNumber=%d



'''

import sqlite3
import matplotlib.pyplot as plt

INPUT_PATH = "/home/juanfraire/git/dtnsim/dtnsim/src/results"
OUTPUT_PATH = "/home/juanfraire/git/dtnsim/dtnsim/src/resultPlots/totin_jsac_plots"

ROUTING_TYPE = ['oneBestPath','perNeighborBestPath','allPaths-firstEnding','allPaths-firstDepleted','allPaths-initial+anchor']
VOLUME_AWARE = ['off','1stContact','allContacts','allContacts','allContacts']
EXTENSION_BLOCK = ['off','off','off','on','on']
CONTACT_PLAN = ['local','local','local','local','global']

RETURN_TO_SENDER = ['true','false']
BUNDLES_NUMBERS = [10,15,20,25,30,35,40,45,50]

METRICS = [
            ("appBundleSent:count","bundles sent"),
            ("appBundleReceived:count", "bundles received count"),
            ("appBundleReceivedDelay", "bundles received delay"),
            ("dtnBundleSentToCom:count", "bundles sent to Com"),
            ("dtnBundleSentToApp:count", "bundles sends to app"),
            ("dtnBundleReceivedFromCom:count", "bundles received from Com"),
            ("dtnBundleReceivedFromApp:count", "bundles received from App"),
            ("dtnBundleReRouted:count", "blundles re-routed"),
            ("routeCgrDijkstraCalls:sum", "calls to CgrDijkstra"),
            ("routeCgrDijkstraLoops:sum", "Cgr Dijkstra loops"),
            ("routeCgrRouteTableEntriesCreated:max", "CGR table entries"),
            ("routeCgrRouteTableEntriesExplored:max","CGR table entries explored")]


def main():
    for routeListType in ROUTING_TYPE:
        for volume_aware,exBlock,cp in list(zip(VOLUME_AWARE, EXTENSION_BLOCK,CONTACT_PLAN)):
            for returnToSender in RETURN_TO_SENDER:
                for metric in METRICS:
                    f = []
                    for bundlesNumber in BUNDLES_NUMBERS:
                        # Connect to database
                        print("%s/General-routingType=routeListType#3a%s,volumeAware#3a%s,extensionBlock#3a%s,contactPlan#3a%s,returnToSender=%s,bundlesNumber=%d-#0.sca"
                                %(INPUT_PATH,routeListType,volume_aware,exBlock,cp,returnToSender,bundlesNumber))

                        conn = sqlite3.connect("%s/General-routingType=routeListType#3a%s,volumeAware#3a%s,extensionBlock#3a%s,contactPlan#3a%s,returnToSender=%s,bundlesNumber=%d-#0.sca"
                                                %(INPUT_PATH,routeListType,volume_aware,exBlock,cp,returnToSender,bundlesNumber))
                        conn.row_factory = sqlite3.Row
                        cur = conn.cursor()

                        # execute sql query to get bundles received by all nodes
                        cur.execute("SELECT SUM(scalarValue) AS result FROM scalar WHERE scalarName='%s'" % (metric[0]))
                        rows0 = cur.fetchall()
                        scalarValue = rows0[0]["result"]  # 0 if (rows0[0]["result"] == None) else rows0[0]["result"]

                        f.append((bundlesNumber,scalarValue))

                    # save function
                    text_file = open(
                        "%s/Metric=%s,General-routingType=%s,volumeAware=%s,extensionBlock=%s,contactPlan=%s,returnToSender=%s,bundlesNumber=%d.txt"
                        % (OUTPUT_PATH, metric[0], routeListType, volume_aware, exBlock, cp, returnToSender, bundlesNumber),"w")

                    text_file.write(str(f))
                    text_file.close()

                    # plot results
                    plt.plot([x[0] for x in f], [y[1] for y in f], '--o')
                    plt.xlabel('Number of bundles generated from 1 to 5')
                    plt.ylabel(metric[1])
                    plt.grid(color='gray', linestyle='dashed')
                    plt.savefig(
                        "%s/Metric=%s,General-routingType=%s,volumeAware=%s,extensionBlock=%s,contactPlan=%s,returnToSender=%s,bundlesNumber=%d.png"
                        % (OUTPUT_PATH,metric[0], routeListType, volume_aware, exBlock, cp, returnToSender, bundlesNumber))

                    plt.clf()
                    plt.cla()
                    plt.close()

main()
