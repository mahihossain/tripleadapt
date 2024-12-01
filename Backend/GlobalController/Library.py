
from Backend.GlobalController.Activity import AlternativeActivity, NormalActivity
from Backend.GlobalController.Task import Task


# includes all tasks and activities and maps them to each other
class Library:
    def __init__(self, taskcollection):

        self.all_tasks = self.set_tasks(taskcollection)
        self.linear, self.linear_dict = self.compute_linear_view(
            taskcollection)
        self.number_tasks = len(self.all_tasks)

        # map of key= id of act and value= object of act
        self.all_correct_flow = []
        self.all_activities = self.set_activities(taskcollection)
        self.number_activities = len(self.linear)



    def compute_linear_view(self, taskcollection):
        linear = []
        linear_dict = {}

        lin_view = taskcollection.find({})
        i = 0

        for tasks in lin_view:

            for act in tasks['steps']:
                linear.append(act['id'])
                linear_dict[act['id']] = i

                i = i + 1
        return linear, linear_dict

    def set_tasks(self,  tasksdb):
        tasks = tasksdb.find({})
        tasks_obj = dict()

        for task in tasks:
            task_t = Task(int(task['id']), task['name'])
            tasks_obj[task_t.id] = task_t
        return tasks_obj

    def get_final_activity_id(self):
        return self.all_tasks[self.number_tasks].correct_flow[-1].id

    def get_task_from_str(self, str):
        return self.all_tasks[int(str)]

    def set_activities(self, tasksdb):
        activitiesdict = dict()
        tasks = tasksdb.find({})
        for task in tasks:
            correct_flow = []
            alternative_flow = []
            task_obj = self.get_task_from_str(task['id'])
            for activity in (task['steps']):
                name = activity['name']
                id = activity['id']
                is_standard_activitiy = activity['ok']
                try:
                    x = activity['x']
                    y = activity['y']
                    #print("added coordinates")

                except:
                    x = None
                    y = None
                    #print("Library Line 67: x and y coordinate. Delete try-except after testing")

                if is_standard_activitiy:

                    act = NormalActivity(id, name, task_obj, x, y)
                    correct_flow.append(act)
                    self.all_correct_flow.append(act)

                else:
                    act = AlternativeActivity(
                        id, name, task_obj, x, y, activity['returntoid'])
                    alternative_flow.append(act)

                activitiesdict[act.id] = act
            task_obj.set_correct_flow(correct_flow)
            task_obj.set_alternative_flow(alternative_flow)
        return activitiesdict

    def str_to_activity(self, ident):
        if ident in self.all_activities:
            return self.all_activities[ident]
        else:
            print("Key does not exist: " + ident)
            return None

    def activity_to_task(self, act):
        return act.task

    def get_successor(self, activity):
        index = self.all_correct_flow.index(activity)
        if (len(self.all_correct_flow) - 1 != index):
            return self.all_correct_flow[index+1]
        return None
