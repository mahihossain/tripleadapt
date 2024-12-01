from pymongo import MongoClient
import Backend.config as conf
import matplotlib.pyplot as plt
import numpy as np
import json
def con_db(url, db):
    client = MongoClient(url)
    return client[db]

client = con_db(conf.url_db, conf.db)


false_act_list = []
coll = client['tasks']  #TODO do this over the libary class
tasks = coll.find({})
for i in tasks:
    for j in i['steps']:
        if j['ok'] == False:
            false_act_list.append(j['id'])

print(false_act_list)


coll = client['user']
user = coll.find({})
j = 0;
dact = {}

user_list = []

for person in user:
    name = person['name']
    user_list.append(name)

relevant_user = 'Ingoi'
index_of_relevant_user = user_list.index(relevant_user)

coll = client['user']
user = coll.find({})

for i in user[index_of_relevant_user]['history']:
    #iteration over all activity sequences for that user
    nodes = i['nodes_list']
    dact[j] = nodes
    if j == 0:
        print(nodes)
    j = j+1

error = []
for i in dact.keys():
    failure_array = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
    for j in dact[i]:
        if j in false_act_list:
            v = false_act_list.index(j)
            failure_array[v] = failure_array[v] + 1
    error.append(failure_array)

#error list of arrays hat nummer des Durchlaufs der Person als index. Sie enthält arrays, die an index 1 die NR von Fehlern der
#Activität wie sie in der failure_act_list an index 1 steht enthält usw.
#turn into numpy array???
d = dict()
i = 0
for a in error:
    d[i] = int(a[8])
    i = i+1
out = json.dumps(d)
print(out)

#visualization errors auf person bezogen für mehrere Durchläufe

error_durchläufe = []
for a in error:
    error_durchläufe.append(a[8])
print(len(error_durchläufe))
fig, ax = plt.subplots()
ax.scatter(range(len(error_durchläufe)), error_durchläufe)
plt.show()












