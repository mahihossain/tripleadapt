import pymongo
from pymongo import MongoClient


from Backend.GlobalController.Assistance import Assistance

from Backend.Resources.Mongodb import DatabaseConnector


import Backend.config as conf
from Backend.Simple_NN.Agent import train
from Backend.Simple_NN.Environment import Score_Environment_NN

thrd = None
db = None
try:
    db = MongoClient([conf.url_db], connectTimeoutMS=10000)[conf.db]
    print("[DB] Connected to online Database")
except pymongo.errors.ConfigurationError:
    print("[DB] No connection to online Database")

databaseconnector = DatabaseConnector(db)
assistance = Assistance(conf.task_collection_name, use_clevr=True, model_path=conf.model_path,
                        db_connector=databaseconnector, use_adaptive_system=True)
env = Score_Environment_NN(assistance)


train(assistance)


