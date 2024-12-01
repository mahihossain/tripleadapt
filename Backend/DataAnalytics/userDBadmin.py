
from pymongo import MongoClient
import Backend.config as conf

def con_db(url, db):
    client = MongoClient(url)
    return client[db]

client = con_db(conf.url_db, conf.db)

coll = client['instances']
instances = coll.find({})

durations = []
acts = []
userdict = {}
user_list = []
for instance in instances:
    user = instance['user']
    user_list.append(user)
    user_iteration = user_list.count(user)
    activities = instance['nodes']
    inst_durs = []
    inst_acts = []
    for act in activities:
        activity_specs = activities[act]
        act_id = activity_specs['bpmn_obj']['id']
        duration = activity_specs['duration']
        inst_acts.append(act_id)
        inst_durs.append(duration)
    acts.append(inst_acts)
    durations.append(inst_durs)
    userdict[user, user_iteration] = [inst_acts, inst_durs, instance]

print(userdict['Ingo', 1][2])

activities_transformed=[]
seq = 0


db = MongoClient(conf.url_db)[conf.db]
users = db['user']
def update_user_to_db(userdict_key_user, instance_i):
    query = {'name': userdict_key_user}  # TODO id

    update = dict()

    update['name'] = userdict_key_user

    #update['id'] = user_obj.id
    #update['tasks_scores'] = user_obj.task_scores
    #update['tasks_levels'] = [l.name for l in user_obj.task_levels]

    old_user_info = users.find_one(query)

    if (old_user_info is None):
        update['history'] = []
    else:
        update['history'] = old_user_info['history']

    update['history'].append(instance_i)

    if (old_user_info is None):
        users.insert_one(update)
    else:
        users.replace_one(query, update, upsert=True)

#update_user_to_db('Ingo', userdict['Ingo', 1][2])

def convert(userdict_entry):
    seq = 0
    for activity in userdict_entry[0]:
        d = userdict_entry[1][seq]
        add = {'Activity': [{'BPMNObject': [{'ObjectId': activity}]}, {'Sequence': str(seq)},
                            {'CalledForHelp': 'false'}, {'StartDate': '2022-01-27T22:37:54.213Z'},
                            {'Duration': str(d)}]}
        seq += 1
        activities_transformed.append(add)
    return activities_transformed


Ingo1stinstance = convert(userdict["Ingo", 1])


