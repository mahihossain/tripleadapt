import random
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import multivariate_normal
import math

var1 = 1
var2 = 1
cov = 0.7
cov_matrix = [[var1, cov],
              [cov, var2]]

coefficients = np.random.multivariate_normal([0, 0], cov_matrix, size=10)
fig, ax = plt.subplots()
ax.scatter(coefficients[:,0], coefficients[:,1])
plt.show()

user_dur_list = []
for param in coefficients:
    dur_list = []
    learning_rate = 0.95 + param[1]*0.005
    start_value = 500 + param[0]*100
    for i in range(20):
        dur_list.append(start_value*learning_rate**(i*2)*random.normalvariate(1, 0.5*0.9**i))
    user_dur_list.append(dur_list)

skill_transfer_coeff = random.normalvariate(0.5, 0.2)



fig, ax = plt.subplots()
for list in user_dur_list:
    ax.plot(range(0, len(list)), list)
plt.show()




inst_list = []
for param in coefficients:
    initial_duration = 300 + 30 * param[0]
    NR_to_min = round(20 + 5 * param[1])
    #min = initial_duration / (3.5 - param[1])
    min = initial_duration / 2 + initial_duration / 20 * param[1]
    lrate = (min / initial_duration) ** (1 / NR_to_min)
    inst_list.append([initial_duration, NR_to_min, min, lrate])

print(inst_list)
#min = initial_duration * lrate ** (NR_to_min)

user_dur_list = []
for param in inst_list:
    print(param)
    dur_list = []
    learning_rate = param[3]
    start_value = param[0]
    for i in range(param[1]):
        dur_list.append(start_value*learning_rate**(i*2)*random.normalvariate(1, 0.1*0.9**i))
    user_dur_list.append(dur_list)

fig, ax = plt.subplots()
for list in user_dur_list:
    ax.plot(range(0, len(list)), list)
plt.show()


