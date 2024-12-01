from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.algo.filtering.log.cases import case_filter
from pm4py.algo.filtering.log.start_activities import start_activities_filter
from pm4py.algo.filtering.log.end_activities import end_activities_filter


def timeIntervalFilter(log, start_timestamp, end_timestamp):
    filtered_log = timestamp_filter.filter_traces_contained(log, start_timestamp, end_timestamp)
    return(filtered_log)


def casePerformanceFilter(log, min_duration, max_duration):
    filtered_log = case_filter.filter_case_performance(log, min_duration, max_duration)
    return(filtered_log)


def startActivityFilter(log, start_activity):
    log_start = start_activities_filter.get_start_activities(log)
    filtered_log = start_activities_filter.apply(log, [start_activity]) 
    return(filtered_log)


def endActivityFilter(log, end_activity):
    end_activities = end_activities_filter.get_end_activities(log)
    filtered_log = end_activities_filter.apply(log, [end_activity])
    return(filtered_log)
