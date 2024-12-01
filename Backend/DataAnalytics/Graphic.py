import numpy as np
import json
import pandas as pd
import collections, functools, operator

import Backend.config as conf
# need numpy, pandas and json import


class GraphicsConstructor:

    def __init__(self, db, user_id):
        self.db = db
        self.user_db = db['user']
        self.all_users = list(self.user_db.find({}))
        self.task_db = db[conf.task_collection_name]
        self.user_id = user_id
        query = {'id': user_id}
        self.user = self.user_db.find_one(query)

        self.tasks_duration = self.generate_all_tasks_duration()
        self.all_tasks, self.task_names, self.task_ids, self.task_names_str = self.load_all_tasks()
        self.false_act_list = self.create_false_activies()

        self.error, self.error_runs = self.calculate_errors(self.user)
        self.all_failures_per_task = self.get_all_failures_task(len(self.all_tasks), self.error)
        self.avg_failures_per_task = [x / (max(1,len(self.error))) for x in self.all_failures_per_task]

        self.all_durations = self.durations(self.user)
        self.durations_per_task_dict = self.all_durations_per_task(self.all_durations)
        self.avg_durations_per_task_dict, self.avg_duration_run = self.avg_durations_per_task(self.durations_per_task_dict)

        self.avg_score_per_task, self.avg_score_run, self.score_per_run = self.compute_avg_scores(self.user_id)
        self.avg_score_all = round(sum(self.avg_score_run)/max(1,len(self.avg_score_run)),2)


    def load_all_tasks(self):
        all_tasks = []
        task_names = dict()
        task_names_string = dict()

        task_ids = []
        tasks = self.task_db.find({})
        for task in tasks:
            all_tasks.append(task)
            task_names[int(task['id'])] = task['name']
            task_names_string[task['id']] = task['name']
            task_ids.append(task['id'])
        return all_tasks, task_names, sorted(task_ids), task_names_string


    def compute_avg_scores(self, user_id):

        runs = self.user['history']
        avg_scores = []
        print(runs)
        avg_score_task = [0]*len(runs[0]["tasks_scores"])
        score_per_run = dict()

        for run in runs:
            avg_scores.append(run["tasks_scores"])
            score_per_run[run['nodes'][run['nodes_list'][0]]['start']] = run['tasks_scores']

        for score in avg_scores:
            avg_score_task[:] = [sum(x) for x in zip(avg_score_task,score)]

        avg_score_task[:] = [x/len(runs) for x in avg_score_task]

        avg_score_run = [sum(x)/len(x) for x in avg_scores]# TODO: Check

        return avg_score_task, avg_score_run, score_per_run

    def get_all_user_ids(self):
        user_ids = []
        for user in self.all_users:
            user_ids.append(user['id'])
        return user_ids

    def compute_avg_score_all_users(self):
        scores_tasks_all = []
        i = 0
        for user in self.all_users:
            i += 1
            if 'data' in user:
                scores_tasks_user = user['data']['avg_score_tasks']
            else:
                scores_tasks_user, x, y = self.compute_avg_scores(user['id'])

            if not scores_tasks_all:
                scores_tasks_all = scores_tasks_user
            else:
                scores_tasks_all[:] = [sum(x) for x in zip(scores_tasks_all, scores_tasks_user)]

        scores_tasks_all[:] = [x / i for x in scores_tasks_all]

        return scores_tasks_all

    def compute_avg_duration_all_users(self):
        duration_tasks_all = []
        for user in self.all_users:
            all_durations = self.durations(user)
            durations_per_task_dict = self.all_durations_per_task(all_durations)
            if 'data' in user:
                avg_durations_per_task_dict = user['data']['avg_task_duration']
            else:
                avg_durations_per_task_dict, avg_duration_run = self.avg_durations_per_task(
                    durations_per_task_dict)

            duration_tasks_all.append(avg_durations_per_task_dict)

        i = len(duration_tasks_all)
        duration_tasks_all = dict(functools.reduce(operator.add,map(collections.Counter, duration_tasks_all)))
        duration_tasks_all = {key: value / i for key, value in duration_tasks_all.items()}

        return duration_tasks_all


    def compute_avg_failure_all_users(self):
        failure_tasks_all = []
        i = 0
        for user in self.all_users:
            if user['history'] != []:
                i += 1
                if 'data' in user:
                    avg_failures_per_task = user['data']['avg_failure_per_failure_category']
                else:
                    error, error_runs = self.calculate_errors(user)
                    all_failures_per_task = self.get_all_failures_task(len(self.all_tasks), error)
                    avg_failures_per_task = [x / len(error) for x in all_failures_per_task]

                if not failure_tasks_all:
                    failure_tasks_all = avg_failures_per_task
                else:
                    failure_tasks_all[:] = [sum(x) for x in zip(failure_tasks_all, avg_failures_per_task)]

            failure_tasks_all[:] = [x / i for x in failure_tasks_all]

        return failure_tasks_all



    def create_false_activies(self):
        false_act_list = []
        for i in self.all_tasks:
            for j in i['steps']:
                if j['ok'] == False:
                    false_act_list.append(j['id'])
        return false_act_list


    def calculate_errors(self, user):
        runs = user['history']
        error = []
        error_dict = dict()
        for run in runs:
            failure_array = [0]*len(self.all_tasks)
            for node_name in run['nodes_list']:
                node = run['nodes'][node_name]
                if node:
                    if not node['action_ok']:
                        failure_array[node['task']] +=1
            error.append(failure_array)
            error_dict[run['nodes'][run['nodes_list'][0]]['start']] = failure_array
        return error, error_dict

    def durations(self, user):
        runs = user['history']
        duration = dict()
        print(user['name'])
        for run in runs:
            duration_array = [0] * len(self.task_ids)
            for node_name in run['nodes_list']:
                node = run['nodes'][node_name]
                if node:
                    duration_array[self.task_ids.index(str(node['task']))] += int(node['duration']) / 1000

            duration[run['nodes'][run['nodes_list'][0]]['start']] = duration_array
        return duration

    def all_durations_per_task(self, all_durations):
        task_dur = dict()
        for run in all_durations.values():
            # TODO: make dynamic
            idx = 1
            for task in run:
                if idx in self.task_names.keys():
                    if str(idx) in task_dur:
                        task_dur[str(idx)].append(task)
                    else:
                        task_dur[str(idx)] = [task]
                idx += 1
        return task_dur


    def avg_durations_per_task(self, durations_per_task_dict):
        avg_task_dur = dict()
        avg_run = 0
        for key in durations_per_task_dict.keys():
            run = durations_per_task_dict[key]
            avg_task_dur[key] = sum(run) / len(run)
            avg_run += sum(run) / len(run)
        return avg_task_dur, avg_run


    def get_all_failures_task(self, cap, error):
        all_failures_per_task = [0]*len(self.all_tasks)
        idx = 0;
        for e in reversed(error):
            all_failures_per_task = [sum(x) for x in zip(all_failures_per_task, e)]
            if idx == cap:
                break
            idx += 1
        return all_failures_per_task


    def failure__one_category_all_iterations(self, error, false_act_list):
        # one category of failures over all iterations
        out1 = {}
        out2 = {}
        out3 = {}
        out4 = {}


        for failure_category in range(len(error[0])):
            d1 = dict()
            d2 = dict()
            d3 = dict()
            d4 = dict()
            i = 0
            for a in error:

                s = str(i)
                d1[s] = int(a[failure_category])     # choose failure category
                # sum of failures in all categories over all iterations
                d2[s] = int(sum(list(a)))
                # sum of all cattegories of failures over last 10 iterations
                if len(error) >= 10:
                    # one category of failures over the last 10 iterations
                    d3[s] = int(a[failure_category])
                    # sum of all cattegories of failures over last 10 iterations
                    d4[s] = int(sum(list(a)))
                else:
                    d3[s] = int(a[failure_category])
                    d4[s] = int(sum(list(a)))
                #singular failure category counters for all different categorys put into dict with failure act as key
                out1["task" + str(failure_category)] = d1  # false_act_list[failure_category]
                out3["task" + str(failure_category)] = d3

                i = i+1
            outlist = [out1, d2, out3, d4, false_act_list]

        return outlist

    def Dataframe(self, db):


        avg_score_dict = dict()
        user_dict = dict()
        l = 0
        c = 0
        for object in self.user['history']:
            iteration = c
            r = object['nodes']
            if 'tasks_scores' in object.keys():
                task_scores = list(object['tasks_scores'])
                avg_score_dict[str(c)] = sum(task_scores) / len(task_scores)
            else:
                avg_score_dict[str(c)] = "none"
            g = 0
            for activity in r:
                j = r[activity]
                if j:
                    act_name = j['name']
                    # the following if statement is a quick bugfix. The categry bpmn_obj contains none in some of the iterated over items.
                    # bc of that the subordinate category ['id'] is not iterable
                    if j['bpmn_obj']:
                        act_id = j['bpmn_obj']['id']
                    help = j['help']
                    duration = int(j['duration'])
                else:
                    act_name = "none"
                    act_id = "none"
                    help = "none"
                    duration = "none"
                act_NR = g
                user_dict[l] = [act_name, act_id, help, duration, act_NR, iteration, self.user['name']]
                g = g + 1
                l = l + 1
            c = c + 1

        dfdict = pd.DataFrame.from_dict(user_dict, orient='index')
        dfdict.columns = ['act_name', 'act_id', 'help',
                          'duration', 'task_NR', 'iteration', 'name']

        tasks_id = list(dfdict['act_id'].drop_duplicates())
        # same order as tasks_id
        tasks_name = list(dfdict['act_name'].drop_duplicates())

        dict_of_task_dur_lists = {}
        for task in tasks_name:
            task_duration_list = list(
                dfdict['duration'].loc[dfdict['act_name'] == task])  # list of all observed durations of a specific task
            dict_of_task_dur_lists[task] = task_duration_list
        #mislabeled activities as tasks
        return tasks_id, tasks_name, dict_of_task_dur_lists, dfdict, avg_score_dict, c


    def histogram_bins(self, list_of_durs, bins):
        bin_entry_list = []
        bin_size = (int(max(list_of_durs)) - int(min(list_of_durs))) / bins
        bin_dict = {}
        bin_list = []
        for nr in range(bins):
            bin_dict[str(int(min(list_of_durs)) + bin_size * (nr + 1))] = 0
            bin_list.append(int(min(list_of_durs)) + bin_size * (nr + 1))
        for dur in list_of_durs:
            c = 1
            for bin in bin_list:
                if int(dur) < bin:
                    bin_dict[str(bin)] = bin_dict[str(bin)] + 1
                    break
                c = c + 1

        return bin_dict


    def avg_stddev(self, list_of_durs):
        avg = int(sum(list_of_durs)) / int(len(list_of_durs))
        list = []
        for dur in list_of_durs:
            list.append((dur - avg) ** 2)
        var = sum(list) / len(list)
        stdDev = var ** (1 / 2)
        results = {}
        results["avg"] = avg
        results['var'] = var
        results['stdDev'] = stdDev
        return results


    def tasks(self, db):
        tasks = self.task_db.find({})

        taskL = dict()
        for task in tasks:
            actL = []
            for act in task['steps']:
                actL.append(act['id'])
            taskL[task['id']] = actL
        return taskL


    def all_taskdurations_oneiteration(self,dfdict, taskL, chosen_iteration):
        counter = 0
        aggregated_task_dict = {}
        dfiteration = dfdict.loc[dfdict['iteration'] == chosen_iteration]

        for task in taskL.keys():
            task_dur = sum(list(dfiteration['duration'].loc[dfiteration['act_id'].isin(taskL[task])]))
            aggregated_task_dict[str(counter)] = task_dur/1000
            counter = counter + 1
        return aggregated_task_dict
        # aggregated_task_list contains ordered list of task duration for the specified instance


    def history_of_chosen_task_duration(self, IndexofChosenTask):
                duration_list = []
                for iteration in self.tasks_duration:
                    if IndexofChosenTask in iteration:
                        duration_list.append(iteration[IndexofChosenTask])

                return duration_list


    def generate_all_tasks_duration(self):
        res = []
        for run in self.user['history']:
            task_dur_dict = dict()
            for node_name in run['nodes_list']:
                node = run['nodes'][node_name]
                if node:
                    # TODO: something suspicius in a run lead to an empty node
                    if str(node['task']) in task_dur_dict:
                        task_dur_dict[str(node['task'])] += int(node['duration'])/1000
                    else:
                        task_dur_dict[str(node['task'])] = int(node['duration'])/1000
            res.append(task_dur_dict)
        return res

