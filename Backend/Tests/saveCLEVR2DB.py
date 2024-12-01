import Backend.clevr.CLEVR as clevr
import Backend.clevr.process_data as process

import Backend.config as conf

import pymongo
from pymongo import MongoClient

from Backend.GlobalController.Assistance import Assistance
from Backend.GlobalController.Instance import Instance
from Backend.GlobalController.Library import Library
from Backend.Resources.Mongodb import DatabaseConnector




date = "2023-04-21T11:50:33.416Z"
def test_updates_from_sandbox(date):
    databaseconnector = None
    assistance = None
    db = None
    try:
        db = MongoClient([conf.url_db], connectTimeoutMS=10000)[conf.db]
        print("[DB] Connected to online Database")
    except pymongo.errors.ConfigurationError:
        print("[DB] No connection to online Database")

    data = clevr.get_data_since_date(date)
    result = []
    process_list = []
    for entry in data:
        if entry["Size"] > 10000:
            result.append(clevr.get_data_uuid(entry['UUID']))
            process_list.append(process.process_data(db, clevr.get_data_uuid(entry['UUID'])))

    databaseconnector = DatabaseConnector(db)
    assistance = Assistance(conf.task_collection_name, use_clevr=True, model_path=conf.model_path,
                            db_connector=databaseconnector, use_adaptive_system=False)

    user_id_running = ""
    for pr in process_list:
        activities = pr.get_activities()

        user_id = pr.content['Sessions']['value'][0]['Session'][4]["AnonymousUser"][0]['Identifier']
        #user_id_test = pr.content['Sessions']['value'][0]['Session'][4]["AnonymousUser"][0]['Identifier']

        #if user_id_test == "6967044b-16ae-4f51-b3f2-3dbd606b7578" or user_id_test == "d29948b3-3af6-4a9e-a839-207dbeecacc7":
        user_id_test = "Tester_all"

        if True:
            print("Start Session "+pr.uuid+" for: "+ user_id)
            print("Performing " +str(len(activities))+ " Activity Steps")
            idx = 0
            for activity in activities:
                idx += 1

                input = activity['Activity']
                session_id = pr.uuid
                d = databaseconnector.data_transfer(input[0]['BPMNObject'][0]['ObjectId'])


                sequence = input[1]['Sequence']
                activity_id = input[0]['BPMNObject'][0]['ObjectId']
                called_help = input[2]['CalledForHelp']
                start = input[3]['StartDate']
                if 'EndDate' not in input[4]:
                    end = start
                    duration = input[4]['Duration']

                else:
                    end = input[4]['EndDate']
                    duration = input[5]['Duration']

                next = activity_id
                if idx == len(activities):
                    print(activity_id)
                else:
                    print(str(assistance.library.str_to_activity(activity_id).name)+"-->",  end="")

                add = {'Activity': [{'BPMNObject': [{'ObjectId': activity_id}]}, {'Sequence': str(sequence)},
                                    {'CalledForHelp': called_help},
                                    {'StartDate': start},
                                    {'EndDate': end},
                                    {'Duration': str(duration)},
                                    {'IdNext': next}
                                    ]}


                if assistance.user is None:
                    assistance.set_user_and_instance(user_id=user_id_test, instance_id=session_id)
                    user_id_running = user_id

                if user_id_running != user_id:
                    user_id_running = user_id
                    assistance.activities = []
                    assistance.library = Library(assistance.db[assistance.tasks_collection])
                    assistance.set_user_and_instance(user_id=user_id_test, instance_id=session_id)

                assistance.activities.append(add)

                assistance.assist_status, recommendation = assistance.update()

#test_updates_from_sandbox(date)

def test_instance_tester_all(user_name):
    databaseconnector = None
    assistance = None
    db = None
    try:
        db = MongoClient([conf.url_db], connectTimeoutMS=10000)[conf.db]
        print("[DB] Connected to online Database")
    except pymongo.errors.ConfigurationError:
        print("[DB] No connection to online Database")

    query = {"user": user_name}

    instances = db['instances'].find(query)

    databaseconnector = DatabaseConnector(db)
    assistance = Assistance(conf.task_collection_name, use_clevr=True, model_path=conf.model_path,
                            db_connector=databaseconnector, use_adaptive_system=False)

    session = ""
    for instance in instances:


        user_id = user_name
        #user_id_test = pr.content['Sessions']['value'][0]['Session'][4]["AnonymousUser"][0]['Identifier']

        #if user_id_test == "6967044b-16ae-4f51-b3f2-3dbd606b7578" or user_id_test == "d29948b3-3af6-4a9e-a839-207dbeecacc7":
        user_id_test = user_name

        if True:
            print("Start Session "+instance['UUID']+" for: "+ user_id)

            idx = 0
            for activity in instance['nodes_list']:
                idx += 1

                session_id = instance['UUID']
                node = instance['nodes'][activity]


                sequence = len(assistance.activities)
                activity_id = activity
                called_help = node['help']
                start = node['start']

                # if node['end'] not in node:
                #    end = start
                #    duration = input[4]['Duration']

#                else:
                end = node['end']
                duration = node['duration']


                activity_id_split = activity_id.split("_")


                activity_id = activity_id.split("_")[0] +"_" +activity_id.split("_")[1]
                next = activity_id


                add = {'Activity': [{'BPMNObject': [{'ObjectId': activity_id}]}, {'Sequence': str(sequence)},
                                    {'CalledForHelp': called_help},
                                    {'StartDate': start},
                                    {'EndDate': end},
                                    {'Duration': str(duration)},
                                    {'IdNext': next}
                                    ]}


                if assistance.user is None:
                    assistance.set_user_and_instance(user_id=user_id_test, instance_id=session_id)
                    user_id_running = user_id

                if user_id_running != user_id:
                    user_id_running = user_id
                    assistance.activities = []
                    assistance.library = Library(assistance.db[assistance.tasks_collection])
                    assistance.set_user_and_instance(user_id=user_id_test, instance_id=session_id)

                assistance.activities.append(add)

                assistance.update()


test_instance_tester_all("Tester_1")
#test_instance_tester_all("Tester_2")
