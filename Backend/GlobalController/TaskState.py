from Backend.GlobalController.ScoreCalculator import Level


class TaskState:


    def __init__(self, task_id):
        self.task_id = task_id
        self.score = 0;
        self.quality = 0;
        self.level = Level.LOW
        self.time = 0;
        self.failure_rate = 0
        self.redo_activity = False
        self.history = []

    def update_from_db (self, score, level):
        self.score= score
        self.level = level

    def update_Time(self, time_of_act ):
        self.time = self.time + time_of_act

    def update_Score(self,  update):
        self.score += update;

    def needs_to_be_redone(self):
        return self.redo_activity;

    def has_bad_quality(self):
        if self.quality < 0:
            return True;
        else:
            return False;
