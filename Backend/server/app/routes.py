from datetime import datetime, timedelta

import pymongo
from flask import request
from pymongo import MongoClient

from Backend.GlobalController.Assistance import Assistance
from Backend.GlobalController.Instance import Instance
from Backend.GlobalController.Library import Library
from Backend.GlobalController.replay_page import replay_page, stop_processing, start_processing_again, \
    load_instance_replay
from Backend.Resources.Mongodb import DatabaseConnector
from Backend.Tests.recommendation_test import test_perform_more_than_one_instance, test_expert_run
from Backend.server.app import app
import Backend.clevr.CLEVR as clevr
import Backend.config as conf
import json
import sched
import time
import threading
import traceback

from Backend.DataAnalytics.Graphic import GraphicsConstructor
from Backend.DataAnalytics.UserList import UserListConstructor

thrd = None
db = None
try:
    db = MongoClient([conf.url_db], connectTimeoutMS=10000)[conf.db]
    print("[DB] Connected to online Database")
except pymongo.errors.ConfigurationError:
    print("[DB] No connection to online Database")

databaseconnector = DatabaseConnector(db)
assistance = Assistance(conf.task_collection_name, use_clevr=True, model_path=conf.model_path,
                        db_connector=databaseconnector, use_adaptive_system=False)

# assistance = Assistance(db, 'tasks_simulation1', model_path=conf.model_path,
#                         db_connector=databaseconnector)


IS_VIRTUAL = False

# @app.route("/Data2Text", methods=["GET", "POST"])
# def data2text():
#     print('-------------------')
#     print(request.json['modelId'])
#     Model2Text().data2text(request.json['modelId'])
#     return 'Hat geklappt'


@app.route("/dummy")
def is_connected():
    print("dummy")
    return "Dummy"


@app.route("/retry")
def retry():
    return databaseconnector.retry()


@app.route("/model", methods=["GET"], strict_slashes=False)
def send_model():
    return assistance.model.model2JSON()

# virtual score - > berechnung


@app.route("/task", methods=["GET", "POST"], strict_slashes=False)
def get_task():
    # request = {}

    # request.json['time'] = 12
    # request.json['error'] = False
    # request.json['activityId'] = 'Activity_0h4egt6'

    print(request.json['activityId'])
    print(request.json['time'])
    print(request.json['error'])

    # nächster schritt: ActivityId: 1, TaskScore_Diffult : MEDIUM, finish = True
    # Finish

    assistance.instance = Instance(assistance.user, assistance.library, reference_model=assistance.model,
                                   activities=[],
                                   id=-1, is_virtual=True)
    seq = 0
    activities_transformed = []
    d = int(request.json['time'])
    activity = request.json['activityId']
    add = {'Activity': [{'BPMNObject': [{'ObjectId': activity}]}, {'Sequence': str(seq)},
                        {'CalledForHelp': 'false'}, {
                            'StartDate': '2022-01-27T22:37:54.213Z'},
                        {'Duration': str(d)}]}
    seq += 1
    activities_transformed.append(add)
    assistance.instance.set_activities_done(activities_transformed)
    assistance.instance.update(assistance.user)

    # what is send back

    # get the next activity id
    current_activity = assistance.library.str_to_activity(
        request.json['activityId'])
    print(assistance.library.get_final_activity_id())
    print(current_activity.id)

    if (not current_activity.is_correct()):
        next_activity = current_activity.jump_back().id
        name_activity = current_activity.jump_back().name

    else:

        next_activity = assistance.library.get_successor(current_activity).id
        name_activity = assistance.library.get_successor(current_activity).name

    is_last = assistance.library.get_final_activity_id() == next_activity

    task = assistance.library.activity_to_task(current_activity)
    difficulty = str(assistance.user.task_levels[task.id])

    result = {"Next_activity_id": next_activity,
              "Next_activity_name": name_activity, "is_last": is_last, "level": difficulty}
    print(result)
    return result


@app.route("/user", methods=["GET"], strict_slashes=False)
def send_user_list():
    constructor = UserListConstructor(databaseconnector.local_db)
    outputjson = constructor.UserList()
    print(outputjson)
    return outputjson


@app.route("/start_replay_page", methods=["GET", "POST"])
def start_replay_page():
    assistance.do_assist = True
    timestamp = request.json['timestamp']
    user_name = request.json['user']
    print(timestamp)

    assistance.set_user(user_id=user_name, user_name=user_name)

    nodes_id, nodes_values, current_start_activity = load_instance_replay(
        assistance, db,  assistance.user.start_dates[timestamp], user_name, user_name)
    replay_page(assistance, nodes_id, nodes_values, current_start_activity)

    return "Thread Started (replay page)"


@app.route("/stop_replay_page", methods=["GET", "POST"])
def stop_replay_page():
    stop_processing()
    return "Thread Stopped"


@app.route("/continue_replay_page", methods=["GET", "POST"])
def continue_replay_page():
    start_processing_again(None)
    return "continue"


@app.route("/start", methods=["GET", "POST"])
def start():
    assistance.do_assist = True
    thrd = threading.Thread(target=send_data, daemon=True)
    thrd.start()
    return "Thread Started"


@app.route("/stop", methods=["GET", "POST"])
def stop():
    assistance.do_assist = False
    if thrd is not None:
        thrd.join()
    return str(assistance.assist_status)


@app.route("/status", methods=["GET", "POST"])
def send_status():
    # return {'nodes': [{'name': 'Kolbenstange messen', 'bpmn_obj': {'type': 'userTask', 'process': 'Process_1', 'id': 'Activity_1pv3djb', 'name': 'Kolbenstange messen', 'incoming': ['Flow_0gt6359'], 'outgoing': ['Flow_1ub4xyw'], 'material': 'Kolbenstange'}, 'sequence': 29, 'help': 'false', 'start': '2022-10-04T12:25:05.189Z', 'end': 'not defined', 'duration': '0', 'task': 5, 'action_ok': True, 'task_score': 'DIFFICULT'}], 'edges': [{'from': 'Activity_06jmsg8', 'to': 'Activity_1pv3djb'}], 'subgraph_task': {'task_id': 5, 'task_name': 'Kolbenstange', 'nodes': [{'type': 'userTask', 'id': 'Activity_06jmsg8', 'name': 'Kolbenstange bereitlegen', 'material': 'Kolbenstange', 'task': 5, 'correct': True}, {'type': 'serviceTask', 'id': 'Activity_037gp20', 'name': 'Kolbenstange bereitlegen', 'material': 'Kolbenstange', 'task': 5, 'correct': True}, {'type': 'userTask', 'id': 'Activity_1pv3djb', 'name': 'Kolbenstange messen', 'material': 'Kolbenstange', 'task': 5, 'correct': True}, {'type': 'userTask', 'id': 'Activity_1sruu4d', 'name': 'Falscher Pick', 'material': 'Kolbenstange', 'task': 5, 'correct': False}, {'type': 'userTask', 'id': 'Activity_06zvj0k', 'name': 'Kolbenstange ok', 'material': 'Kolbenstange', 'task': 5, 'correct': True}, {'type': 'userTask', 'id': 'Activity_1fjlefr', 'name': 'Kolbenstange nicht ok', 'material': 'Kolbenstange', 'task': 5, 'correct': False}], 'edges': [{'from': 'Activity_06jmsg8', 'to': 'Activity_1pv3djb'}, {'from': 'Activity_06jmsg8', 'to': 'Activity_1sruu4d'}, {'from': 'Activity_037gp20', 'to': 'Activity_06jmsg8'}, {'from': 'Activity_1pv3djb', 'to': 'Activity_06zvj0k'}, {'from': 'Activity_1pv3djb', 'to': 'Activity_1fjlefr'}, {'from': 'Activity_1sruu4d', 'to': 'Activity_06jmsg8'}, {'from': 'Activity_06zvj0k', 'to': 'Activity_19eo8f7'}, {'from': 'Activity_1fjlefr', 'to': 'Activity_06jmsg8'}]}}
    return assistance.assist_status


@app.route("/data", methods=["GET", "POST"], strict_slashes=False)
def send_data():
    input = {}
    if request.json is None:
        input = json.loads(request.get_data())
    else:
        input = request.json
    d = databaseconnector.data_transfer(input['BPMNActivityID'])

    user_id = input['UserID']

    if assistance.user is not None:
        user_id = assistance.user.name


    # sollte das selbe wie uuid sein ungefähr
    session_id = input['SessionID']
    sequence = input['Sequence']
    activity_id = input['BPMNActivityID']
    called_help = input['CalledForHelp']
    start = input['StartDate']
    end = input['EndDate']
    duration = input['Duration']

    next = None
    if 'BPMNActivityIDNext' in input:
        next = input['BPMNActivityIDNext']
    '''/

        if next in assistance.new_to_old.keys():
            next = assistance.new_to_old[next]
    else:
        next = None

    assistance.set_user_and_instance(user_id, session_id)
    id = activity_id
    if activity_id in assistance.new_to_old.keys():
        id = assistance.new_to_old[activity_id]
    /'''

    add = {'Activity': [{'BPMNObject': [{'ObjectId': activity_id}]}, {'Sequence': str(sequence)},
                        {'CalledForHelp': called_help},
                        {'StartDate': start},
                        {'EndDate': end},
                        {'Duration': str(duration)},
                        {'IdNext': next}
                        ]}

    if assistance.instance is None:
        assistance.set_instance(is_virtual=IS_VIRTUAL, instance_id=session_id)


    if assistance.user is None:
        assistance.set_user_and_instance(
            user_id=user_id, is_virtual=IS_VIRTUAL,  instance_id=session_id)
    elif assistance.user.name != user_id:
            assistance.activities = []
            assistance.library = Library(
                assistance.db[assistance.tasks_collection])
            assistance.set_user_and_instance(
                user_id=user_id,is_virtual=IS_VIRTUAL,  instance_id=session_id)

    assistance.activities.append(add)

    try:
        assistance.assist_status = assistance.update()

       # for node in recommendation['nodes']:
       #     node['bpmn_obj']['id'] = activity_id

        print(assistance.assist_status['nodes'][len(
            assistance.assist_status['nodes']) - 1])
        return assistance.assist_status['nodes'][len(assistance.assist_status['nodes']) - 1]
    except:
        print("ERROR")
        traceback.print_exc()
        return "[]"


@app.route("/statistics", methods=["GET", "POST"])
def send_statistics():
    outdict = {}
    graphlist = request.json["DataID"]
    id = request.json['userId']
    #assistance.set_user(id, id)

    if not assistance.user.history:
        return "[]"

    if assistance.user.role is not None:
        if assistance.user.role == "admin":
            result = databaseconnector.data_transfer(databaseconnector.user_all.id)
        else:
            result = databaseconnector.data_transfer(assistance.user.id)
    else:
        result = databaseconnector.data_transfer(assistance.user.id)

    if result is not None:
        for graph in graphlist:
            outdict[graph] = result[graph]
    return outdict


@app.route("/register", methods=["GET", "POST"])
def register():

    id = request.json['username']
    pw = request.json['password']
    role = request.json['role']

    print('------------')
    print('id: ', id)
    print('pw: ', pw)
    print('role: ', role)

    user = databaseconnector.create_user(id, id, assistance.library, assistance.score_calulator, pw=pw, role=role)
    assistance.set_user(id, id)
    return {'id': user['id'], 'name': user['name'], 'password': user['password'], 
                'role': user['role'], 'difficulty': user['tasks_levels'][0]}


@app.route("/login", methods=["GET", "POST"])
def login():

    id = request.json['username']
    pw = request.json['password']

    print('----------------------')
    print('id: ', id)

    query = {"id": id}
    user = databaseconnector.users.find_one(query)

    if user is None:
        return "False"

    print('userName: ', user['name'])
    print('userId: ', user['id'])


    if user['password'] == pw:
        assistance.set_user(id, id)
        # print('user: ', user)
        return {'id': user['id'], 'name': user['name'], 'password': user['password'], 
                'role': user['role'], 'difficulty': user['tasks_levels'][0]}
    return "False"


# test()
# start_replay_page()
# time.sleep(6)  # Wait for 5 seconds
# stop_replay_page()
# time.sleep(5)

# time.sleep(3)  # Wait for 5 seconds
# stop_replay_page()
# time.sleep(20)

# Then call start_processing_again to continue where it left off or restart with new parameters
# Wait for another 5 seconds
# start_processing_again(None)
# start_processing_again(new_activity_id=5)
#
# get_task()
# send_model()
# send_graphics()
# send_user_list()
# get_permission()
# start()
# stop()
# send_status()
# send_data()
