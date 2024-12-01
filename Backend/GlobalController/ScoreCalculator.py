from enum import Enum
from math import exp

import matplotlib.pyplot as plt
import numpy
import numpy as np
import random

# DONE
# findbar in db, nur eine action "3542393b-6c7a-4d0b-949a-68d6d59ab818" -> expert
# findbar in  db, nur eine action   "a7a19f4a-5770-4b43-ba04-2644f1a3b7cd" -> expert
# findbar works, but is the one which quit early from Alisa '077d2518-dc99-4087-b693-1da3d7390294'
# expert: 'cb4c5550-799f-42c4-bf4d-5ad0cc4356ee', bei tests rausgekickt, fehler bei schrauber nehmen


weight_duration = 0.5
weight_failure = 0.5
percentage_of_diff_mind_required_for_difficult = 0.2
percentage_of_diff_mind_required_for_medium = 0.7
percentage_boarder_higher = 75
percentage_boarder_lower = 25
perecentage_consider_virtual_score = 0.3


class Level(Enum):
    LOW = 1
    MEDIUM = 2
    DIFFICULT = 3


class ScoreCalculator():

    def __init__(self, assistance):

        #choose the instances here you would like to have for calculating the boarders, if task collection changes, these have to change too
        self.beginners = ['61c69be2-1cc0-4c91-ae7c-e449a46f1575',
                          '85ac81ad-bb3d-4e55-b3b5-b01c4d35dfc6',
                          'd32ff98d-f671-49df-a68e-784c02ee8e49', '29d9cbd9-678e-4972-a59d-75804a47288f']
        self.expert = ['1a2ad18f-d19b-469a-b0f0-00cf2d8893c1',
                       '6206f3e8-04f8-47dc-ad09-c9ef7dbc551a']

        self.instances = assistance.db['instances_for_border_calculation']

        # TODO use here another collection since the collected pervious data was working on this

        self.failure_easy_max = 30
        self.MAXLOW_pertask = []
        self.MAXMEDIUM_pertask = []
        self.MAXHARD_pertask = []
        self.MINLOW_pertask= []

        self.calculate_level_boarders()

        self.failure_easy = 5

        self.failure_middle = 2
        self.failure_hard = 1

        self.add_variabilitiy()

        #TODO if you would like to consider the NN for score calculation
        #if (assistance.use_adaptive_system):
        #assistance.db_connector.load_boarders(self)


    #add random variability to task boarders
    def add_variabilitiy(self):

       for ar in [self.MAXLOW_pertask, self.MAXMEDIUM_pertask,  self.MAXHARD_pertask, self.MINLOW_pertask]:
        percentage = random.uniform(0.1, 0.25)
        direction =  random.randint(-1, 1)


        if (direction == 1):
            for idx, el in enumerate(ar):
                ar[idx]= el + percentage*el

        else:
            for idx, el in enumerate(ar):
                ar[idx] = el - percentage * el


        self.failure_easy =  random.randint(0, 8)
        self.failure_middle =  random.randint(-1, 5)
        self.failure_hard =  random.randint(-1, 4)


    #initial calculation of boarders, depends on the instances given in self.beginners, self.experts
    def calculate_level_boarders(self):

        min_expert_values_activities = []
        max_beginner_values_activities = []

        #per activitiy
        plot_expert = self.get_means_per_tasks(self.expert, "expert")
        plot_beginners = self.get_means_per_tasks(self.beginners, "beginners")
        print (plot_beginners)

        #plt.plot(self.libary.linear, plot_beginners, label="mean_beginners", )

        # show plots
        # plt.xticks(range(self.libary.number_activities), self.libary.linear)
        # plt.xticks(rotation=90)
        # plt.axis([0, self.libary.number_activities, 0, 80000])
        # plt.legend()
        # plt.show()

        #calculate the sum of durations per tasks
        sum_of_durations_expert =numpy.zeros(self.libary.number_tasks+1)
        sum_of_durations_beginner = numpy.zeros(self.libary.number_tasks+1)
        for act  in self.libary.all_activities:

            act_obj =  self.libary.all_activities[act]
            index = self.libary.linear_dict[act]

            sum_of_durations_expert[act_obj.task.id] += plot_expert[index]
            sum_of_durations_beginner[act_obj.task.id] += plot_beginners [index]

        r = numpy.subtract (sum_of_durations_beginner , sum_of_durations_expert)
        if not np.all((r >= 0)):
            raise ValueError('Experts need to be faster than beginners.')

        difference = numpy.absolute (numpy.subtract (sum_of_durations_beginner , sum_of_durations_expert))

        self.MAXMEDIUM_pertask = sum_of_durations_expert + percentage_of_diff_mind_required_for_difficult * difference
        self.MAXLOW_pertask =  sum_of_durations_expert + percentage_of_diff_mind_required_for_medium * difference
        self.MAXHARD_pertask = sum_of_durations_expert
        self.MINLOW_pertask =  sum_of_durations_beginner


    #initial calculation of boarders, only called by calculate_level_boarders(self)
    def get_means_per_tasks(self, category, name):
        category_result =[]

        already_visited = []
        plot_time_y = [0] * self.libary.linear.__len__()

        for b in category:

                query = {"UUID":   b }

                inst = self.instances.find_one(query)

                nodes = inst ['Sessions']['value'][0]['Session'][4]['Historys'][0]['History'][0]['Activitys']

                for item in nodes[:-1]:
                    str_plot = item['Activity'][0]['BPMNObject'][0]['ObjectId']
                    #TODO problem: if activity was already visited, do not add it twice: either take max, first value, or add penalty

                    if (str_plot not in self.libary.linear):
                        print("problem: actitivity, not in task db", str_plot)
                        print(item['Activity'][0])

                    if (str_plot not in already_visited and str_plot in self.libary.linear):
                        already_visited.append(str_plot)


                        plot_time_y[self.libary.linear_dict[str_plot]] =(int(item['Activity'][5]['Duration']))

                        act_obj = self.libary.all_activities[str_plot]
                        if (act_obj.task.id == 11 and name == "beginners"):
                            plot_time_y[self.libary.linear_dict[str_plot]] += 2000 #TODO task 11

                            w = int(item['Activity'][5]['Duration'])
                            t = True

                category_result.append(plot_time_y)
                #for plotting only
                #if (name == 'expert'):
               # plt.plot (self.libary.linear, plot_time_y, label = name)
                plot_time_y = [0] * self.libary.linear.__len__()
                already_visited=[]

        # compute average of category
        arrays = [np.array(x) for x in category_result]
        category_result = [np.mean(k) for k in zip(*arrays)]

        return category_result



    def scores_to_levels(self, scores):

        levels = []
        for score in scores:
            levels.append(self.compute_level(score))
        return levels

    def compute_level(self, score, current_level):

        if score > percentage_boarder_higher :
            if current_level== Level.LOW:
                return Level.MEDIUM

            else:
                return Level.DIFFICULT
        elif  score < percentage_boarder_lower:
            if current_level== Level.DIFFICULT:
                return  Level.MEDIUM
            else:
                return Level.LOW

        return current_level

    def calculate_efficiency_loss(self, currentScore, previousScore):
        return  # TODO

    #per task
    def calculate_new_User_Score(self, taskState, previous_score, isvirtual):

        q = self.compute_duration_score(taskState)
        p = self.compute_failure_score(taskState)

        #if we have a virtual run, consider it less than normal runs
        #alternative: e.g. add some time to duration... to simulate an "actual run"
        score = (weight_duration * q+ weight_failure * p )

        if (isvirtual):
            score = previous_score + perecentage_consider_virtual_score * score
        return score


    def compute_duration_score (self, taskState):

        if (taskState.level == Level.LOW):
            # max low per task one is 10872, task.State.time =60
            return min(100, (self.MAXLOW_pertask[taskState.task_id] / taskState.time) * 100)

        if (taskState.level == Level.MEDIUM):
            return min(100, (self.MAXMEDIUM_pertask[taskState.task_id] / taskState.time) * 100)


        if (taskState.level== Level.DIFFICULT):
            return min(100, (self.MAXHARD_pertask[taskState.task_id] / taskState.time) * 100)

        print("Problem")
        return 0




    def compute_failure_score(self, taskState):

        if (taskState.level == Level.LOW ):

            if (taskState.failure_rate <= self.failure_easy):
                return 100
            else:
                # 3 mistakes
                # 2 +3+2-> 2/3
                return min (100, (self.failure_easy/ abs (self.failure_easy+ (taskState.failure_rate- self.failure_easy)))*100 )

        if (taskState.level == Level.MEDIUM):
            if (taskState.failure_rate <= self.failure_middle):
                return 100
            else:
                return min(100, (self.failure_middle / abs(self.failure_middle + (taskState.failure_rate - self.failure_middle))) * 100)

        if (taskState.level == Level.DIFFICULT):
            if (taskState.failure_rate <= self.failure_hard):
                return 100
            else:
                return min (100, (self.failure_hard/ abs (self.failure_hard+ (taskState.failure_rate- self.failure_hard)))*100 )


