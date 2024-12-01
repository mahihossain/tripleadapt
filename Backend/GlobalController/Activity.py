from abc import ABC, abstractmethod


class Activity(ABC):

    @abstractmethod
    def __init__(self, id , name , task, x, y):
        self.name = name
        self.id = id
        self.correct = None
        self.task = task
        self.current_activity_status = None
        self.x = x
        self.y = y
        self.next = None

    def set_next_activity(self, activity):
        self.next = activity

    def get_next_activity(self):
        return self.next

    def is_correct(self):
        return self.correct

    def get_duration(self):
        return self.current_activity_status.duration

    def set_activity_status(self, status):
        self.current_activity_status = status

    def get_x_coordinate(self):
        return self.x

    def get_y_coordinate(self):
        return self.y


class NormalActivity(Activity):

    def __init__(self, id, name, task, x, y):
        super(NormalActivity, self).__init__(id, name, task, x, y)
        self.correct = True



class AlternativeActivity(Activity):

    def __init__(self, id, name, task, x, y, jump_back):
        super(AlternativeActivity, self).__init__(id, name, task, x, y)
        self.correct = False
        self.jump_back_to = jump_back

    def jump_back(self):
        return self.jump_back_to()
