from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.statistics.traces.generic.log import case_arrival


def throughputTime(log):
    all_case_durations = case_statistics.get_all_casedurations(log, parameters={
    case_statistics.Parameters.TIMESTAMP_KEY: "time:timestamp"})
    return(all_case_durations)


def arrivalRatio(log):
    case_arrival_ratio = case_arrival.get_case_arrival_avg(log, parameters={
    case_arrival.Parameters.TIMESTAMP_KEY: "time:timestamp"})    
    return(case_arrival_ratio)
