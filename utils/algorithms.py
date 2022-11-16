import numpy as np
import time

VMP = 30.3
Pmmtstc = 250.49
action_space = [-0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03] 
dDutty_PYO = 0.03


def RL_Algorithm(last_power, last_voltage, power, voltage, dDutty, interpreter):
    
    dV = (voltage-last_voltage)/VMP
    dP = (power-last_power)/Pmmtstc

    results = []
    y_likelihoods_tflite = []



    interpreter.allocate_tensors()


    # Following this, the index of the model's input and output nodes are extracted from the interpreter. These are used to feed input images into the model, and save likelihoods from the output nod
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_index = input_details[0]['index']
    output_index = output_details[0]['index']
    start_rl = time.time()
    for i in action_space:
        
        x1 = np.float32(np.array([[i]])) 
        x2 = np.float32([[dP,dV,dDutty]])

        # Explicitly set input tensor
        interpreter.set_tensor(input_details[0]['index'], x1)
        interpreter.set_tensor(input_details[1]['index'], x2)


        # Free up numpy reference to internal tensor, then invoke
        interpreter.invoke()

        # Explicitly get the value stored within the output tensor
        y_softmax_tflite = interpreter.get_tensor(output_index)

        y_likelihoods_tflite.extend(y_softmax_tflite)

        results.append(y_softmax_tflite)
    end_rl = time.time()
    times_rl = end_rl-start_rl
    
    deltaD = action_space[np.argmax(results)]

    return deltaD, times_rl


def PYO(last_power, last_voltage, power, voltage, Dprev):
    if (power-last_power != 0):
        if (power-last_power > 0):
            if ((voltage-last_voltage)>0):
                D=Dprev-dDutty_PYO
            else:
                D=Dprev+dDutty_PYO
        else:
            if ((voltage-last_voltage) > 0):
                D=Dprev+dDutty_PYO
            else:
                D=Dprev-dDutty_PYO
    else:
        D=Dprev
    return D