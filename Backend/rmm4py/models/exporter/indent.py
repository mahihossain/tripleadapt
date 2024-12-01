""" function for indent of petrinet, bpmn and epc exporter. """


def indent(elem, level=0, more_sibs=False):
    """
    Indents an element in the epml file based on a given level

    Parameters
    ----------
    elem : ET XML element
        element to indent

    level : int
        level of indent

    more_sibs : bool

    Returns
    -------
    indented_elem :  ET XML element
        the indented element
    """
    i = "\n"
    if level:
        i += (level-1) * '  '
    num_kids = len(elem)
    if num_kids:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
            if level:
                elem.text += '  '
        count = 0
        for kid in elem:
            indent(kid, level + 1, count < num_kids - 1)
            count += 1
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            if more_sibs:
                elem.tail += '  '
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            if more_sibs:
                elem.tail += '  '
