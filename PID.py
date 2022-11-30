import numpy as np
import matplotlib.pyplot as plt
import Adafruit_MCP4725
import Adafruit_ADS1x15
import time
from simple_pid import PID
from utils import functions

Kp = 2.2e-5
Ki = 0.12
Kd = 2.1999999999999994e-9
len_window = 10 # length of the window used to calculate an avetage of 10 iterations for the output voltage and input voltage
desired_voltage = 5 # Desired output votlage
initial_dutty = 0.5 # initial duty cycle set

SAMPLE_TIME = 0.1 # sample time for each experiment


pid = PID(Kp, Ki, Kd, setpoint=desired_voltage)


# function to get the data of the 
def get_data():
    voltage_window = np.zeros(len_window)
    output_voltage_window = np.zeros(len_window)
    for i in range(len_window):
        voltage_window[i] = functions.get_voltage(0)
        output_voltage_window[i] = functions.get_voltage(2)
    voltage = np.mean(voltage_window)
    output_voltage = np.mean(output_voltage_window)
    return voltage, output_voltage



if __name__ == "__main__":
    D = functions.set_dutty_cycle(initial_dutty)
    start_time = time.time()
    while True:
        input_voltage, output_voltage = get_data()
        D = pid(output_voltage)
        end_time = time.time()
        functions.execute_sleep(start_time, end_time,SAMPLE_TIME)
        D = functions.set_dutty_cycle(D)
        start_time = time.time()
        print('|Input Voltage: {0:10.2f} | Output Voltage: {1:10.2f}| Current Duty: {2:10.2f}'.format(input_voltage, output_voltage, D))
        
        
