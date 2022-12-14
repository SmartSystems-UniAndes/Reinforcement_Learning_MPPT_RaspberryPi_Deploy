import Adafruit_MCP4725
import Adafruit_ADS1x15
import numpy as np
import time

MAX_DUTTY = 0.9
MIN_DUTTY = 0.15


#Set-Up ADS
adc = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)
GAIN = 1
DATA_RATE = 920
BITS = 4096/2
VOLTAGE = 4.096

#Set-Up DAC
dac = Adafruit_MCP4725.MCP4725(address=0x60,busnum=1)
DAC_VOLTAGE_REFERENCE = 3.31
BITS_DAC = 4096



def get_current(index):
    value = adc.read_adc(index, gain=GAIN, data_rate=DATA_RATE)
    current = (value*VOLTAGE/BITS-2.5)*8/0.625 #632
    if current < 0:
        current = 0
    return current

def get_voltage(index):
    value = int(adc.read_adc(index, gain=GAIN, data_rate=DATA_RATE))
    voltage = value*(VOLTAGE/BITS)*((2+16.98)/2)#9.1547-0.042
    if voltage < 0:
        voltage = 0
    return voltage

def dutty_to_bits(dutty):
    control_voltage = dutty*-3.0704 + 2.8105
    return int(control_voltage*BITS_DAC/DAC_VOLTAGE_REFERENCE)

def set_dutty_cycle(dutty):
    if (dutty > MAX_DUTTY):
        dac.set_voltage(dutty_to_bits(MAX_DUTTY))
        dutty = MAX_DUTTY
    elif (dutty < MIN_DUTTY):
        dac.set_voltage(dutty_to_bits(MIN_DUTTY))
        dutty = MIN_DUTTY
    else:
        dac.set_voltage(dutty_to_bits(dutty))
    return dutty

def execute_sleep(start_time, end_time, SAMPLE_TIME):
    elapsed_time = end_time - start_time
    if (elapsed_time < SAMPLE_TIME):
        time.sleep(SAMPLE_TIME-elapsed_time)

