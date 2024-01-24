import json
import sys
import json2latex
import math


"""
In this function all seeds of a run from an algorithm in a simulation are collected and put into a map to have access to them later

@param path: The path to the collected metrics
       num_of_seeds: The number of seeds tested
       
@return The dictionary with the collected seed metrics

@author Simon Rink
"""
def collect_seed_metrics(path, num_of_seeds):
	seeds_dict = dict()
	
	for num in range(0, num_of_seeds): #read all seed files
		with open(path + '/metrics/jsonResults_' + str(num) + '.txt') as file1:
			seeds_dict[num] = json.load(file1)
	
	result = dict() #initiate result dictionary
	bundleIds = seeds_dict[0]['bundleIds'] #collect the bundles from the simulation
	result["receivedIds"] = dict()
	bundles_received_count = dict()
	rucop_calls = 0 
	computation_time = 0
	
	#set up required seed values
	seed_values = dict()
	seed_values["ratio"] = dict()
	seed_values["times"] = dict()
	seed_values["counts"] = dict()
	
	delivery_ratio = 0
	
	
	for id_ in bundleIds:
		bundles_received_count[id_] = 0
	
	for num in range(0, num_of_seeds):
		seed_values["times"][num] = dict()
		seed_values["counts"][num] = dict()
		delivery_ratio += len(seeds_dict[num]["receivedIds"]) / len(bundleIds)
		seed_values["ratio"][num] = len(seeds_dict[num]["receivedIds"]) / len(bundleIds)
		for id_ in bundleIds:
			seed_values["times"][num][id_] = -1 #if no bundle was received in that seed, set it to -1
			seed_values["counts"][num][id_] = -1
			if id_ in seeds_dict[num]["receivedIds"]:
				if (seeds_dict[num]["bundleDeliveryTimes"][id_] == 0):
					seed_values["times"][num][id_] = 1 #set the delivery time to 1, if it was actually 0 to compete for the 0-ranges
				else:
					seed_values["times"][num][id_] = seeds_dict[num]["bundleDeliveryTimes"][id_]
				seed_values["counts"][num][id_] = seeds_dict[num]["bundleDeliveryCounts"][id_]
				bundles_received_count[id_] = bundles_received_count[id_] + 1
				result["receivedIds"][id_] = 1 #Bundle was received at least once in the run
		rucop_calls += seeds_dict[num]["RUCoPCalls"]
		computation_time += seeds_dict[num]["RUCoPComputationTime"]
	
	rucop_calls = rucop_calls / num_of_seeds
	computation_time = computation_time / num_of_seeds
							
	delivery_ratio = delivery_ratio / num_of_seeds
	
	
	if delivery_ratio == 0:
		seed_values["ratio"][0] = 1 / len(bundleIds) #if the bundle has not been delivered at any time, give it one bundle for comparison reason
	
	result["bundleIds"] = bundleIds
	result["seed_values"] = seed_values
	result["calls"] = rucop_calls
	result["computation"] = computation_time
	
	return result
	
"""
This function computes the covariance for two sets with the same length
@param set_one: The values from the first set
	   mean_one: The mean of the first set
	   set_two: The values from the second set
	   mean_two: The mean of the second set

@return The computed covariance

@author Simon Rink
"""
def calculate_covariance(set_one, mean_one, set_two, mean_two):
	
	if len(set_one) == 0 or len(set_one) == 1:
		return 0
	covariance = 0
	for i in range(0, len(set_one)):
		covariance += (set_one[i] - mean_one) * (set_two[i] - mean_two)
	
	return covariance / (len(set_one) - 1)
	
"""
This function computes the standard deviation of a data set

@param data_set: The given data set
	   mean: The mean of the data set
	   
@return The computed standard deviation

@author Simon Rink
"""
def calculate_standard_deviation(data_set, mean):

	if len(data_set) == 0 or len(data_set) == 1:
		return 0	
	sd = 0
	for i in range(0, len(data_set)):
		sd += (data_set[i] - mean)**2
	
	return math.sqrt(sd / (len(data_set) - 1))
	
"""
This function computes the mean for a given data set

@param data_set: The given data set

@return The computed mean

@author Simon Rink
"""
def calculate_mean(data_set):
	
	if len(data_set) == 0:
		return 0
	mean = 0
	for i in range(0, len(data_set)):
		mean += data_set[i]
		
	return mean / len(data_set)
		
"""
This function computes the 95 % CI and the mean for the comparison of two sets, thus including the error propagation"

@param set_other: The values from the algorithm to be compared with CGR
	   set_cgr: The values from the CGR run
	   
@return The computed CI

@author Simon Rink
"""
def compute_confidence_interval(set_other, set_cgr):

	result = dict()
	other_mean = calculate_mean(set_other)
	
	other_sd = calculate_standard_deviation(set_other, other_mean)
	
	cgr_mean = calculate_mean(set_cgr)

	cgr_sd = calculate_standard_deviation(set_cgr, cgr_mean)

	
	cv = calculate_covariance(set_other, other_mean, set_cgr, cgr_mean)

	#use formula for error propagation, if both means and sds are equal, the resulting confidence is also
	if (other_mean == cgr_mean and other_sd == cgr_sd):
		confidence = other_sd
	else:
		root = math.sqrt((other_sd/other_mean)**2 + (cgr_sd/cgr_mean)**2 - 2*(cv/(cgr_mean * other_mean)))
		confidence = (other_mean / cgr_mean) * root
	
	result["mean"] = other_mean / cgr_mean
	result["confidence"] = (1.96 * confidence) / math.sqrt(len(set_other))
	
	return result
	
"""
This function compares the results of CGR run with that of another algorithm

@param cgr_result: The results from CGR
	   other_result: The results from the other algorithm
	   
@return A dictionary with the computed results

@author Simon Rink
""" 			
def compare_with_cgr(cgr_result, other_result, num_of_seeds):
	
	bundleIds = cgr_result['bundleIds']
	receivedIds = cgr_result["receivedIds"]

	
	delivery_ratio_result = compute_confidence_interval(other_result["seed_values"]["ratio"], cgr_result["seed_values"]["ratio"]) #compute result for delivery ratio
	delivery_ratio = delivery_ratio_result["mean"]
	delivery_ratio_ci = delivery_ratio_result["confidence"]
	
	#set up dictionaries for delivery delay and energy efficiency
	other_delivery = dict()
	cgr_delivery = dict()
	other_count = dict()
	cgr_count = dict()
	bundles_arrived = dict()
	bundles_results = dict()
	bundles_results["times"] = dict()
	bundles_results["counts"] = dict()
	overall_received = 0
	
	for id_ in receivedIds:
		bundles_arrived[id_] = 0
		other_delivery[id_] = dict()
		cgr_delivery[id_] = dict()
		other_count[id_] = dict()
		cgr_count[id_] = dict()
		for num in range(0, num_of_seeds):
			if (cgr_result["seed_values"]["times"][num][id_] != -1 and other_result["seed_values"]["times"][num][id_] != -1): #only compare two seeds if the bundles arrived in both
				other_delivery[id_][bundles_arrived[id_]] = other_result["seed_values"]["times"][num][id_]
				cgr_delivery[id_][bundles_arrived[id_]] = cgr_result["seed_values"]["times"][num][id_]
				other_count[id_][bundles_arrived[id_]] = other_result["seed_values"]["counts"][num][id_]
				cgr_count[id_][bundles_arrived[id_]] = cgr_result["seed_values"]["counts"][num][id_]
				bundles_arrived[id_] = bundles_arrived[id_] + 1
		
		if (bundles_arrived[id_] > 0):	#compute delivery delay and energy efficiency results	
			bundles_results["times"][id_] = compute_confidence_interval(other_delivery[id_], cgr_delivery[id_])
			bundles_results["counts"][id_] = compute_confidence_interval(other_count[id_], cgr_count[id_])
		
	delivery_times = 0
	delivery_times_ci = 0
	delivery_counts = 0
	delivery_counts_ci = 0
	
	#computes means for delay, efficiency and their respective CIs over all bundles
	for id_ in receivedIds:
		if (bundles_arrived[id_] > 0):
			delivery_times += bundles_results["times"][id_]["mean"]
			delivery_times_ci += bundles_results["times"][id_]["confidence"]
			delivery_counts += bundles_results["counts"][id_]["mean"]
			delivery_counts_ci += bundles_results["counts"][id_]["confidence"]
			overall_received +=1
		
	delivery_times = delivery_times / overall_received
	delivery_times_ci = delivery_times_ci / overall_received
	delivery_counts = delivery_counts / overall_received
	delivery_counts_ci = delivery_counts_ci / overall_received
		
	#store results
	result = dict()
	
	result["delivery_ratio"] = delivery_ratio - 1
	result["delivery_ratio_ci"] = delivery_ratio_ci
	result["delivery_times"] = delivery_times - 1
	result["delivery_times_ci"] = delivery_times_ci
	result["delivery_counts"] = 1 - delivery_counts
	result["delivery_counts_ci"] = delivery_counts_ci
	result["calls"] = other_result["calls"]
	result["computation"] = other_result["computation"]
	
	return result
	
		
"""
This function analyzes one run of an algorithm with CGR
@param path: The path to the results from the other algorithm
	   num_of_seeds: The number of tested seeds
	   cgr_result: The results from CGR

@return The analyzed results

@author Simon Rink
"""
def analyze_run(path, num_of_seeds, cgr_result):
	other_result = collect_seed_metrics(path, num_of_seeds)
	
	cgr_comparison = compare_with_cgr(cgr_result, other_result, num_of_seeds)
	
	return cgr_comparison
	
"""
This function analyzes one whole simulation

@param path: The path to the simulation
       pfs: The used failure probabilities
       num_of_seeds: The number of tested seeds
       num: The simulation number
       
@return A dictionary containing all results

@author Simon Rink
""" 
def analyze_simulation(path, pfs, num_of_seeds, num):
	cgr_results = dict()
	
	for pf in pfs: #compute cgr results for each pf
		cgr_results[pf] = collect_seed_metrics(path + '/OCGR/pf=' + str(pf) + '/no_opp', num_of_seeds)
		
	algorithm_results = dict()
	algorithm_results["OCGR"] = dict()
	algorithm_results["RUCoP"] = dict()
	algorithm_results["CGR-AK"] = dict()
	algorithm_results["RUCoP-AK"] = dict()
	algorithm_results["OCGR-UCoP"] = dict()
	algorithm_results["ORUCoP"] = dict()
	algorithm_results["CGR-UCoP"] = dict()
	algorithm_results["CGR-UCoP-AK"] = dict()
	algorithm_results["SW5"] = dict()
	algorithm_results["SW10"] = dict()
	algorithm_results["SW15"] = dict()
	algorithm_results["PRoPHET"] = dict()
	
	for pf in pfs: #compare all algorithms with CGR for each pf
		algorithm_results["OCGR"][pf] = analyze_run(path + '/OCGR/pf=' + str(pf) + '/opp_not_known', num_of_seeds, cgr_results[pf])
		algorithm_results["RUCoP"][pf] = analyze_run(path + '/ORUCoP/pf=' + str(pf) + '/no_opp', num_of_seeds, cgr_results[pf])
		algorithm_results["CGR-AK"][pf] = analyze_run(path + '/OCGR/pf=' + str(pf) + '/opp_known', num_of_seeds, cgr_results[pf])
		algorithm_results["RUCoP-AK"][pf] = analyze_run(path + '/ORUCoP/pf=' + str(pf) + '/opp_known', num_of_seeds, cgr_results[pf])
		algorithm_results["OCGR-UCoP"][pf] = analyze_run(path + '/OCGR-UCoP/pf=' + str(pf) + '/opp_not_known', num_of_seeds, cgr_results[pf])
		algorithm_results["ORUCoP"][pf] = analyze_run(path + '/ORUCoP/pf=' + str(pf) + '/opp_not_known', num_of_seeds, cgr_results[pf])
		algorithm_results["CGR-UCoP"][pf] = analyze_run(path + '/OCGR-UCoP/pf=' + str(pf) + '/no_opp', num_of_seeds, cgr_results[pf])
		algorithm_results["CGR-UCoP-AK"][pf] = analyze_run(path + '/OCGR-UCoP/pf=' + str(pf) + '/opp_known', num_of_seeds, cgr_results[pf])
		algorithm_results["SW5"][pf] = analyze_run(path + '/SW5/pf=' + str(pf) + '/opp_not_known', num_of_seeds, cgr_results[pf])
		algorithm_results["SW10"][pf] = analyze_run(path + '/SW10/pf=' + str(pf) + '/opp_not_known', num_of_seeds, cgr_results[pf])
		algorithm_results["SW15"][pf] = analyze_run(path + '/SW15/pf=' + str(pf) + '/opp_not_known', num_of_seeds, cgr_results[pf])
		algorithm_results["PRoPHET"][pf] = analyze_run(path + '/PRoPHET/pf=' + str(pf) + '/opp_not_known', num_of_seeds, cgr_results[pf])
		
	
	return algorithm_results
	
"""
This function prints one metric for simulations with multiple failure probabilites

@param results: The computed results
	   metric: The metric (e.g. delivery ratio) to be printed
	   pfs: The used failure probabilities
	   num: The number of the simulation
	   
@author Simon Rink
"""
def print_metric_graph_non_specific(results, metric, pfs, num):
	final_string = "x "
	
	for i in range(1, 25): #set up y values for each algorithm. These are the mean and their corresponding CI
		final_string += "y" + str(i) + " "
		
	final_string += "\n"
	
	for pf in pfs:
		if pf == 0.2:
			final_string += "1 "
		if pf == 0.35:
			final_string += "2 "
		if pf == 0.5:
			final_string += "3 "
		if pf == 0.65:
			final_string += "4 "
		if pf == 0.8:
			final_string += "5 "
			
		final_string += str(round(results["OCGR"][pf][metric] * 100, 2)) + " "
		final_string += str(round(results["CGR-AK"][pf][metric] * 100, 2))  + " "
		final_string += str(round(results["RUCoP"][pf][metric] * 100, 2))  + " "
		final_string += str(round(results["ORUCoP"][pf][metric] * 100, 2))  + " "
		final_string += str(round(results["RUCoP-AK"][pf][metric] * 100, 2))  + " "
		final_string += str(round(results["CGR-UCoP"][pf][metric] * 100, 2))  + " "
		final_string += str(round(results["OCGR-UCoP"][pf][metric] * 100, 2))  + " "
		final_string += str(round(results["CGR-UCoP-AK"][pf][metric] * 100, 2) ) + " "
		final_string += str(round(results["SW5"][pf][metric] * 100, 2) ) + " "
		final_string += str(round(results["SW10"][pf][metric] * 100, 2) ) + " "
		final_string += str(round(results["SW15"][pf][metric] * 100, 2) ) + " "
		final_string += str(round(results["PRoPHET"][pf][metric] * 100, 2) ) + " "
		final_string += str(round(results["OCGR"][pf][metric + "_ci"] * 100, 2)) + " "
		final_string += str(round(results["CGR-AK"][pf][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["RUCoP"][pf][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["ORUCoP"][pf][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["RUCoP-AK"][pf][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["CGR-UCoP"][pf][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["OCGR-UCoP"][pf][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["CGR-UCoP-AK"][pf][metric + "_ci"] * 100, 2) ) + " "
		final_string += str(round(results["SW5"][pf][metric + "_ci"]  * 100, 2) ) + " "
		final_string += str(round(results["SW10"][pf][metric + "_ci"] * 100, 2) ) + " "
		final_string += str(round(results["SW15"][pf][metric + "_ci"] * 100, 2) ) + " "
		final_string += str(round(results["PRoPHET"][pf][metric + "_ci"] * 100, 2) ) + " "		
		final_string += "\n"
		
	with open("plots/sim_" + str(num) + "_" + metric, "w") as output:
		output.write(final_string)

"""
This funtion prints one metric for a simulation with only one failure probability

@param results: The aquired results
	   metric: The metric (e.g. delivery ratio) to be printed
	   num: The number of the simulation
	   
@author Simon Rink
"""		
def print_metric_graph_specific(results, metric, num):
	final_string = "x "
	
	for i in range(1, 25):  #set up y values for each algorithm. These are the mean and their corresponding CI
		final_string += "y" + str(i) + " "
		
	final_string += "\n"
	
	for i in range(0, 2):
		if i == 0:
			final_string += "0 "
		else:
			final_string += "2 "
			
		final_string += str(round(results["OCGR"][-1][metric] * 100, 2)) + " "
		final_string += str(round(results["CGR-AK"][-1][metric] * 100, 2))  + " "
		final_string += str(round(results["RUCoP"][-1][metric] * 100, 2))  + " "
		final_string += str(round(results["ORUCoP"][-1][metric] * 100, 2))  + " "
		final_string += str(round(results["RUCoP-AK"][-1][metric] * 100, 2))  + " "
		final_string += str(round(results["CGR-UCoP"][-1][metric] * 100, 2))  + " "
		final_string += str(round(results["OCGR-UCoP"][-1][metric] * 100, 2))  + " "
		final_string += str(round(results["CGR-UCoP-AK"][-1][metric] * 100, 2) ) + " "
		final_string += str(round(results["SW5"][-1][metric] * 100, 2) ) + " "
		final_string += str(round(results["SW10"][-1][metric] * 100, 2) ) + " "
		final_string += str(round(results["SW15"][-1][metric] * 100, 2) ) + " "
		final_string += str(round(results["PRoPHET"][-1][metric] * 100, 2) ) + " "			
		final_string += str(round(results["OCGR"][-1][metric + "_ci"] * 100, 2)) + " "
		final_string += str(round(results["CGR-AK"][-1][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["RUCoP"][-1][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["ORUCoP"][-1][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["RUCoP-AK"][-1][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["CGR-UCoP"][-1][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["OCGR-UCoP"][-1][metric + "_ci"] * 100, 2))  + " "
		final_string += str(round(results["CGR-UCoP-AK"][-1][metric + "_ci"] * 100, 2) ) + " "
		final_string += str(round(results["SW5"][-1][metric + "_ci"]  * 100, 2) ) + " "
		final_string += str(round(results["SW10"][-1][metric + "_ci"] * 100, 2) ) + " "
		final_string += str(round(results["SW15"][-1][metric + "_ci"] * 100, 2) ) + " "
		final_string += str(round(results["PRoPHET"][-1][metric + "_ci"] * 100, 2) ) + " "		
	
		final_string += "\n"
	
	with open("plots/sim_" + str(num) + "_" + metric, "w") as output:
		output.write(final_string)
	
"""
This function prints results for one simulation

@param result: The collected results from the simulation
	   pfs: The used failure probabilities
	   num: The number of the current simulation
	   
@author Simon Rink
"""
def print_results(results, pfs, num):
	
	if (num < 7): #All simulations below 7 use multiple failure probabilites
		print_metric_graph_non_specific(results, "delivery_ratio", pfs, num)
		print_metric_graph_non_specific(results, "delivery_times", pfs, num)
		print_metric_graph_non_specific(results, "delivery_counts", pfs, num)
	else:
		print_metric_graph_specific(results, "delivery_ratio", num)
		print_metric_graph_specific(results, "delivery_times", num)
		print_metric_graph_specific(results, "delivery_counts", num)
	
"""
This function calculates the mean for each metric for each pf for two simulations from one category

@param result_1: The results from the first simulation
	   result_2: The results from the second simulation
	   
@return The combined simulation results

@author Simon Rink
"""
def combine_result(result_1, result_2):
	final_result = dict()
	
	for algorithm in result_1:
		final_result[algorithm] = dict()
		for pf in result_1[algorithm]:
			final_result[algorithm][pf] = dict()
			for metric in result_1[algorithm][pf]:
				final_result[algorithm][pf][metric] = (result_1[algorithm][pf][metric] + result_2[algorithm][pf][metric]) / 2
	
	return final_result
	
"""
This function computes the means for each metric for each algorithm and prints them

@param final_result: All combined results from each categories

@author Simon Rink
""" 
def generate_overall_means(final_results):
	
	overall_means = dict()
	for algorithm in final_results[0]:
		overall_means[algorithm] = dict()
		overall_means[algorithm]["delivery_ratio"] = 0
		overall_means[algorithm]["delivery_times"] = 0
		overall_means[algorithm]["delivery_counts"] = 0
		overall_means[algorithm]["delivery_ratio_ci"] = 0
		overall_means[algorithm]["delivery_times_ci"] = 0
		overall_means[algorithm]["delivery_counts_ci"] = 0
		overall_means[algorithm]["calls"] = 0
		overall_means[algorithm]["computation"] = 0
		
	
	for num in final_results:
		for algorithm in final_results[num]:
			for pf in final_results[num][algorithm]:
				for metric in final_results[num][algorithm][pf]:
					overall_means[algorithm][metric] += final_results[num][algorithm][pf][metric]
					
					
	for algorithm in overall_means:
		overall_means[algorithm]["delivery_ratio"] = overall_means[algorithm]["delivery_ratio"] / 17 #there are 17 different simulation results available for each metric
		overall_means[algorithm]["delivery_times"] = overall_means[algorithm]["delivery_times"] / 17
		overall_means[algorithm]["delivery_counts"] = overall_means[algorithm]["delivery_counts"] / 17
		overall_means[algorithm]["calls"] = overall_means[algorithm]["calls"] / 17
		overall_means[algorithm]["computation"] = overall_means[algorithm]["computation"] / 17
				
	print_overall_means(overall_means)
	
"""
This function prints the overall means from above

@param overall_means: The calculated overall means

@author Simon Rink
"""
def print_overall_means(overall_means):
	
	with open("plots/means", "w") as output:
		for algorithm in overall_means:
			output.write(algorithm + ": " + str(round(overall_means[algorithm]["delivery_ratio"]*100,2)) + " " + str(round(overall_means[algorithm]["delivery_times"]*100,2)) + " " +  str(round(overall_means[algorithm]["delivery_counts"]*100,2)) + " " + str(overall_means[algorithm]["calls"]) + " " + str(overall_means[algorithm]["computation"]) + "\n")
 				
	
def main():
	num_of_sims = 10
	path = str(sys.argv[1])
	result = dict()
	final_results = dict()
	
	for sim in range(1, num_of_sims + 1): #calculate results for each simulations
		if sim < 7:
			result[sim] = analyze_simulation(path + "/simulation_" + str(sim), [0.2, 0.35, 0.5, 0.65, 0.8], 30, sim)
		else:
			result[sim] = analyze_simulation(path + "/simulation_" + str(sim), [-1], 30, sim)
			
	for i in range(0, 5): #combine all results
		final_results[i] = combine_result(result[2*i+1], result[2*i+2])
		print_results(final_results[i], [0.2, 0.35, 0.5, 0.65, 0.8], 2*i+1)
	
	generate_overall_means(final_results)
	
if __name__ == "__main__":
    main()	
		
	
	
