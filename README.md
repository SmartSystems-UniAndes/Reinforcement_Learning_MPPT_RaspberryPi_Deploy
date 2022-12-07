# Reinforcement_Learning_MPPT_RaspberryPi_Deploy
This is a project for research related to the applications of reinforcement learning towards global maximum power point tracking in photovoltaic systems. The code presented in python is meant to be used with a Raspberry Pi with the I2C protocol activated. This project is part 2 in deploying a Reinforcement Learning model into a Raspberry PI for maximum power point tracking. Part one can be found in the Github repository presented [here](https://github.com/SmartSystems-UniAndes/Train_and_Convert_RL_MPPT)

The next diagram shows the main idea of the deployment of the tensorflow lite models into the raspberry pi:

![diagrama_nuevo drawio](https://user-images.githubusercontent.com/49125155/206209593-8ed5bbd1-97da-4650-9f34-33caba923049.png)

## Install

To use this project, execute the following commands in your console after cloning the github repository:

The following two commands must be executed outside the directory:
```
python3 -m venv name_virtual_env
```
```
source name_virtual_env/bin/activate
```
The following commands must be executed inside the directory cloned:
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

| Type | License |
| :------: | --- |
| Software    | [MIT License](https://opensource.org/licenses/MIT)     |
| Hardware  | [CERN-OHL-P](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2)        |
| Documentation  | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)    |

### Software
The software is licensed under an [MIT License](https://opensource.org/licenses/MIT). A copy of the license has been included in the repository and can be found [here](https://github.com/jfgf11/Reinforcement_Learning_MPPT/blob/main/LICENSE-MIT.txt).

### Hardware
The hardware design files are licensed under a CERN Open Source Hardware license version 2 CERN-OHL-P. Details of the license can be found [here](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2) and a copy of the license has been included [here](https://github.com/jfgf11/Reinforcement_Learning_MPPT_RaspberryPi_Deploy/blob/main/LICENSE-CERN-OHL-P.txt).

### Documentation
![image](https://user-images.githubusercontent.com/49125155/205604437-01cdbdd8-6366-4861-b0d8-b9e25aec0f39.png)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

