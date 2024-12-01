from abc import abstractmethod

from Backend.GlobalController.TaskState import TaskState


class Task:

    def __init__(self, id, name):
        self.name = name
        self.id = id

        self.correct_flow = None
        self.alternative_flow = None
        self.taskState = TaskState(id)

    def set_correct_flow (self, correct_flow):
        self.correct_flow=correct_flow

    def set_alternative_flow(self, alternative_flow):

        self.alternative_flow= alternative_flow

    def update_task(self, act):

        self.taskState.history.append(act)
        self.taskState.update_Time(int(act.get_duration()))

        if not act.is_correct():
            self.taskState.redo_activity = True;
            self.taskState.failure_rate += 1
        else:
            self.taskState.redo_activity = False;

        return self.taskState;

    def needs_to_be_redone(self):
        return self.redo_activity;

    #TODO!!!
    def is_complete(self, act):
        if (self.correct_flow[-1].id == act.id):
            return True;
        return False;



