from pymongo import MongoClient
import Backend.config as conf
import pandas as pd


name = 'Ingoi'

def con_db(url, db):
    client = MongoClient(url)
    return client[db]

client = con_db(conf.url_db, conf.db)
coll = client['user']
stuff = coll.find({})
doc = coll.find_one()

l = 0

user_dict = dict()
c = 0
name = "Ingoi"
for i in stuff[0]['history']:
    r = i['nodes']
    g = 0
    iteration = c
    for node in r:
        j = r[node]
        task_NR = g
        act_name = j['name']
        act_id = j['bpmn_obj']['id']
        help = j['help']
        duration = j['duration']
        user_dict[l] = [act_name, act_id, help, duration, task_NR, iteration, name]
        g = g + 1
        l = l+1
    c = c + 1

dfdict = pd.DataFrame.from_dict(user_dict, orient='index')
dfdict.columns = ['act_name', 'act_id', 'help', 'duration', 'task_NR', 'iteration', 'name']

tasks_id = list(dfdict['act_id'].drop_duplicates())
tasks_name = list(dfdict['act_name'].drop_duplicates()) #same order as tasks_id

dict_of_task_dur_lists = {}
for task in tasks_name:
    task_duration_list = list(dfdict['duration'].loc[dfdict['act_name'] == task]) #list of all observed durations of a specific task
    dict_of_task_dur_lists[task] = task_duration_list

def histogram(list_of_durs, bins):
    bin_entry_list = []
    bin_size = (max(list_of_durs) - min(list_of_durs)) / bins
    bin_dict = {}
    bin_list = []
    for nr in range(bins):
        bin_dict[min(list_of_durs) + bin_size*(nr+1)] = 0
        bin_list.append(min(list_of_durs) + bin_size*(nr+1))
    for dur in list_of_durs:
        c = 0
        for bin in bin_dict:
            if dur << bin_dict[bin]:
                bin_dict[bin_list[c]] = bin_dict[bin_list[c]] + 1
            c = c + 1
    return bin_dict

def task_avg_stdDev_var(list_of_durs):
    avg = sum(list_of_durs) / len(list_of_durs)
    list = []
    for dur in list_of_durs:
        list.append((dur-avg)**2)
    var = sum(list) / len(list)
    stdDev = var ** (1/2)
    results= {}
    results["avg"] = avg
    results['var'] = var
    results['stdDev'] = stdDev
    return results



