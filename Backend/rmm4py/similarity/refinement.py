"""
Functions regarding trace refinements
"""
import string
import difflib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from rmm4py.similarity.equals import control_flow
from rmm4py.event_logs.event_log import Trace


def compute(trace_1, trace_2):
    """
    Check if one trace is an refinement of another, i.e. they have a common subsequence of activities
    (control-flow only).
    True if one sequence can be transformed to the other only by inserting activities.

    0 if not refinement
    1 if completely equal
    1 - (#insertion/max(trace length)) otherwise

    For example:
    trace_1 = a, b, c, h, i ,j
    trace_2 = a, b, c, d, e, f, h, i ,j
    returns 3/9

    while
    trace_1 = a, b, c, h, i, j
    trace_2 = a, b, c, d, e, f
    returns 0


    Parameters
    ----------
    trace_1:    Trace
                Input trace 1

    trace_2:    Trace
                Input trace 2

    Returns
    -------
    int
                similarity as a score between 0 and 1

    """

    """Check for equal control flow"""
    if control_flow(trace_1, trace_2):
        return 1

    diff = differences(trace_1, trace_2)

    """None signals that no difference could be computed"""
    if diff is None:
        return 0

    added = diff[0]
    deleted = diff[1]

    if len(deleted) > 0:
        return 0

    return 1 - (len(added) / max(len(trace_1), len(trace_2)))


def differences(trace_1, trace_2):
    """
    Compute the difference between trace 1 and trace 2, i.e. what insertions or deletions are required to
    transform 1 into 2.
    If the shorter trace cannot be transformed into the other simply be adding events, False is returned to signal
    a problem.
    Otherwise, the list of activities required will be returned.

    Parameters
    ----------
    trace_1:    Trace
                Input trace 1

    trace_2:    Trace
                Input trace 2

    Returns
    -------
    Tuple of lists: list
                Two lists. The first one with the activities required to add to the trace and the second with activities


    """

    if isinstance(trace_1, (Trace, pd.DataFrame)):
        """If trace is empty, return False, too. Should be überdacht werden"""
        cf_trace_1 = trace_1["concept:name"].values.tolist()

    else:
        raise ValueError(trace_1, "not a trace")

    if isinstance(trace_2, (Trace, pd.DataFrame)):
        cf_trace_2 = trace_2["concept:name"].values.tolist()

    else:
        raise ValueError(trace_2, "not a trace")

    le = LabelEncoder()
    le.fit(cf_trace_1 + cf_trace_2)

    cf_trace_1 = le.transform(cf_trace_1)
    cf_trace_2 = le.transform(cf_trace_2)

    """
    if len(cf_trace_1) == len(cf_trace_2):
        if cf_trace_1 != trace_2:
            return False
    """

    if len(cf_trace_2) > len(cf_trace_1):
        short_trace = cf_trace_1
        long_trace = cf_trace_2
    else:
        short_trace = cf_trace_2
        long_trace = cf_trace_1

    """Encode all activities as a characters as the latter diff comparison works on characters only"""
    activity_dict = {int(i): s for i, s in enumerate(string.printable)}
    if len(le.classes_) > len(activity_dict.keys()):
        raise ValueError("Too many different activities, not supported")

    short_trace = [str(activity_dict[int(i)]) + "\n" for i in short_trace]
    long_trace = [str(activity_dict[int(i)]) + "\n" for i in long_trace]

    deleted = []
    added = []

    """
    Use the difflib library for comparing the two sequences of characters representing activities
    Empty ' ' signals that both sequences are equal at this point, '-' signals that a deletion is required and
    '+' signals that a insertion is required.
    """

    for i, s in enumerate(difflib.ndiff(short_trace, long_trace)):
        #print(s)
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            d = int(list(activity_dict.keys())[list(activity_dict.values()).index(s[2])])
            deleted.append(str(le.inverse_transform([d])[0]))
            # print(u'Delete "{}" from position {}'.format(le.inverse_transform([int(s[-1])]), i))
        elif s[0] == '+':
            a = int(list(activity_dict.keys())[list(activity_dict.values()).index(s[2])])
            added.append(str(le.inverse_transform([a])[0]))
            # print(u'Add "{}" to position {}'.format(le.inverse_transform([int(s[-1])]), i))

    return added, deleted
