import json
import time

from Backend.GlobalController.Library import Library
from Backend.GlobalController.Score_Calculator_cyclinder_eval import ScoreCalculator_cyclinder_eval

from Backend.Resources.Model import Model
from Backend.GlobalController.Instance import Instance
from Backend.Simple_NN.Agent import train
from Backend.Simple_NN.Environment import Score_Environment_NN


class Assistance(object):
    """
    initialize the assistance by creating an empty instance and a user who uses (by name) the system

    """
    do_assist = True
    assist_status = "{}"

    def __init__(self, tasks_collection, use_clevr=True, model_path=None, button=False, db_connector=None, use_adaptive_system=False, activities=[]):

        self.start = button

        self.use_clevr = use_clevr
        self.db = db_connector.local_db
        self.db_connector = db_connector

        self.tasks_collection = tasks_collection
        self.library = Library(self.db[tasks_collection])
        self.model = Model(model_path, self.db, self.library)
        self.use_adaptive_system = use_adaptive_system
        self.activities = activities


        #self.old_to_new = dict()
        #self.new_to_old = dict()
        #self.create_mapping('tasks_new',"tasks_cylinder_v2")


        if (use_adaptive_system):  # for testing
            self.score_calulator = ScoreCalculator_cyclinder_eval(self)
            self.score_calulator = Score_Environment_NN(self)

        else:
            self.score_calulator = ScoreCalculator_cyclinder_eval(self)

        self.instance = None
        self.user = None
        self.user_all = self.db_connector.load_user_from_db("all", "all", self.library, self.score_calulator)
        self.db_connector.user_all = self.user_all

    def create_mapping(self, old, new):
        tasks_old = self.db[old]
        tasks_new = self.db[new]
        task_list_old = []
        task_list_new = []
        for task in tasks_old.find({}):
            task_list_old.append(task)

        for task in tasks_new.find({}):
            task_list_new.append(task)

        temp = dict()
        temp2 = dict()
        for task in task_list_old:
            for activity in (task['steps']):
                temp[activity['name']] = activity['id']

        for task in task_list_new:
            for activity in (task['steps']):
                self.new_to_old[activity['id']] = temp[activity['name']]
                temp2[activity['name']] = activity['id']

        for task in task_list_old:
            for activity in (task['steps']):
                self.old_to_new[activity['id']] = temp2[activity['name']]



    def set_user(self, user_id, user_name = 'Not provided'):
        self.user = self.db_connector.load_user_from_db(user_id, user_name, self.library, self.score_calulator)

    def set_instance(self, instance_id, is_virtual=False):
        self.instance = Instance(self.user, self.library, reference_model=self.model,
                                 activities=self.activities,
                                 id=instance_id,  is_virtual=is_virtual)

    def set_user_and_instance(self, user_id, instance_id, is_virtual=False, user_name="Not provided"):

        self.set_user(user_id, user_name)
        self.instance = Instance(self.user, self.library, reference_model=self.model,
                                 activities=self.activities,
                                 id=instance_id,  is_virtual=is_virtual)


    def update(self, no_test=True):

        while self.do_assist:
            time.sleep(1)
            if self.use_clevr:
                    self.instance.set_activities_done(self.activities)
                    final_result = self.instance.update(self.user)
                    #self.send_info_to_clevr(self.library.all_tasks)  #TODO needed?

                    if (no_test):
                        self.db_connector.save_progress(self, self.instance.is_finished())

                    # Check whether process is finished
                    if (self.instance.is_finished()):
                        #self.db_connector.save_progress(self, is_finished=True)
                        #self.send_info_to_clevr(self.library.all_tasks)
                        if (self.use_adaptive_system):
                            self.update_neural_network()

            return final_result

        return "None"

    # TODO: Change if permission isn't necessary anymore
    def set_permission(self, permission):
        if permission:
            self.update()
            return True
        else:
            self.data = None
            self.model = None
            self.instance = None
            self.start = False
            return False

    def send_info_to_clevr(self, tasks):
        response = dict()
     #  response['guide_uuid'] = self.data.get_guide()
        response['user_uuid'] = self.user.id
        response['revision_uuid'] = self.instance.id

        tasks_response = []
        for task in tasks.values():

            task_response = dict()
            task_response['task_id'] = task.id
            # TODO: hardcoded atm
            task_response['show_nugget'] = False
            task_response['task_name'] = task.name
            task_response['level'] = self.user.task_levels[task.id].name
            task_response['activities'] = [i.id for i in (
                task.alternative_flow + task.correct_flow)]

            tasks_response.append(task_response)

        response['recommendations'] = tasks_response
        # print("clevr debug")
        # send recommendation to clevr (not needed at the moment; send response back in /data)
        # print(send_recommendation(response))
        return response

    def update_neural_network(self):
        train(self)

