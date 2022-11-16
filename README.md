# Reinforcement_Learning_MPPT
This is a project for research related to the applications of reinforcement learning towards maximum power point tracking in photovoltaic systems. The code presented in python is meant to be used with a Raspberry Pi.

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

### PID

To run PID control of the buck converter execute the following command:

```
python3 PID.py
```
