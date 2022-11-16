import numpy as np
import matplotlib.pyplot as plt
from tflite_runtime.interpreter import Interpreter
import time
import os
import random
from utils import functions
from utils import algorithms as alg


initial_dutty = 0.15 # Initial duty cycle for when the random_init variable is set to True
EXPERIMENT_SECONDS = 1 # Length time of each experiment
SAMPLE_TIME = 0.02 # sample time for the excequition of the algorithms
dDutty = 0 # initial change of duty cycle
len_window = 2 # window length for creating an average of measurements for current and voltage
algorithms = ["DQN", "P&O"] # algorithms that will be used
irradiation = "400-500" # Irradiation tracked according to pyranometer
number_DQN = "_003_250" # current algorithm being used for the DQN
num_experiments = 5 # number of runs where the experiment will be repeated
colors = [["darkorange", "bisque"], ["royalblue", "lightsteelblue"]] # colors of the graphs
PS_scenario = 0 # Partial Shading scenario specified
random_init = True # condition that sets if the inital duty cycle will be set randomly


# config Interpreter
if 'DQN' in algorithms:
    tflite_path = os.getcwd() + "/models/DQN" + number_DQN  + ".tflite"
    interpreter = Interpreter(tflite_path)
    
#----------------------------------------------
# create_graph
# this function creates the graphs for the average power at each time-step and will
# also plot the standard deviation at each time steps for the n runs.
def create_graph(results_dict, results_total):
    parent_dir = os.getcwd() + "/data/"
    if not random_init:
        directory = "P&O vs DQN " + number_DQN + " irr="+irradiation + " PT=" + str(PS_scenario)
    else:
        directory = "P&O vs DQN " + number_DQN + " irr="+irradiation + " PT=" + str(PS_scenario) + "_random_init"

    path = os.path.join(parent_dir, directory)
    isExist = os.path.exists(path)
    if isExist == False:
        os.mkdir(path)


    figures, axis = plt.subplots(2,1, figsize=(8, 8))
    sigmas = {}
    for algorithm in algorithms:
        sigmas[algorithm] = np.zeros((2,len(results_total[algorithm][0][0])))
        for experiment in range(num_experiments):
            x_minus_mean = np.square(np.abs(results_total[algorithm][experiment][0] - results_dict[algorithm][0]))
            x_minus_mean_dutty = np.square(np.abs(results_total[algorithm][experiment][1] - results_dict[algorithm][1]))
            sigmas[algorithm][0]  = sigmas[algorithm][0] + x_minus_mean
            sigmas[algorithm][1]  = sigmas[algorithm][1] + x_minus_mean_dutty
        sigmas[algorithm][0] = np.sqrt(sigmas[algorithm][0]/num_experiments)
        sigmas[algorithm][1] = np.sqrt(sigmas[algorithm][1]/num_experiments)
    
    
    for i, algorithm in enumerate(algorithms):
        average_power = str(int(np.mean(results_dict[algorithm][0])))
        
        axis[0].plot(time_range, results_dict[algorithm][0], label=algorithm + ", Avg. Power="+average_power, color = colors[i][0])
        axis[0].fill_between(time_range, results_dict[algorithm][0]-sigmas[algorithm][0], results_dict[algorithm][0]+sigmas[algorithm][0],
        edgecolor=colors[i][0], facecolor=colors[i][1])
        
        
        axis[1].step(time_range, results_dict[algorithm][1], label="Duty Cycle " + algorithm, color = colors[i][0])
        axis[1].fill_between(time_range, results_dict[algorithm][1]-sigmas[algorithm][1], results_dict[algorithm][1]+sigmas[algorithm][1],
        edgecolor=colors[i][0], facecolor=colors[i][1])
    
    
    if PS_scenario == 0:
        title = "Power of algorithms DQN and P&O \n (G=" + irradiation + "W/m2, Averaged over " + str(num_experiments) + " runs, No Partial Shading)"
    else:
        title = "Power of algorithms DQN and P&O \n (G=" + irradiation + "W/m2, Averaged over " + str(num_experiments) + " runs, Partial Shading Scenario " + str(PS_scenario) + ")"

    axis[0].set_title(title, fontweight="bold", fontsize=10)
    axis[0].set_ylabel("Power (W)"  )
    axis[0].set_xlabel("Time (s)"  )
    axis[0].legend(loc = "lower right")
    axis[0].grid()
    axis[1].set_title("Duty Cycle of algorithms DQN and P&O", fontweight="bold", fontsize=10)
    axis[1].set_ylabel("Duty Cycle"  )
    axis[1].set_xlabel("Time (s)"  )
    axis[1].grid()
    axis[1].legend()
    name ="P&O vs DQN "
    if not random_init:
        path_fig = path + "/P&O vs DQN " + number_DQN + " average irr="+irradiation+" averaged over " + str(num_experiments) + " runs.png"
    else:
        path_fig = path + "/P&O vs DQN " + number_DQN + " average irr="+irradiation+" averaged over " + str(num_experiments) + " runs_randominit.png"

    figures.tight_layout()

    plt.savefig(path_fig)
    
    
    np.save(path + "/mean.npy", results_dict)
    np.save(path+ "/every_data.npy", results_total)
    np.save(path+ "/sigmas.npy", sigmas)

    plt.show()


# this function gets the input current and voltage at each time step
def get_data():
    voltage_window = np.zeros(len_window)
    current_window = np.zeros(len_window)
    for i in range(len_window):
        voltage_window[i] = functions.get_voltage(0)
        current_window[i] = functions.get_current(1)
    voltage = np.mean(voltage_window)
    current = np.mean(current_window)
    return voltage, current


    
if __name__ == "__main__":

    max_range = int((EXPERIMENT_SECONDS+SAMPLE_TIME)/SAMPLE_TIME)
    results_mean = {}
    results_total = {algorithm : {} for algorithm in algorithms}
    time_range = np.arange(0, EXPERIMENT_SECONDS+SAMPLE_TIME, SAMPLE_TIME)
    times_rls = []
    for experiment in range(num_experiments):
        if random_init: 
                initial_dutty = random.uniform(0.15, 0.9)
        for algorithm in algorithms:
            if experiment == 0:
                results_mean[algorithm] = np.zeros((2,max_range))
            results_total[algorithm][experiment] = np.zeros((2,max_range))
            last_power = 0
            last_voltage = 0
            last_current = 0
            
            start_time = time.time()
            D = functions.set_dutty_cycle(initial_dutty)
            last_voltage, last_current = get_data()
            last_power = last_current*last_voltage
            end_time = time.time()
            results_mean[algorithm][0][0] = results_mean[algorithm][0][0] + last_power
            results_mean[algorithm][1][0] = results_mean[algorithm][1][0] + D
            results_total[algorithm][experiment][0][0] = last_power
            results_total[algorithm][experiment][1][0] = D
            
            functions.execute_sleep(start_time, end_time,SAMPLE_TIME)
            
            for step in range(1,max_range):
                start_time = time.time()
                voltage, current = get_data()
                power = voltage*current
            
                if algorithm == 'P&O':
                    D = alg.PYO(last_power, last_voltage, power, voltage, D)
                elif algorithm == 'DQN':
                    dDutty, times_rl = alg.RL_Algorithm(last_power, last_voltage, power, voltage, dDutty, interpreter)
                    D+=dDutty
                    #times_rls.append(times_rl)
                results_mean[algorithm][0][step] = results_mean[algorithm][0][step] + power
                results_total[algorithm][experiment][0][step] = power
            
                last_current = current
                last_voltage = voltage
                last_power = power
                
                end_time = time.time()
                
                functions.execute_sleep(start_time, end_time,SAMPLE_TIME)
                D = functions.set_dutty_cycle(D)
                results_mean[algorithm][1][step] = results_mean[algorithm][1][step] + D
                results_total[algorithm][experiment][1][step] = D
    for algorithm in algorithms:
        results_mean[algorithm][0] = results_mean[algorithm][0]/num_experiments 
        results_mean[algorithm][1] = results_mean[algorithm][1]/num_experiments
    create_graph(results_mean, results_total)


