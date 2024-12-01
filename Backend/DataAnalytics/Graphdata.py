import numpy as np
import json
import pandas as pd
from pymongo import MongoClient
import Backend.config as conf
from Backend.DataAnalytics.Graphic import GraphicsConstructor

class Graphdata:

    def __init__(self):

        def con_db(url, db):
            client = MongoClient(url)
            return client[db]
        self.db = con_db(conf.url_db, conf.db)

    def generate_values(self, id):
        graphics = GraphicsConstructor(self.db, id)

        '''
        durationetc = graphics.Dataframe(self.db) # list of: tasks_id, tasks_name, dict_of_task_dur_lists, dfdict, avg_score_dict, iteration

        bin_dict_list = []
        avg_var_stddev_dict_list = []

        for task in durationetc[1]:
            durs = durationetc[2][durationetc[1][8]]  # durationetc[1] = task name list; [8] is the 9th entry in the list.
            bin_dict = graphics.histogram_bins(durs, len(graphics.all_tasks))
            bin_dict_list.append(bin_dict)
            avg_var_stddev_dict = graphics.avg_stddev(durs)
            avg_var_stddev_dict_list.append(avg_var_stddev_dict)

        '''
        failures_10_runs = graphics.get_all_failures_task(9, graphics.error)

        d = {}

        # Failues

        d['false_activity_list'] = graphics.false_act_list
        d['task_names'] = graphics.task_names_str
        d['failure one cat all iterations'] = graphics.all_failures_per_task
        d['failures_per_run'] = graphics.error_runs
        d['sum failures all cat over all iterations'] = sum(graphics.all_failures_per_task)
        d['one cat failures last 10 iterations'] = failures_10_runs
        d['sum all cat failures last 10 iterations'] = sum(failures_10_runs)
        d['avg_failure_per_failure_category'] = graphics.avg_failures_per_task
        d['individual_average_completion_failure'] = sum(graphics.avg_failures_per_task)

        #d['histogram bin values'] = bin_dict
        #d['average variance std dev'] = avg_var_stddev_dict

        # Durations
        d['durations_per_run'] = graphics.all_durations #speichert überall 2730
        d['history_of_specific_task_duration'] = graphics.durations_per_task_dict
#        d['history_of_specific_task_failures'] =
#        d['history_of_specific_task_scores'] =
        d['avg_task_duration'] = graphics.avg_durations_per_task_dict
        d['individual_average_completion_duration'] = graphics.avg_duration_run

        # Score
        d['avg_score_tasks'] = graphics.avg_score_per_task
        d['avg_score_runs'] = graphics.avg_score_run # TODO check<
        d['score_per_run'] = graphics.score_per_run
        d['avg_score_history'] = graphics.avg_score_all

        d['avg_score_all_user'] = graphics.compute_avg_score_all_users()
        d['avg_duration_all_user'] = graphics.compute_avg_duration_all_users()
        d['avg_failure_all_user'] = graphics.compute_avg_failure_all_users()


        print(d)
        out = json.dumps(d)
        return out, d








