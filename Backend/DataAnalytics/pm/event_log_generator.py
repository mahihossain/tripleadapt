import pandas
import pm4py
from pm4py.objects.conversion.log import converter as log_converter

def import_csv(file_path):
    event_log = pandas.read_csv(file_path, sep=';')
    num_events = len(event_log)
    num_cases = len(event_log.case_id.unique())
    event_log = pm4py.format_dataframe(event_log, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    logs = log_converter.apply(event_log)
    return(logs, start_activities, end_activities)

def import_xes(file_path):
    event_log = pm4py.read_xes(file_path)
    num_events = len(event_log)
    num_cases = len(event_log.case_id.unique())
    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    return(event_log, start_activities, end_activities)