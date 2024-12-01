"""
Functions to check for equality between two event log traces
"""
import pandas as pd
from rmm4py.event_logs.event_log import Trace
from rmm4py.event_logs.xes_terminology import EVENT_ID


def perspective(trace_1:Trace, trace_2:Trace, perspective:str):
    """
    Check if two perspectives are similar

    Parameters
    ----------
    trace_1: Trace, first trace
    trace_2: Trace, second trace
    perspective: str, name of the perspective of interest

    Returns
    -------
    bool    True if both trace have the same values in the perspective. False otherwise.

    """

    if not isinstance(trace_1, (Trace, pd.DataFrame)):
        raise ValueError(trace_1, "neither Trace nor dataframe")

    if not isinstance(trace_2, (Trace, pd.DataFrame)):
        raise ValueError(trace_2, "neither Trace nor dataframe")

    if not isinstance(perspective, str):
        raise ValueError(perspective, "not a string")

    result = trace_1[perspective].values == trace_2[perspective].values

    if type(result) == bool:
        return result

    else:
        return result.all()



def control_flow(trace_1:Trace, trace_2:Trace, control_flow_attribute:str=EVENT_ID):
    """
    Check if two traces have the same control-flow, i.e. the same sequence of activities.

    Parameters
    ----------
    trace_1 :   Trace
    trace_2 :   Trace
    control_flow_attribute: str, the name of the control-flow attribute

    Returns
    -------
    bool
                True if both traces (or list) have the same sequence of activities, False otherwise


    """

    if trace_1 is None and trace_2 is None:
        return True
    elif trace_1 is None:
        return False
    elif trace_2 is None:
        return False

    if not isinstance(trace_1, (Trace, pd.DataFrame)):
        raise ValueError(trace_1, "Not a trace")
    if not isinstance(trace_2, (Trace, pd.DataFrame)):
        raise ValueError(trace_2, "not a trace")

    if len(trace_1) != len(trace_2):
        return False
    else:
        return perspective(trace_1, trace_2, control_flow_attribute)

