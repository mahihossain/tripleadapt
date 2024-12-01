"""
Imports csv logs and changes timestamp format to datetime
"""

import pandas as pd
import os

from rmm4py.event_logs.xes_terminology import CASE_ID, EVENT_ID, RESOURCE, TIMESTAMP, CASE_PREFIX
from rmm4py.event_logs.event_log import EventLog, create_lifecycle_transition


def load_csv_log(filepath:str, sep:str=";", case_id:str=CASE_ID, activity:str=EVENT_ID,
                 timestamp:str=TIMESTAMP, resource:str=RESOURCE, timestamp_end:str= None,
                 case_attributes:list=None):
    """
    Load a csv log from file and create an internal Event Log representation of it.

    Parameters
    ----------
    filepath:           basestring
                        Path to Log
    sep:                basestring
                        delimiter in csv file (e.g. "," or ";")
    case_id:            basestring
                        column name of case id
    activity:           basestring
                        column name of activity
    timestamp:          basestring
                        column name of timestamp
    resource:           basestring (optional)
                        column name of resource
    timestamp_end:      basestring
                        column name of "end" timestamp (only necessary if every activity
                        has two timestamps: "start" and "end")
    case_attributes:    list[basestring] (optional)
                        list with case attributes

    Returns
    -------
    EventLog:
                        EventLog

    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    #TODO(@Peter): Use engine="pyarrow"
    # https://pandas.pydata.org/docs/whatsnew/v1.4.0.html#multi-threaded-csv-reading-with-a-new-csv-engine-based-on-pyarrow

    try:
        """engine = "python" for file encoding UTF-8"""
        pd_log = pd.read_csv(filepath, sep=sep, engine="python")
    except UnicodeDecodeError:
        # For BPIC2016
        pd_log = pd.read_csv(filepath, sep=sep, encoding="ISO-8859-1")

    el = convert_csv_to_el(pd_log=pd_log, case_id=case_id, activity=activity, timestamp=timestamp, resource=resource,
                           timestamp_end=timestamp_end, case_attributes=case_attributes)

    return el


def convert_csv_to_el(pd_log:pd.DataFrame(), case_id:str=CASE_ID, activity:str=EVENT_ID, timestamp:str=TIMESTAMP,
                      resource:str=RESOURCE, timestamp_end:str=None, case_attributes:list=None):
    """
    Convert a pandas dataframe comming from reading a .csv file to a rmm4pycore EventLog.

    Does not localize timestamps at the moment (all are +00:00)

    Parameters
    ----------
    pd_log:             pd.Dataframe()
                        pandas object to convert
    case_id:            str
                        column name of CASE_ID
    activity:           str
                        column name of EVENT_ID
    timestamp:          str
                        column name of TIMESTAMP
    resource:           str
                        column name of RESOURCE
    timestamp_end:      str
                        column name of "end" timestamp
                        (only necessary if every activity has two timestamps: "start" and "end")
    case_attributes:    list[basestring] (optional)
                        list with case attributes column names

    Returns
    -------
    EventLog:
                        EventLog

    """

    """check if given column names exist in log and rename them"""
    main_attributes = [case_id, activity, timestamp]
    not_exist_str = " does not exist as column name"

    for e in main_attributes:
        if e not in pd_log.columns:
            raise ValueError(e + not_exist_str)

    pd_log.rename(columns={activity: EVENT_ID,
                           timestamp: TIMESTAMP,
                           case_id: CASE_ID},
                  inplace=True)

    if resource in pd_log.columns:
        pd_log.rename(columns={resource: RESOURCE}, inplace=True)

    if case_attributes == None:
        case_attributes = list()

    for element in case_attributes:
        if element in pd_log.columns:
            pd_log.rename(columns={element: CASE_PREFIX + element}, inplace=True)
        else:
            raise ValueError(element + not_exist_str)

    """Convert to rmm4pycore Event Log"""
    el = EventLog(pd_log)

    """if second timestamp is given -> add lifecycle:transition and to combine both given timestamps to one"""
    if timestamp_end is not None:
        el.data = create_lifecycle_transition(el, start_col=TIMESTAMP, complete_col=timestamp_end)

    """Convert the timestamps from string to a pandas Timestamp"""
    el.data[TIMESTAMP] = pd.to_datetime(el.data[TIMESTAMP], utc=True, infer_datetime_format=True)
    #print(el.data[TIMESTAMP])

    """Convert the timestamps to localized datetimes"""
    #TODO @Peter: Check if we still want this or not
    #timezone = "Europe/Berlin"
    #el.data = el.data.apply(lambda e: localize_datetime(e, timezone, timestamp_format), axis=1)

    """Finally, update the attributes and data structure"""
    el._update_attributes()
    el._update_data_structure()

    return el





