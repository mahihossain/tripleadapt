from enum import Enum
import Backend.config as conf

from Backend.GlobalController.ScoreCalculator import Level

class User(object):

    def __init__(self,  id, name, task_scores, score_caluclator , task_levels, library,  history=None,
                 statistical_data= None, boarders=None, role="default", pw = None):
        self.name = name
        self.id = id
        self.tasks_states = self.set_tasks_states (task_scores, task_levels, library)
        self.task_scores = task_scores
        self.task_levels =  task_levels
        self.history = history
        self.score_calculator = score_caluclator
        self.statistical_data = statistical_data
        self.boarders_used =boarders
        self.start_dates = {}
        self.role = role
        self.pw = pw
        if history is not None:
            for run in history:
                self.start_dates[run['nodes'][run['nodes_list'][0]]['start']] = run['UUID']

    def set_tasks_states (self, task_scores, task_levels, library):
         task_states =[]
         alltasks = library.all_tasks
         for task_id  in alltasks:
             task = alltasks[task_id]
             task.taskState.update_from_db (task_scores[task.id], task_levels[task.id])
             task_states.append(task.taskState)
         return task_states


    def compute_all_levels (self):
        task_levels = []
        for id in range(0, len (self.task_scores)):
            if (id== 0):
                task_levels.append(Level.LOW)
            else:
                task_levels.append (self.score_calculator.compute_level (self.task_scores[id], self.task_levels[id]))
        return task_levels


    def get_Score(self, task_id):
        return self.task_scores[task_id]

    def update_user_score_and_level(self, taskState, isvirtual):

        previous_score = self.get_Score(taskState.task_id)

        new_score = self.score_calculator.calculate_new_User_Score(taskState, previous_score, isvirtual)

        self.task_scores[taskState.task_id] = new_score

        if conf.method == "NN":
            self.task_levels[taskState.task_id] = self.score_calculator.compute_level(new_score, taskState.level)
        elif conf.method == "PM":
            # TODO: Integrate AI Method here:
            self.task_levels[taskState.task_id] = self.score_calculator.compute_level(new_score, taskState.level)

