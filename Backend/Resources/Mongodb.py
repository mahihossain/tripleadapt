import networkx as nx
import pymongo
from pymongo import MongoClient
import Backend.config as conf

from Backend.GlobalController.ScoreCalculator import Level
from Backend.GlobalController.User import User
import socket
import time
import schedule
import threading
from Backend.DataAnalytics.Graphdata import Graphdata

import numpy


class DatabaseConnector:

    def __init__(self, db):

        self.online_db = db
        self.user_id = None
        # create local db to work with
        # Connect to MongoDB Container
        if conf.inside_docker:
            self.local_db = MongoClient("mongodb://mongodb:27017")[conf.db]
            try:
                # Check internet connection
                socket.create_connection(("www.google.com", 80))
                self.backup_db = MongoClient(conf.url_db)["tripleadapt"]
            except Exception as e:
                print("Could not upload data. Error:", e)

            # start scheduled Thread
            schedule.every().hour.do(self.daily_task)

            thread = threading.Thread(target=self.run_schedule)
            thread.start()
        elif conf.stay_online_db:
            self.local_db = db
            self.online_db = None
        else:
            self.local_db = MongoClient()[conf.db]

        if db is not None:
            self.users = db['user']
            self.instances = db['instances']
            self.meta_data = db['meta_data']
            # load online db, if exists into local one (or just update existing collections)
        else:
            self.users = self.local_db['user']
            self.instances = self.local_db['instances']
            self.meta_data = self.local_db['meta_data']

        self.load_db(self.online_db, self.local_db)
        self.user_all = None



    def save_progress(self, assistance, is_finished):

        self.update_user_to_db(assistance.user, assistance.instance, assistance.score_calulator,is_finished)
        self.update_user_to_db(self.user_all, assistance.instance, assistance.score_calulator,is_finished)


        if is_finished:
            #TODO
            self.save_instance_to_db(assistance.instance, assistance.score_calulator)
            self.userdb_dataupdate(assistance.user.id)
            self.userdb_dataupdate(self.user_all.id)


    def save_instance_to_db(self, instance, score_calculator):
        query ={"UUID": instance.id}
        self.instances.replace_one(query, instance.prepare_dict(score_calculator), upsert=True)

    def update_next_id(self):
        query_next_id = {"name": "next_free_id"}
        next_free_id = self.meta_data.find_one(query_next_id)
        update = dict()
        update['name'] = next_free_id['name']
        update['id'] = next_free_id['id'] + 1

        #self.meta_data.replace_one(query_next_id, update, upsert=True)
        self.replace_one_query("meta_data", query_next_id, update)


    def load_boarders(self, score_calculator):
        query = {"name": "score_boarders"}
        current_boarders = self.meta_data.find_one(query)["boarders"]


        score_calculator.MAXHARD_pertask = numpy.array(current_boarders["MAXHARD_pertask"])
        score_calculator.MAXLOW_pertask=    numpy.array(      current_boarders["MAXLOW_pertask"])
        score_calculator.MAXMEDIUM_pertask=  numpy.array(  current_boarders["MAXMEDIUM_pertask"])
        score_calculator.MINLOW_pertask =  numpy.array( current_boarders["MINLOW_pertask"])
        score_calculator.failure_easy =  current_boarders["failure_easy"]
        score_calculator.failure_middle =  current_boarders["failure_middle"]
        score_calculator.failure_hard =  current_boarders["failure_hard"]

        return

    def save_boarders(self, score_calculator):
        query = {"name":"score_boarders"}
        score_boarders = self.meta_data.find_one(query)
        update = dict()
        update["name"] = score_boarders["name"]
        update["boarders"] = self.return_boarders_used(score_calculator)
        self.replace_one_query("meta_data", score_boarders, update)

    def return_boarders_used(self, score_calculator):
        update = dict()
        update["MAXHARD_pertask"] = score_calculator.MAXHARD_pertask.tolist()
        update["MAXLOW_pertask"] = score_calculator.MAXLOW_pertask.tolist()
        update["MAXMEDIUM_pertask"] = score_calculator.MAXMEDIUM_pertask.tolist()
        update["MINLOW_pertask"] = score_calculator.MINLOW_pertask.tolist()
        update["failure_easy"] = score_calculator.failure_easy
        update["failure_middle"] = score_calculator.failure_middle
        update["failure_hard"] = score_calculator.failure_hard
        return update


    def create_user(self, id, name, library, score_calculator, pw, role="default"):

        task_scores = [0] * (library.number_tasks + 1)
        query_next_id = {"name": "next_free_id"}
        # TODO nochmal einbauen aber weiter vorne wegen tests
        next_free_id = self.meta_data.find_one(query_next_id)['id']

        # TODO: proof
        task_levels = [Level.LOW] * (library.number_tasks + 1)
        if name == "Not provided":
            name = id
        user_obj = User(id, name, task_scores,
                        score_calculator, task_levels, library, history=None, role=role)

        self.update_next_id()
        update = dict()
        update['name'] = user_obj.name
        update['id'] = id
        update['password'] = pw
        update['role'] = role
        update['tasks_scores'] = user_obj.task_scores
        update['tasks_levels'] = [l.name for l in user_obj.task_levels]
        update['history'] = []
        update['statistical_data'] = self.initialize_statistical_data(user_obj)
        update['boarders_used'] = self.return_boarders_used(score_calculator)

        query = {"id": id}
        self.replace_one_query("user", query, update)
        return self.users.find_one(query)

    def load_user_from_db(self, id, name, library, score_calculator):

        query = {"id": id}
        user = self.users.find_one(query)

        # create new user in database
        if user is None:
            user_obj = self.create_user(id, name, library, score_calculator, pw=None)
            print("Created a user out of nowhere!")
        else:
            #TODO this should not be necessary after next evaluation anymore, until now, we have fixed boarders

            user['boarders_used'] =self.return_boarders_used(score_calculator)



            user_obj = User(user['id'], user['name'], user['tasks_scores'], score_calculator, [
                            Level[l] for l in user['tasks_levels']], library, user['history'],
                            user['statistical_data'], user['boarders_used'], pw=user['password'], role = user['role'])

        return user_obj

    def compute_new_statistics(self, statistics_old, size_old_history, user_obj, failure_rate):

        statistics_new = []
        statistics_new.append(0)
        for taskState in user_obj.tasks_states:
            if (failure_rate):
                statistics_new.append(taskState.failure_rate)
            else:
                statistics_new.append(taskState.time)

        avg_result = []
        for i in range(len(statistics_new)):
            old = statistics_old[i]
            new = statistics_new[i]

            avg_result.append(size_old_history/(size_old_history + 1)
                              * old + 1 / (size_old_history + 1)*new)

        return avg_result

    # must be created before this

    #must be created before this
    def update_user_to_db(self, user_obj, instance, score_calculator, is_finished):

        query = {'id': user_obj.id}

        update = dict()

        update['name'] = user_obj.name

        if user_obj.name == "Not provided":
            update['name'] = user_obj.id
        update['id'] = user_obj.id

        update['password'] = user_obj.pw
        update['role'] = user_obj.role
        update['tasks_scores'] = user_obj.task_scores
        update['tasks_levels'] = [l.name for l in user_obj.task_levels]

        old_user_info = self.users.find_one(query)

        #TODO pervious cases not needed ! need to be covered in one place->load_user_from_db

        old_size_of_history = len( old_user_info['history'])
        update['history'] = old_user_info['history']
        update['statistical_data'] = old_user_info['statistical_data']

        #TODO discuss this boarders always the same for a user or not?
        update['boarders_used'] = old_user_info['boarders_used']


        if is_finished:
            old_statistical_data = old_user_info['statistical_data']

            statistics = update['statistical_data'] = {}

            statistics['avg_failure_rate_per_task'] = self.compute_new_statistics(old_statistical_data['avg_failure_rate_per_task'],  old_size_of_history, user_obj, failure_rate=True)
            statistics['avg_duration_per_task'] = self.compute_new_statistics(old_statistical_data['avg_duration_per_task'],old_size_of_history, user_obj, failure_rate=False)

        instance_dict = instance.prepare_dict(score_calculator)
        is_first_element = len(instance_dict['nodes']) == 1

        if is_first_element or update['history'] == []:
            update['history'].append(instance_dict)
        else:
            update['history'][-1] = instance_dict


        self.replace_one_query("user", query, update)

    def initialize_statistical_data(self, user_obj):


        avg_failure_rate_per_task = []
        avg_duration_per_task = []
        avg_failure_rate_per_task.append(0)
        avg_duration_per_task.append(0)

        for taskState in user_obj.tasks_states:
            avg_failure_rate_per_task.append(taskState.failure_rate)
            avg_duration_per_task.append(taskState.time)

        data = {}

        data['avg_failure_rate_per_task'] = avg_failure_rate_per_task
        data['avg_duration_per_task'] = avg_duration_per_task
        return data

    # TODO not used currently, not working perfectly

    def load_instance_from_db(self, instance):
        query = {"UUID": instance.id}
        inst_dict = {}
        inst = self.instances.find_one(query)
        graph = nx.DiGraph()
        id = inst['UUID']
        date = inst['StartDate']
        username = inst['user']

        nodes = inst['nodes_list']
        node_obj = inst['nodes']

        inst_dict['UUID'] = id
        inst_dict['StartDate'] = date
        inst_dict['user'] = username
        d_nodes = []
        for item in nodes:
            node = node_obj[item]
            d_nodes.append(node)
            seq = node['sequence']
            h = node['help']
            s = node['start']
            e = node['end']
            d = node['duration']
            bpmn_object = node['bpmn_obj']
            n = bpmn_object['name']
            graph.add_node(item, name=n, bpmn_obj=bpmn_object, sequence=seq, help=h,
                           start=s, end=e, duration=d)

        inst_dict['nodes'] = d_nodes
        edges = []
        for edge in inst['edges']:
            edges.append((edge['from'], edge['to']))
        graph.add_edges_from(edges)
        inst_dict['edges'] = edges

       # instance = Instance (library,reference_model , activities, id, date, username )
        return instance

    """
    synchronize database.   If database is online, update the local_db regularly and vice versa.
                            If no internet connection exists, use offline database
    Use offline db usually and do just download once (programm starts) and then upload regularly?
    What happens, if DB crashes? Is this a problem?
    """

    def synchonize_db(self):

        try:
            #db = MongoClient([conf.url_db], connectTimeoutMS=10000)[conf.db]
            print("[DB] Use online Database")
        except pymongo.errors.ConfigurationError:
            print("[DB] Use local Database")
            # TODO: import all collections into local MongoDB (write script for Docker-Container)
            #db = MongoClient()[conf.db]
            print("localhost" in str(self.db.client))

    '''
    :param db: online database
    :return: updated local database (maybe return None and just update)
    '''

    def load_db(self, from_db, to_db):
        if from_db is not None:
            for coll in from_db.list_collection_names():
                if self.local_db[coll].count_documents({}) != from_db[coll].count_documents({}):
                    for entry in from_db[coll].find():
                        query = {'_id': entry['_id']}
                        to_db[coll].replace_one(query, entry, upsert=True)
                print("Successfully stored collection -" +
                      coll + "- into MongoDB-Container.")
            print("Load database - finished")
        else:
            print("FromDB is None. Nothing to load here..")

    def replace_one_query(self, collection_name, query, update):
        self.local_db[collection_name].replace_one(query, update, upsert=True)
        if self.online_db is not None:
            self.online_db[collection_name].replace_one(
                query, update, upsert=True)

    '''
    Could be used some time to try connecting again, but do only use as backup DB to not override mistakenly
    Should be used in a thread, while the program is not in use (block usage during uploading?) May using a 
    button in Frontend.
    '''

    def retry(self):
        try:
            self.online_db = MongoClient([conf.url_db], connectTimeoutMS=10000)[
                conf.db+"_backup"]
            self.load_db(self.local_db, self.online_db)
            print("[DB] Connected to online Database")
            return "[DB] Connected to online Database"
        except pymongo.errors.ConfigurationError:
            print("[DB] No connection to online Database")
            return "[DB] No connection to online Database"


    def userdb_dataupdate(self, userdict_key_user):
        query = {'id': userdict_key_user}  # TODO id

        d = Graphdata()
        values, dic = d.generate_values(userdict_key_user)

        self.users.update_one(query, {"$set": {'data': dic}})
        return dic

    def data_transfer(self, id):
        query = {'id': id}
        self.user_id = id
        user = self.users.find_one(query)

        if user is None:
            return None
        elif 'data' in user:
            data = user['data']
            return data
        else:
            return self.userdb_dataupdate(id)


        #self.users.update_one(query, {"$set": {'data': dic}})

    def load_all_users(self, assistance, constraint):
        users = []

        for i in self.users.find():

            name = i['name']
            id = i['id']
            if (constraint(name)):
                users.append(self.load_user_from_db(id, name, assistance.library,  assistance.score_calulator))

        return users

    def upload_data(self, local, online):
        try:
            # Check internet connection
            socket.create_connection(("www.google.com", 80))

            # Connect to local MongoDB instance
            #local_client = pymongo.MongoClient(local_uri)
            local_db = local

            # Connect to online MongoDB instance
            #online_client = pymongo.MongoClient(online_uri)
            online_db = online

            # Upload data from local MongoDB to online MongoDB
            for collection_name in local_db.list_collection_names():
                local_collection = local_db[collection_name]
                online_collection = online_db[collection_name]
                online_collection.insert_many(local_collection.find({}))

            print("Data uploaded successfully.")
        except Exception as e:
            print("Could not upload data..")

    def daily_task(self):
        self.upload_data(self.local_db, self.backup_db)
        print("Task completed: Update MongoDB.")

    def run_schedule(self):
        print("Start schedule")
        while True:
            schedule.run_pending()
            time.sleep(1)
