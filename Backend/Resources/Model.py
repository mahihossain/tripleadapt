from xml.etree.ElementTree import fromstring, ElementTree

import json


# TODO: integrate process model (SOLL-Modell) &
import fnmatch
#TODO change bpmn path possible here
from ..rmm4py.models.importer import bpmn_importer


class Model(object):

    def __init__(self, bpmn_path, db, library):
        self.collection = db['models']
        self.name = bpmn_path

        self.collaboration_model = bpmn_importer.load_diagram_from_xml(bpmn_path)
        # graph is from networkx
        self.graph = self.collaboration_model.process_graph
        self.db = db
        self.add_material(db)

        self.all_activities = library.all_activities
        self.all_tasks = library.all_tasks
        self.library = library

        self.tasks = dict()
        self.task_edges = dict()
        self.load_model_db(self.name)

        if self.graph_json is None:
            self.graph_json = self.prepare_dict_json()
            self.save_model_db()

        #self.update_acitivty_ids('tasks_new',"tasks_cylinder_v2")

    def update_acitivty_ids(self, old_task_collection, new_task_collection):
        tasks_old = self.db[old_task_collection]
        tasks_new = self.db[new_task_collection]
        task_list = []
        for task in tasks_old.find({}):
            task_list.append(task)

        for node in self.graph.nodes:
            if 'name' in self.graph.nodes[node]:
                for task in task_list:
                    for activity in (task['steps']):
                        if activity['name'] == self.graph.nodes[node]['name']:
                            activity['id'] = node


        for task in task_list:
            query = {"id": task['id']}
            tasks_new.replace_one(query, task, upsert=True)


    def add_material(self, db):
        materials = db['material']

        for node in self.graph.nodes:
            query = {"id": node}
            res = materials.find_one(query)
            if res is not None:
                self.graph.nodes[node]['material'] = res['material']


    def get_model(self):
        return self.collaboration_model

    def get_nodes(self):
        return self.graph.nodes

    def get_edges(self):
        return self.graph.edges

    def load_model_db(self, name):
        query = {"name": name}
        self.graph_json = self.collection.find_one(query)
        if self.graph_json is not None:
            self.graph_json['_id'] = str(self.graph_json['_id'])

    def save_model_db(self):
        query = {"name": self.name}
        self.collection.replace_one(query, self.graph_json, upsert=True)

    def prepare_dict(self):
        entry = dict()
        entry['name'] = self.name
        entry['nodes'] = self.graph.nodes
        edges = []
        for edge in self.graph.edges:
            edges.append({'from': edge[0], 'to': edge[1]})
        entry['edges'] = edges
        return entry

    #'TODO' aufräumen
    def get_subgraph_for_task(self, task):

         entry = dict()
         task_all_activities =[]
         for z in task.correct_flow:
             task_all_activities.append(z.id)

         for t in task.alternative_flow:
             task_all_activities.append(t.id)

         nodes =[]
         all_node_objects =[]
         edges = []
         for node in self.graph.nodes.data():

             values = node[1]
             id = values['id']

             if (id in task_all_activities):
                 all_node_objects.append(node)
                 data = dict()
                 # TODO: Add task infos (task_id & is_ok)
                 data['type'] = values['type']
                 data['id'] = values['id']
                 if 'name' in values.keys():
                     data['name'] = values['name']
                     if 'material' in values.keys():
                        data['material'] = values['material']
                 else:
                     data['name'] = ""
                     data['material'] = ""

                 if values['id'] in self.all_activities.keys():
                     activity = self.all_activities[values['id']]
                     data['task'] = activity.task.id
                     data['correct'] = activity.correct
                     data['x'] = activity.get_x_coordinate()
                     data['y'] = activity.get_y_coordinate()
                 else:
                     data['task'] = ""
                     data['correct'] = ""
                     data['x'] = ""
                     data['y'] = ""

                 nodes.append(data)

         pred_dict = self.graph.pred
         succ_dict = self.graph.succ
         for edge in self.graph.edges:


             if (edge[0] in task_all_activities):

                 #if gateway
                 if (edge[1][0:7] == 'Gateway'):

                     outgoing = succ_dict[edge[1]]
                     for e in outgoing:

                        edges.append({'from': edge[0], 'to': e})

                 else:
                     edges.append({'from': edge[0], 'to': edge[1]})

             elif (edge[1] in task_all_activities):

                # if it is a gateaway we have the endnode, but startnode is gateaway
                # if (edge[0][0:7] == 'Gateway'):

                   #  incoming = pred_dict[edge[0]]
                   #  for e in incoming:
                    #     edges.append({'from': e, 'to':  edge[1] })
                if (edge[0][0:7] != 'Gateway'):
                    edges.append({'from': edge[0], 'to': edge[1]})

         entry['task_id'] = task.id
         entry['task_name'] = task.name
         entry['nodes'] = nodes
         entry['edges'] = edges
         return entry

        #id noten, , connetor or , connectoren ,


    #send the global modes once to frontend at beginning
    def prepare_dict_json(self):
        #here
        entry = dict()
        entry['name'] = self.name
        nodes = []

        for node in self.graph.nodes.data():
            values = node[1]

            data = dict()

            data['type'] = values['type']
            data['id'] = values['id']
            if 'name' in values.keys():
                data['name'] = values['name']
                if 'material' in values:
                    data['material'] = values['material']
                else:
                    data['material'] = ""
            else:
                data['name'] = ""
                data['material'] = ""

            if values['id'] in self.all_activities.keys():
                activity = self.all_activities[values['id']]
                data['task'] = activity.task.id
                data['correct'] = str(activity.correct)
                data['x'] = activity.get_x_coordinate()
                data['y'] = activity.get_y_coordinate()
                ''' dict from task_id to lost of acitivies (no edges yet)
                if self.tasks[activity.task.id] is None:
                    self.tasks[activity.task.id] = [activity]
                else:
                    self.tasks[activity.task.id].append(activity)
                    '''
            else:
                data['task'] = ""
                data['correct'] = ""
                data['x'] = ""
                data['y'] = ""

            nodes.append(data)

        edges = []
        for edge in self.graph.edges:
            edges.append({'from': edge[0], 'to': edge[1]})

        tasks = []
        for task in self.all_tasks.values():
            tasks.append({'task_id': task.id, 'task_name': task.name})
            pass

        entry['nodes'] = nodes
        entry['edges'] = edges
        entry['tasks'] = tasks

        # set initial task
        act_obj = self.library.str_to_activity("Activity_0dwnqmx")
        task = self.library.activity_to_task(act_obj);
        subgraph_of_task = self.get_subgraph_for_task(task)
        entry['init_model'] = subgraph_of_task

        return entry


    #calles by frontend
    def model2JSON(self):
        return json.dumps(self.graph_json)
