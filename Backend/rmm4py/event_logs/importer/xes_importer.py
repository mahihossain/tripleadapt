"""
Importer for XES files.
"""
import os.path

import pandas as pd
from lxml import etree
from tqdm import tqdm
from datetime import datetime

from rmm4py.event_logs.xes_terminology import CASE_PREFIX
from rmm4py.event_logs.event_log import EventLog


def import_xes(filepath, number_traces=None, multiprocessing=False):
    """
    Read a XES Log from file and convert it to an EventLog.

    Parameters
    ----------
    filepath:           str, path to the file to read.
    number_traces       int, maximum number of traces to read.
    multiprocessing     boolean, if to use multiprocessing while reading the events (not working yet).

    Returns
    -------
    An EventLog containing all events in traces.

    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    """Open the XES"""
    tree = etree.parse(filepath)
    root = tree.getroot()

    """Extract the namespace"""
    root_tag = str(root.tag)
    namespace = root_tag[root_tag.find("{"):root_tag.find("}")+1]

    """Find all traces"""
    traces = root.findall(namespace + "trace")

    """Cut to number_traces"""
    if number_traces:
        traces = traces[0:number_traces]

    """event_data is a list of dicts with attribute/value pairs"""
    event_data = []
    if not multiprocessing:
        for trace in tqdm(traces):
            event_data.extend(parse_trace(trace))

    else:
        #TODO @Peter: Fix it.
        trace_list = read_parallel(traces)

    """Build the EventLog from the list of dicts"""
    event_log = EventLog()
    event_log.data = pd.DataFrame(event_data)
    event_log._update_attributes()
    """Reset index to have it going from 1,..,#events instead of starting at 1 in each trace again"""
    event_log.data.reset_index(drop=True, inplace=True)
    """Finally, update the data structure, i.e. the case list etc."""
    event_log._update_data_structure()

    return event_log

def parse_trace(trace_root):
    """
    Parse a single trace to a list of dicts.

    Parameters
    ----------
    trace_root  The etree root of the trace to be parsed.

    Returns
    -------
    A list of dicts, each representing a event and its case attributes.
    """

    case_attributes = {}
    event_list = []

    #print(len(trace_root.findall(namespace + "event")))
    for elem in trace_root:
        if elem.tag.endswith("event"):
            """Read a event"""
            event = parse_event(elem)
            event_list.append(event)
        else:
            """Otherwise its a trace attribute"""
            if elem.tag.endswith("date"):
                dt = parse_date(elem.get("value"))
                case_attributes[CASE_PREFIX + elem.get("key")] = dt
            else:
                case_attributes[CASE_PREFIX + elem.get("key")] = elem.get("value")

    """Add case attributes to each event"""
    [event.update(case_attributes) for event in event_list]

    return event_list


def parse_event(event_root):
    """
    Parse a single event to a dict.

    Parameters
    ----------
    event_root  The root of the event in the etree.

    Returns
    -------
    A dict containing all attribute/value pairs.
    """
    event = {}
    for elem in event_root:
        if elem.tag.endswith("date"):
            dt = parse_date(elem.get("value"))
            event[elem.get("key")] = dt
        else:
            event[elem.get("key")] = elem.get("value")

    return event


def parse_date(value):
    """
    Parse the tree element if it is a date.

    Parameters
    ----------
    value   value to parse

    Returns
    -------
    A datetime object.
    """
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)

    return dt

def read_parallel(traces):
    """
    Read and convert the traces in multiple processes. Not working yet.

    Parameters
    ----------
    traces  list of traces to process.

    Returns
    -------
    list of dicts, each element a event.

    """

    """
    from multiprocessing import Pool
    import multiprocessing

    n_cores = int(multiprocessing.cpu_count()/2)

    traces_splits = np.array_split(traces, n_cores)
    pool = Pool(n_cores)

    grouped_cases = pool.map(parse_trace, traces_splits)
    print(grouped_cases)

    pool.close()
    pool.join()

    return grouped_cases
    """

    raise NotImplementedError("Not working yet. Issue with pickle and lxml object.")



