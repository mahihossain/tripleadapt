"""
The Event Log class
"""

import datetime
import pandas as pd
import pytz
import re

from rmm4py.event_logs.xes_terminology import CASE_ID, EVENT_ID, CASE_PREFIX, TIMESTAMP, TRANSITION


class EventLog():
    """Class to hold the event log"""
    def __init__(self,
                 log:pd.DataFrame=pd.DataFrame([], columns=[CASE_ID, EVENT_ID, TIMESTAMP]),
                 case_id_name:str=CASE_ID,
                 event_id_name:str=EVENT_ID):
        """
        Initialize the log from a pandas dataframe

        Parameters
        ----------
        log: pd.Dataframe. Holds the traces with events.
        case_id_name: str, column name of the case identifier.
        event_id_name: str, column name of the event identifier
        """

        assert isinstance(log, pd.DataFrame), str(log) + "not a pandas dataframe"

        """In case of an empty log only fill the data with the empty dataframe and set all attributes to None"""
        if log.empty:
            self.data = log
            self.case_id_attribute = []
            self.event_id_attribute = []
            self.attributes = []
            self.case_list = []

        else:
            """Validate the log structure and attribute types and names"""
            validate_frame_and_attributes(log, case_id_name, event_id_name)
            self.data = log
            self.case_id_attribute = case_id_name
            self.event_id_attribute = event_id_name
            self.attributes = log.columns.tolist()
            """Contains the cases in a list for quick access"""
            self._update_data_structure()

        self.data = log
        self.case_id_attribute = case_id_name
        self.event_id_attribute = event_id_name

        """Set the case and event attributes"""
        self._update_attributes()

        """Dummy attributes for reading XES logs"""
        self.extensions = {}
        self.schema = {}
        self.classifiers = {}

        self.case_iter = None

    def append(self, trace):
        """Add a trace to the log"""

        if isinstance(trace, list):
            """In case its a list, recursively call append on each element"""
            for t in trace:
                self.append(t)

        else:
            """Otherwise it must be a trace or a pandas dataframe"""
            assert isinstance(trace, (Trace, pd.DataFrame))

            if isinstance(trace, pd.DataFrame):
                self.data = self.data.append(trace, ignore_index=True)

            elif isinstance(trace.data, (pd.DataFrame, dict)):
                self.data = self.data.append(trace.data, ignore_index=True)

        self._update_attributes()
        self._update_data_structure()

        return self

    def __len__(self):
        """Return the number of cases in the log"""
        return len(self.data.groupby(self.case_id_attribute))

    def __iter__(self):
        """Returns an iterator over the groupby object over the pd log by the case ID"""
        self.case_iter = self.data.groupby(self.case_id_attribute).__iter__()
        return self

    def __next__(self):
        """Returns the next case from the pd log by calling the next function of the groupby iterator"""
        return Trace(next(self.case_iter)[1])

    def __repr__(self):
        """Returns the data if using print"""
        return self.data.__repr__()

    def __getitem__(self, item):
        """Return the requested data. Either the n-th case if passing int or the column if passing an string"""

        """Column requested"""
        if type(item) == str:
            assert item in self.attributes
            return self.data[item]

        """Case idx requested"""
        if type(item) == int:
            return Trace(self.case_list[item])

        """View requested"""
        if type(item) == pd.Series:
            return self.data[item]

        else:
            raise NotImplementedError

    def get_case(self, case_id):
        """Get a case by its case id"""
        return Trace(self.data[self.data[self.case_id_attribute] == case_id])

    def update_event_value(self, case_id, event, attribute, value):
        """Update a single value in a log, i.e. the value of a specific attribute
        of a specific event in a specific case"""

        case = self.get_case(case_id)
        if type(event) == str:
            event = case[case[self.event_id_attribute] == event]
            index = event.index
        elif type(event) == int:
            event = case.data.iloc[event]
            index = event.name
        else:
            raise ValueError(event)

        self.data.iloc[index, self.data.columns.get_loc(attribute)] = value

    def _update_attributes(self):
        """Update the attributes in cases where a new case was added and the attributes, i.e. column names might
        have changed."""

        self.attributes = self.data.columns.tolist()
        self.case_attributes = [attr for attr in self.attributes if attr[:5] == CASE_PREFIX]
        self.event_attributes = [attr for attr in self.attributes if attr[:5] != CASE_PREFIX]

    def _update_data_structure(self):
        """Update the data structure in cases where a new case was added"""
        #cls.sort_log()
        """Do not sort as this might change the original order of the cases in the log.
        If case id is string, this will break the order."""
        self.case_list = [case for _, case in self.data.groupby(self.case_id_attribute, sort=False)]
        self.data = pd.concat(self.case_list).reset_index(drop=True)

        #TODO: Sort log by case_id or timestamp

    def sort_log(self):
        """
        Currently, we sort the log based on the case id

        Returns
        -------

        """

        if self.data[self.case_id_attribute].dtype == str:
            self.data.sort_values(by=self.case_id_attribute,
                                  key=lambda c_id: c_id.map(lambda c: int(re.sub("[^0-9]", "", c))),
                                  inplace=True)
        if self.data[self.case_id_attribute].dtype == int or self.data[self.case_id_attribute].dtype == float:
            self.data.sort_values(by=self.case_id_attribute, inplace=True)


class Trace():
    """Class to represent a trace/case"""
    def __init__(self, trace:pd.DataFrame=pd.DataFrame([]), case_id_name:str=CASE_ID, event_id_name:str=EVENT_ID):
        """
        Initialize a trace by a pandas Dataframe

        Parameters
        ----------
        trace: pd.Dataframe. Hold the data, i.e. sequences of events.
        case_id_name: str, column name of the case identifier.
        event_id_name: str, column name of the event identifier
        """

        assert isinstance(trace, pd.DataFrame), str(trace) + "not a pandas dataframe"

        """In case of an empty trace only fill the data with the empty dataframe and set all attributes to None"""
        if trace.empty:
            self.data = trace
            self.case_id_attribute = []
            self.event_id_attribute = []
            self.attributes = {}

        else:
            validate_frame_and_attributes(trace, case_id_name, event_id_name)
            self.data = trace
            self.case_id_attribute = case_id_name
            self.event_id_attribute = event_id_name
            self.attributes = trace.columns.tolist()

        self._update_attributes()

        self._importer_attributes = {}

        self.trace_iter = None

    def append(self, event):
        """Append an event to the trace"""

        if isinstance(event, list):
            """In case its a list, recursively call append on each element"""
            for e in event:
                self.append(e)

            self._update_attributes()
            return

        assert isinstance(event, Event), "event not a Event"

        if isinstance(event.data, (pd.DataFrame, dict)):
            self.data = self.data.append(event.data, ignore_index=True)
            self._update_attributes()

    def __repr__(self):
        """Returns the data if using print"""
        return self.data.__repr__()

    def __getitem__(self, item):
        """
        Return the requested data. Either the n-th event by passing n (int) or a perspective by passing an attribute
        name (string). Makes trace subscriptable, i.e., allows trace[n] or trace[concept:name]

        Parameters
        ----------
        item: int or string. n-th event or perspective

        Returns
        -------
        Either the n-th event as Series or the column.
        """

        if type(item) == int:
            return Event(self.data.iloc[item].to_dict())
        elif type(item) == str:
            return self.data[item]
        elif type(item) == pd.Series:
            return self.data[item]
        else:
            raise ValueError(item, "not supported")

    def __len__(self):
        """Returns the number of events in the trace"""
        return len(self.data)

    def __iter__(self):
        """Returns an iterator over rows, i.e., events"""
        self.trace_iter = self.data.iterrows().__iter__()
        return self

    def __next__(self):
        """Returns the next row, i.e., event using the iterator"""
        return Event(next(self.trace_iter)[1].to_dict())

    def _update_attributes(self):
        """Update the attributes in cases where a new trace was added and the attributes, i.e. column names might
        have changed."""

        self.attributes = self.data.columns.tolist()
        self.case_attributes = [attr for attr in self.attributes if attr[:5] == CASE_PREFIX]
        self.event_attributes = [attr for attr in self.attributes if attr[:5] != CASE_PREFIX]


class Event():
    """Class which holds the attribute/values pairs for an event"""
    def __init__(self, event=None):
        """
        Initialize an event by a dict.

        Parameters
        ----------
        event: dict holding as keys the attributes and as values the values.
        """

        if event is None:
            event = dict()

        assert isinstance(event, dict)
        self.data = event

    def __repr__(self):
        """Returns the data if using print"""
        return "Event:" + self.data.__repr__()

    def __getitem__(self, item):
        """Get the value of a attribute"""
        return self.data.__getitem__(item)


def validate_frame_and_attributes(log, case_id_name, event_id_name):
    """
    Check if the data is a valid pandas frame, if columns are strings and important attributes are present.
    Throws error if an issue is recognized.

    Parameters
    ----------
    log:            EventLog to be checked.
    case_id_name    str, name of the case ID column.
    event_id_name   str, name of the event id column.

    Returns
    -------


    """
    if not isinstance(log, pd.DataFrame):
        raise ValueError("Log must be a pandas dataframe")
    if not isinstance(case_id_name, str):
        raise ValueError(case_id_name, "must be a string, i.e. a column name")
    if not isinstance(event_id_name, str):
        raise ValueError(event_id_name, "must be a string, i.e. a column name")
    if not case_id_name in log.columns.tolist():
        raise ValueError(case_id_name, "not in log attributes.", log.columns.tolist())
    if not event_id_name in log.columns.tolist():
        raise ValueError(event_id_name, "not in log attributes.", log.columns.tolist())


def create_lifecycle_transition(el:EventLog, start_col, complete_col):
    """
    Create a lifecycle:transition attribute column in el by removing the start and end timestamps.
    Instead of two columns with start and end timestamp create two events. One with lifecycle:transition start
    and the start timestamp and one with lifecycle:transition end and the end timestamp

    Parameters
    ----------
    el: EventLog to work on.
    start_col: str. Column name where the timestamp that holds the start timestamp of the event is stored.
    complete_col: str. Column name where the timestamp that holds the end timestamp of the event is stored.

    Returns
    -------
    new_log: EventLog.
    """

    assert start_col in el.attributes
    assert complete_col in el.attributes

    new_log = el.data.loc[el.data.index.repeat(2)].reset_index(drop=True)
    lifecycle_col = []
    lifecycle_transition = ["start", "complete"]

    for idx in new_log.index:
        if idx % 2 != 0:
            new_log.at[idx, TIMESTAMP] = new_log.loc[new_log.index[idx], complete_col]
            lifecycle_col.extend(lifecycle_transition)

    del new_log[complete_col]
    new_log[TRANSITION] = lifecycle_col

    return new_log


def localize_datetime(event, timezone, timestamp_format):
    """
    Add the localization to the timestamp of an event.

    Parameters
    ----------
    event: Event to work on.
    timezone: Timezone to use.
    timestamp_format: str. Format in which the timestamp is encoded.

    Returns
    -------
    """

    tz = pytz.timezone(timezone)
    event[TIMESTAMP] = tz.localize(datetime.datetime.strptime(event[TIMESTAMP], timestamp_format))
    return event
