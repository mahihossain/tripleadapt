import Backend.config as conf
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import numpy as np
from Backend.GlobalController.Library import Library
db = 'tripleadapt'

"""
class DatabaseConnectorV2:

    def connect_db(self, url, db):
        client = MongoClient(url)
        return client[db]

    def __init__(self,db):
        self.users = db[0]
        self.instances = db[1]

conn = DatabaseConnectorV2(conf.db)

client = conn.connect_db(conf.url_db, conf.db)
"""

def con_db(url, db):
    client = MongoClient(url)
    return client[db]

client = con_db(conf.url_db, conf.db)


coll = client['clevr']

from Backend.Resources.Model import Model
#model = Model(conf.model_path, client, Library(db['tasks']))

query = {"UUID": '15d0bef8-4123-4d18-afc8-65d90956f8cd'}
# {"UUID": '15d0bef8-4123-4d18-afc8-65d90956f8cd'}
inst = coll.find({})
activities = inst[0]['Sessions']['value'][0]['Session'][5]['Historys'][0]['History'][0]['Activitys']
LAct = dict()
j = 0
i = 0;
for instance in inst:
    activity = instance['Sessions']['value'][0]['Session'][5]['Historys'][0]['History'][0]['Activitys']
    for act in activity:

        bpnm = act['Activity'][0]
        sequencenumber = act['Activity'][1]['Sequence']
        help = act['Activity'][2]['CalledForHelp']
        startdate = act['Activity'][3]['StartDate']
        enddate = act['Activity'][4]['EndDate']
        duration = act['Activity'][5]['Duration']
        LAct[i]= [int(duration), help, sequencenumber, bpnm, j]
        i = i+1
    j = j+1

dfdict = pd.DataFrame.from_dict(LAct, orient='index')
dfdict.columns = ['duration', 'help', 'sequencenr', 'bpmn', 'instancenr']
dfdict["repeatcumsum"] = (dfdict["bpmn"] == dfdict["bpmn"].shift()).cumsum()

print(dfdict.keys())
print(dfdict)

#for i in self.df['instancenr'].unique():
#    l.append(self.df.loc[df['instancenr'] == i])


# following lists in order of first appearance of task -> drop duplicates logic
taskavg = [] #avg duration of all tasks in a list
taskdur = [] #list of lists with with duration of specific task in a list for all tasks
taskdur_nrObs = [] #list of lengths of lists in taskdur
tasks = list(dfdict['bpmn'].drop_duplicates())
for task in tasks:
    task_dur_l = list(dfdict['duration'].loc[dfdict['bpmn'] == task])
    taskdur.append(task_dur_l)

    taskdur_nrObs.append(len(task_dur_l))

    avg = sum(task_dur_l)/len(task_dur_l)
    taskavg.append(avg)



"""
#all tasks in one graph
fig, ax = plt.subplots()
for task in tasks:
    ax.plot(list(range(0, len(taskdur[tasks.index(task)]))), taskdur[tasks.index(task)])
plt.show()

print(len(tasks))
print(tasks)
print(taskdur)
print(taskdur_nrObs.index(max(taskdur_nrObs)))

#neccesary to find index of desired task and call via that
desired_tasks = [14,0,6]
fig, ax = plt.subplots()
for i in desired_tasks:
    ax.plot(list(range(0, len(taskdur[i]))), taskdur[i])
plt.show()

from scipy.stats import norm

#Activity duration statistics
index_of_desired_task_in_tasks = 14
i = index_of_desired_task_in_tasks
fig, ax = plt.subplots()
a = np.array(taskdur[i])
ax.hist(a)
mean = a.mean()
std_dev = a.std()
ax.axvline(mean, ymin=0, ymax=max(taskdur[i]), color='red')
ax.axvline(mean+std_dev, ymin=0, ymax=max(taskdur[i]), color='magenta')
ax.axvline(mean-std_dev, ymin=0, ymax=max(taskdur[i]), color='magenta')
dist = norm(mean, std_dev)
values = [value for value in range(int(float(mean)-2*float(std_dev)), int(float(mean)+2*float(std_dev)))]
probs = [dist.pdf(value)*mean for value in values]
ax.plot(values, probs)
plt.show()


print(list(dfdict['repeatcumsum']))
print(list(dfdict['help']))
print(list(dfdict['bpmn']))

print(list(dfdict['instancenr']))
print(list(dfdict['sequencenr']))


#new column if help called = 1
def f(row):
    if row['help'] == 'false':
        val = 0
    else:
        val = 1
    return val
dfdict['counter'] = dfdict.apply(f, axis=1)

#list of help calls per instance (personal progress)
nr_help_calls = []
for i in range(max(dfdict['instancenr'])+1):
    nr = sum(list(dfdict['counter'].loc[dfdict['instancenr'] == i]))
    nr_help_calls.append(nr)
inr = list(range(0, max(dfdict['instancenr'])+1))
fig, ax = plt.subplots()
ax.scatter(inr, nr_help_calls)
plt.show()

#Nr of help called per activity
tasks = list(dfdict['bpmn'].drop_duplicates())
mistake_per_activity_type = []
for activity in tasks:
    NR_mistakes = sum(list(dfdict['counter'].loc[dfdict['bpmn'] == activity]))
    mistake_per_activity_type.append(NR_mistakes)
print(mistake_per_activity_type)
c = [*range(1, len(mistake_per_activity_type+1), 1)]
fig, ax = plt.subplots()
ax.bar(c, mistake_per_activity_type)
plt.show()

#ps.plot(dfdict['duration'])

#ps.show()
"""

"""
for stuff in inst:
    print(stuff['Sessions']['value'][0]['Session'][5]['Historys'][0]['History'][0]['Activitys'])
"""

#history = Instance(db=client, activities=activities)
#history.graph
"""
print(inst[2])
print(inst[2]["Sessions"])
print(inst[2]["Sessions"]["value"])
print(inst[2]['Sessions']['value'][0]['Session'][5]['Historys'][0]['History'][0]['Activitys'])
"""
#print(activities)