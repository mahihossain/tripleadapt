"""
Compares the length of two traces
"""


def trace_len_compare(trace1, trace2):
    """
        Compares the length of two traces

        Parameters
        ----------
        trace1: list of tasks
        trace2: list of tasks


        Returns
        -------
        int
            1 if trace1 is greater than trace2
            -1 if trace1 is s smaller than trace2
            0 if equal


    """

    len1 = len(trace1)
    len2 = len(trace2)
    if (len1 == len2):
        return 0
    if (len1 < len2):
        return -1
    else:
        return 1
