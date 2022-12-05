# Reinforcement_Learning_MPPT_RaspberryPi_Deploy
This is a project for research related to the applications of reinforcement learning towards maximum power point tracking in photovoltaic systems. The code presented in python is meant to be used with a Raspberry Pi with the I2C protocol activated. This project is part 2 in deploying a Reinforcement Learning model into a Raspberry PI for maximum power point tracking. Part one can be found in the next repository:
https://github.com/jfgf11/Train_and_Convert_RL_MPPT

## Install

To use this project, execute the following commands in your console after cloning the github repository:

The following two commands must be executed outside the directory:
```
python3 -m venv name_virtual_env
```
```
source name_virtual_env/bin/activate
```
The following commands must be done inside the directory cloned:
```
pip3 install -r requirements.txt
```
```
pip3 install .
```

## RL Model tests TrackerMPPT.py

To test the created RL model and compare it against the P&O algorithm by plotting graphs at the end. The next code must be executed:
```
python3 TrackerMPPT.py
```
A tensorflow lite model must be present in the models folder to execute this script. The name of the file must start with the "DQN" as the examples present in the models folder. The variable number_DQN inside the TrackerMPPT.py file reference the last part of the name of the model that you want to use (the name after the DQN name part).

### Utils folder
The utils folder contains the Perturb and Obeserve algorithm and the DQN algorithm in the algorithms.py file. The functions.py file contains the functions used to extract the current and voltage measurements with the ADS1015. It also contains the code used to manipulate the TL4446 module with the MCP4725. The TL4446 needs to be characterized with an osciloscope to check what voltages accuratetly produce what duty cycles. You could also use the datasheet indications of the TL4446.

## PID

To run PID control of the buck converter execute the following command:

```
python3 PID.py
```

## Licenses

### Software
The software is licensed under an [MIT License](https://opensource.org/licenses/MIT). A copy of the license has been included in the repository and can be found [here](https://github.com/jfgf11/Reinforcement_Learning_MPPT/blob/main/LICENSE-MIT.txt).


