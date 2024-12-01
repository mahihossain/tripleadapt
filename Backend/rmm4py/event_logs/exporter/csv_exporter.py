"""
Export event logs to .csv
"""

import pandas as pd

from rmm4py.event_logs.event_log import EventLog


def save_as_csv(eventlog:EventLog, savepath, sep=";"):
    """
    Export a EventLog as .csv file

    Parameters
    ----------
    eventlog:   EventLog
                The event log to export
    savepath:   str
                Path where to save the exported .csv file
    sep:        str, optional
                Separator used to separate the attributes in the .csv file

    Returns
    -------

    """
    assert isinstance(eventlog, EventLog)
    assert isinstance(eventlog.data, pd.DataFrame)

    if savepath[-4:] != ".csv":
        savepath += ".csv"

    eventlog.data.to_csv(savepath, sep=sep)

