import networkx as nx
import json
from Backend.GlobalController.ActivityState import ActivityState


class Instance(object):

    def __init__(self, user, library,  reference_model=None, activities=[], id=None,  is_virtual=False):
        self.id = id

        self.user = user
        self.library = library
        self.failure_rate = 0
        self.is_virtual = is_virtual
        self.activities_done = []#self.set_activities_done(activities)

        # static model how process flow looks like
        self.reference_model = reference_model
        # dynamically adjusted during the process
        self.graph = nx.DiGraph()
        # is response for the fact that only new activities are send to the frontend
        self.sequence = len(activities) - 1

    def is_finished(self):
        return (self.library.get_final_activity_id() == self.get_last_processed_activity_id())

    def get_last_processed_activity_id(self):
        return self.activities_done[-1].id

    def update_graph(self, act_obj, predecessor, task, user):

        act_state = act_obj.current_activity_status
        bpmn_object = None
        n = "unknown"
        if act_state.ident in self.reference_model.get_nodes():
            bpmn_object = self.reference_model.get_nodes()[act_state.ident]
           # print(bpmn_object)

        if bpmn_object is not None:
            n = bpmn_object['name']

        r = user.task_levels[task.id]
        level_next = None
        if act_obj.get_next_activity() is not None:
            task_next = self.library.activity_to_task(act_obj.get_next_activity())
            level_next = user.task_levels[task_next.id].name

        node_id = act_state.ident
        duplicates = [value for key, value in self.graph.nodes.items() if node_id in key]
        if duplicates:
            node_id += "_" + str(len(duplicates))

        self.graph.add_node(node_id, name=n, bpmn_obj=bpmn_object, sequence=act_state.seq, help=act_state.help,
                            start=act_state.start, end=act_state.end, duration=act_state.duration, task=task.id,
                            action_ok=act_obj.is_correct(),
                            task_score=user.task_levels[task.id].name, task_score_next=level_next)

        if act_state.ident != predecessor.id:
            self.graph.add_edge(predecessor.id, act_state.ident)

    # sets the activities received by the clevr database or by a test case and transforms it to act states

    def set_activities_done(self, activities):

        activities_done = []
        for activity in activities:
            act =  activity['Activity']

            ident = act[0]['BPMNObject'][0]['ObjectId']

            ident_parts = ident.split('_')
            if len(ident_parts) > 2:
                ident = '_'.join(ident_parts[:-1])


            seq = act[1]['Sequence']
            h = act[2]['CalledForHelp']
            s = act[3]['StartDate']

            #Enddate is not safed
            if (len(act) == 5):
                d = act[4]['Duration']
                e = "not defined"
            else:
                e = act[4]['EndDate']
                d = act[5]['Duration']

            # get the corresponding activity
            act_obj = self.library.str_to_activity(ident)
            if act_obj is not None:
                if len(act) > 5:
                    #TODO this is prob wrong
                    if act[6]['IdNext'] is not None:
                        act_next = self.library.str_to_activity(act[6]['IdNext'])
                        act_obj.set_next_activity(act_next)

                activity_state = ActivityState(ident, seq, h, s, e, d)
                act_obj.set_activity_status(activity_state)

                activities_done.append(act_obj)

        self.activities_done = activities_done

        return activities_done

    # construct a graph for the frontend and updates scores

    def update(self, user):
        update = dict()
        subgraph_of_task = []
        nodes = []
        edges = []

        # if size >= 1
        predecessor = self.activities_done[0]
        for act_obj in self.activities_done:
            act_state = act_obj.current_activity_status
            if (act_state.seq) > self.sequence:
                self.sequence += 1

                # update the tasks and the scores
                task = self.library.activity_to_task(act_obj)
                task_state = task.update_task(act_obj)
                if not act_obj.is_correct():
                    self.failure_rate += 1
                    user.update_user_score_and_level(task_state, self.is_virtual)

                elif task.is_complete(act_obj):
                    user.update_user_score_and_level(task_state,  self.is_virtual)

                # update graph
                self.update_graph(act_obj, predecessor, task, user)

                # get the subgraph of task
                subgraph_of_task = self.reference_model.get_subgraph_for_task(
                    task)

                # construct the dict for the frontend
                if act_obj.id != predecessor.id:
                    edge = {"from": predecessor.id, "to": act_obj.id}
                    edges.append(edge)

                nodes.append(self.graph.nodes[act_obj.id])

            predecessor = act_obj

        update['nodes'] = nodes
        update['edges'] = edges
        update['subgraph_task'] = subgraph_of_task

       # print(update)
        return update

    # for writing an instance in db
    # 'TODO'

    def prepare_dict(self, score_calculator):
        entry = dict()
        entry['UUID'] = self.id
       # entry['StartDate'] = self.date
        entry['user'] = self.user.name
        entry['nodes'] = self.graph.nodes  # TODO hier falsche info
        entry['failure_rate'] = self.failure_rate
        entry['tasks_levels'] = [l.name for l in self.user.task_levels]
        entry['tasks_scores'] =self.user.task_scores

        entry['boarders_used'] = {}
        entry['boarders_used']["MAXHARD_pertask"] = score_calculator.MAXHARD_pertask.tolist()
        entry['boarders_used']["MAXLOW_pertask"] = score_calculator.MAXLOW_pertask.tolist()
        entry['boarders_used']["MAXMEDIUM_pertask"] = score_calculator.MAXMEDIUM_pertask.tolist()
        entry['boarders_used']["MINLOW_pertask"] = score_calculator.MINLOW_pertask.tolist()

        entry['boarders_used']["failure_easy"] = score_calculator.failure_easy
        entry['boarders_used']["failure_hard"] = score_calculator.failure_hard
        entry['boarders_used']["failure_middle"] = score_calculator.failure_middle




        nodes = []
        for node in self.graph.nodes:

            nodes.append(node)
        entry['nodes_list'] = nodes

        edges = []
        for edge in self.graph.edges:
            edges.append({'from': edge[0], 'to': edge[1]})

        entry['edges'] = edges
        return entry

    def build_JSON(self):
        json_object = json.dumps(self.inst_dict)
        return json_object
