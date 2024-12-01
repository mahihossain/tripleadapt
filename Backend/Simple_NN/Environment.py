
from enum import Enum

from Backend.GlobalController.ScoreCalculator import ScoreCalculator


class Level(Enum):
    LOW = 1
    MEDIUM = 2
    DIFFICULT = 3

class Action(Enum):

    INCREASE_FAILURE = 1
    DECREASE_FAILURE = 2

    INCREASE_SCORE= 3
    DECREASE_SCORE = 4


# possible actions
# move boarder MAXLOW, MAXMEDIUM, MAXHARD (either higher or lower so additional float)
# move failure_easy, failure_easy_max, failure_middle, failure_hard (additional int)



class Score_Environment_NN(ScoreCalculator):
    # TODO put somewhere else
    def __init__(self, assistance):
        super(Score_Environment_NN, self).__init__(assistance)

        self.assistance = assistance
        #TODO this needs to be optimized, prob. runtime too long in future
        constraint =  lambda name: len(name)>25
        self.person_to_levels = self.extract_info(assistance.db_connector.load_all_users(assistance, constraint))

        self.score_calculator = assistance.score_calulator
        self.MAXLOW_pertask = self.score_calculator.MAXHARD_pertask
        self.MAXMEDIUM_pertask = self.score_calculator.MAXMEDIUM_pertask
        self.MAXHARD_pertask = self.score_calculator.MAXHARD_pertask

        self.failure_easy = self.score_calculator.failure_easy
        self.failure_easy_max = self.score_calculator.failure_easy_max
        self.failure_middle =self.score_calculator.failure_middle
        self.failure_hard =self.score_calculator.failure_hard

        #which time where needed, called for help, failures made
        self.current_person_run =[]

    def extract_info(self, users):
        #TODO avg_overall_failure .. are empty because über ehemaliges lever interface gmeacht
        #TODO nexte eval-> boarders müssen varrieren und abgespeichert werden
        #calculate overall average-> sum
        #TODO anpassen da nicht übereinstimmend
        boarders_used =[0]*7
        avg_overall_failure = [0] * 13
        avg_overall_duration = [0] * 13
        for u in users:
            for idx, q in enumerate(u.statistical_data['avg_failure_rate_per_task']):
                avg_overall_failure[idx] += q

            for idx, q in enumerate(u.statistical_data['avg_duration_per_task']):
                avg_overall_duration[idx] += q

            for idx, q in enumerate(u.boarders_used):
                boarders_used[idx]=q


        return avg_overall_duration, avg_overall_failure, boarders_used




    def update_users(self):
        self.person_to_levels = self.extract_info(self.assistance.db_connector.load_all_users())

    def update_enviroment(self, newboarders):
        newboarders = newboarders.view(3, 13)
        new_duration_boarders_min = newboarders[0]
        new_duration_boareders_mid = newboarders[1]

        self.MAXLOW_pertask =  new_duration_boarders_min.detach().numpy()
        self.MAXMEDIUM_pertask = new_duration_boareders_mid.detach().numpy()

        self.failure_easy =newboarders[2][0].item()
        self.failure_middle = newboarders[2][1].item()
        self.failure_hard =newboarders[2][2].item()

        return






