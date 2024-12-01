"""
Module to find the most frequent traces in a log.
"""
import sys
import pandas as pd

from rmm4py.event_logs.event_log import EventLog, Trace
from rmm4py.event_logs.xes_terminology import CASE_ID, EVENT_ID


def compute_variants(log, event_id_col:str=EVENT_ID, sort_by_frequency=False):
    """
    Computes the variants present in the log and returns a dict with str "Variant x" as key and
    the control-flow as value.

    Parameters
    ----------
    log:                Event Log.
    event_id_col:       str, name of the event ID column.
    sort_by_frequency:  bool, if true sort the dict by the variant frequency.

    Returns
    -------
    dictionary with str "Variant x" as key and the control-flow as value.
    """

    assert isinstance(log, EventLog), "log must be an Event Log"
    assert event_id_col in log.attributes, "event id not in log"

    if sort_by_frequency:
        log_variant_dict = group_log_by_variants(log, event_id_col=event_id_col, sort_by_frequency=True)
        log_variant_dict = {v: cf[0][event_id_col].tolist() for v, cf in log_variant_dict.items()}

        return log_variant_dict

    pd_log = log.data[[CASE_ID, EVENT_ID]]

    variants = {}
    cases = pd_log.groupby([CASE_ID])
    for case_id, c in cases:
        cf = c[EVENT_ID].tolist()

        if cf not in variants.values():
            variants["Variant " + str(len(variants.values()) + 1)] = cf

    return variants


def group_log_by_variants(log:EventLog, event_id_col:str=EVENT_ID, sort_by_frequency=False):
    """
    Group a log based on the variant of the cases.

    Parameters
    ----------
    log:                EventLog to be grouped.
    event_id_col:       str, column name of the event ID
    sort_by_frequency:  bool if to sort by variant frequency.

    Returns
    -------
    A dict with the variant names as key and a list of Trace with that variant as value.

    """
    log_variant_dict = {}

    """Compute the variants in the log"""
    variants = compute_variants(log, event_id_col=event_id_col, sort_by_frequency=False)

    """Add the variant names to a new dict which holds the list of cases later"""
    for v in variants.keys():
        log_variant_dict[v] = []

    """Creat a dict with the control-flow as key to have access to the variant name"""
    cf_to_variant = {str(cf): v for v, cf in variants.items()}

    pd_log = log.data

    """For each case in the log, determine the variant and append the case to the dict"""
    for case_id, case in pd_log.groupby([CASE_ID]):
        cf = case[event_id_col].tolist()
        v = cf_to_variant[str(cf)]
        log_variant_dict[v].append(Trace(case))

    if sort_by_frequency:
        log_variant_dict = sort_variant_by_frequency(log_variant_dict)

    return log_variant_dict


def sort_variant_by_frequency(log_variant_dict:dict):
    """Sort the variants by their frequency, i.e. the number of cases per variant"""

    log_variant_dict = dict(reversed(sorted(log_variant_dict.items(), key=lambda item: len(item[1]))))

    """Create new dict with the variant names according to the frequency, i.e. the most prominent variant with 1"""
    new_log_variant_dict = {}
    for i, (variant, cases) in enumerate(log_variant_dict.items()):
        new_log_variant_dict["Variant " + str(i + 1)] = cases

    return new_log_variant_dict


def get_n_most_frequent_traces(event_log:EventLog, n=sys.maxsize, min_num_traces=0, activity_key=EVENT_ID):
    """
    Return an event log with the most frequent traces such that at most n case variants are in the log
    and/or each variant has as least min_num_traces.

    Parameters
    ----------
    event_log
    n:                  int, maximum number of most frequent traces.
    min_num_traces:     int, minimum number of traces a variant must have.

    Returns
    -------

    """

    mfv = group_log_by_variants(log=event_log, event_id_col=activity_key, sort_by_frequency=True)
    n_variant = 0

    n_most_frequent_traces = []

    for variant, case_list in mfv.items():
        if len(case_list) < min_num_traces:
            continue
        if n_variant >= n:
            break
        else:
            n_most_frequent_traces.extend(case_list)
            n_variant += 1

    n_most_frequent_traces = [t.data for t in n_most_frequent_traces]
    pd_log = pd.concat(n_most_frequent_traces).reset_index(drop=True)

    return EventLog(pd_log)

