from Backend.Tests.different_process_flows import activities_perfect_flow, activities_perfect_flow_tasks_cyclinder_eval

from Backend.GlobalController.Instance import Instance
import pymongo
from pymongo import MongoClient

import Backend.config as conf

import time


factor_milliseconds_to_seconds = 1000


try:
    if conf.inside_docker:
        db = MongoClient("mongodb://mongodb:27017")[conf.db]
    else:
        db = MongoClient()[conf.db]
except pymongo.errors.ConfigurationError:
    print("Problems with database connection for testing...")



def test_expert_run(assistance, db, instance_id=None, user_name=None, user_id=None, sleep=True):
    assistance.use_clevr = True
    if (user_id == None):
        assistance.set_user(-2, 'expert')
    else:
        assistance.set_user(user_id, user_name)

    assistance.instance = Instance(assistance.user, assistance.library,

                                   reference_model=assistance.model,
                                   activities=[],
                                   id=-1)
    seq = 0
    # load expert run from database
    # could also be the correct run '6206f3e8-04f8-47dc-ad09-c9ef7dbc551a' ]
    if (instance_id == None):
        expert_run = '1a2ad18f-d19b-469a-b0f0-00cf2d8893c1'
    else:
        expert_run = instance_id
    query = {"UUID": expert_run}
    inst = db['clevr'].find_one(query)
    nodes = inst['Sessions']['value'][0]['Session'][4]['Historys'][0]['History'][0]['Activitys']

    for item in nodes:
        activity = item['Activity'][0]['BPMNObject'][0]['ObjectId']
        # TODO problem: if activity was already visited, do not add it twice: either take max, first value, or add penalty
        if (seq == 40):
            d = (int(item['Activity'][4]['Duration']))
        else:
            d = (int(item['Activity'][5]['Duration']))

        add = {'Activity': [{'BPMNObject': [{'ObjectId': activity}]}, {'Sequence': str(seq)},
                            {'CalledForHelp': 'false'}, {
                                'StartDate': '2022-01-27T22:37:54.213Z'},
                            {'Duration': str(d)}]}
        seq += 1
        print(activity)

        assistance.assist_status = assistance.update([add])
        if sleep:
            time.sleep(d/factor_milliseconds_to_seconds)

    print("done")
    return assistance.instance


def test_perform_more_than_one_instance(assistance):
    assistance.use_clevr = True
    assistance.set_user(777, 'todayuser')

    assistance.instance = Instance(assistance.user, assistance.library,
                                   reference_model=assistance.model,
                                   activities=[],
                                   id=-1)
    seq = 0
    for activity in activities_perfect_flow_tasks_cyclinder_eval:
        d = 12
        add = {'Activity': [{'BPMNObject': [{'ObjectId': activity}]}, {'Sequence': str(seq)},
                            {'CalledForHelp': 'false'}, {
                                'StartDate': '2022-01-27T22:37:54.213Z'},
                            {'Duration': str(d)}]}
        seq += 1
        assistance.activities = [add]

        assistance.assist_status = assistance.update(False)

        time.sleep(1)
        print(activity)

    print("first round completed")

    #for activity in activities_perfect_flow:
        # TODO: create a test to add a new activity to the instance and only send the update to the frontend.
     #   add = {'Activity': [{'BPMNObject': [{'ObjectId': activity}]}, {'Sequence': str(seq)},      {'CalledForHelp': 'false'}, {
      #      'StartDate': '2022-01-27T22:37:54.213Z'},
       #     {'Duration': '0'}]}
        #seq += 1

        #assistance.update([add])

       # time.sleep(1)

