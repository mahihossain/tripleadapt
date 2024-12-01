from enum import Enum
from math import exp

import matplotlib.pyplot as plt
import numpy
import numpy as np
import random

#TODO in task 11, sind experten langer, s unten deshalb gehardcoded
from Backend.GlobalController.Library import Library
from Backend.GlobalController.ScoreCalculator import Level, ScoreCalculator

weight_duration = 0.5
weight_failure = 0.5
percentage_of_diff_mind_required_for_difficult = 0.2
percentage_of_diff_mind_required_for_medium = 0.7
percentage_boarder_higher = 75
percentage_boarder_lower = 25

class ScoreCalculator_cyclinder_eval(ScoreCalculator):

    def __init__(self, assistance, collect_data_for_nn=False):

        self.beginners = [ '61c69be2-1cc0-4c91-ae7c-e449a46f1575',
            '85ac81ad-bb3d-4e55-b3b5-b01c4d35dfc6',
            'd32ff98d-f671-49df-a68e-784c02ee8e49', '29d9cbd9-678e-4972-a59d-75804a47288f']
        self.expert = ['1a2ad18f-d19b-469a-b0f0-00cf2d8893c1',
                       '6206f3e8-04f8-47dc-ad09-c9ef7dbc551a' ]

        self.instances = assistance.db['instances_for_border_calculation']

        #TODO use here another collection since the collected pervious data was working on this
        self.libary = Library(assistance.db['tasks_for_border_calculation'])

        self.failure_easy_max = 30
        self.MAXLOW_pertask = []
        self.MAXMEDIUM_pertask = []
        self.MAXHARD_pertask = []
        self.MINLOW_pertask= []

        self.calculate_level_boarders()

        self.failure_easy = 5

        self.failure_middle = 2
        self.failure_hard = 1

        #TODO if collecting data
        self.collect_data_for_nn = collect_data_for_nn
        if self.collect_data_for_nn:
            self.add_variabilitiy()

        if (assistance.use_adaptive_system):
            assistance.db_connector.load_boarders(self)






