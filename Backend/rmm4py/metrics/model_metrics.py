"""
Generates metrics for process models
"""
import copy
import math
import networkx as nx
from rmm4py.metrics.mismatch import Mismatch
from rmm4py.metrics.variant_simulation import TraceExtractor
from rmm4py.models.graph_representation.collaboration_model import CollaborationModel
from rmm4py.models.rpst.rpst import RPST
from rmm4py.models.graph_representation.node_types import Gateway


def get_predecessors(node, graph, visited):
    """
    Computes all non-gateway predecessors of a node

    Parameters
    ----------
    node : networkx.Graph.NodeView
        node to get predecessors from
    graph : networkx.DiGraph
        graph the node is contained
    visited : list of networkx.Graph.NodeView
        all currently visited nodes

    Returns
    -------
    predecessors : list of networkx.Graph.NodeView
        all predecessors of the given node
    """

    result = []

    for predecessor in list(graph.predecessors(node)):

        if predecessor in visited:
            continue

        visited.append(predecessor)
        typ = graph.nodes[predecessor]['type']

        if typ in Gateway.__members__ or 'name' not in graph.nodes[predecessor]:
            recursive = get_predecessors(predecessor, graph, visited)

            for n in recursive:
                if n not in result:
                    result.append(n)

        else:
            result.append(predecessor)

    return result


def get_successors(node, graph, visited):
    """
    Computes all non-gateway successors of a node

    Parameters
    ----------
    node : networkx.Graph.NodeDataView
        node to get successors from
    graph : networkx.DiGraph
        graph the node is contained
    visited : list of networkx.Graph.NodeDataView
        all currently visited nodes

    Returns
    -------
    successors : list of networkx.Graph.NodeDataView
        all successors of the given node
    """
    result = []

    for successor in list(graph.successors(node)):

        if successor in visited:
            continue

        visited.append(successor)
        typ = graph.nodes[successor]['type']

        if typ in Gateway.__members__ or 'name' not in graph.nodes[successor]:
            recursive = get_successors(successor, graph, visited)

            for n in recursive:
                if n not in result:
                    result.append(n)

        else:
            result.append(successor)

    return result


def get_node_by_id(id, graph):
    """
    Returns the model including the node

    Parameters
    ----------
    id : string
        node id
    graph : networkx.DiGraph

    Returns
    -------
    node
        the node object, including the type, given the id of the node and the graph its taken from
    """
    for n in graph.nodes(data='type'):

        if n[0] == id:
            return n


def start_events(graph):
    """
    Returns the number of start events

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        number of start_events

    """
    nodelist = [node[1] for node in graph.nodes(data='type')]

    return nodelist.count('startEvent')


def internal_events(graph):
    """
    Returns the number of internal events

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        number of internal_events

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction, and
    guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """

    nodelist = [node[1] for node in graph.nodes(data='type')]

    return nodelist.count('boundaryEvent') + nodelist.count('intermediateThrowEvent') + \
           nodelist.count('intermediateCatchEvent')


def end_events(graph):
    """
    Returns the number of end events

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        number of end_events

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction, and
    guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    nodelist = [node[1] for node in graph.nodes(data='type')]

    return nodelist.count('endEvent')


def events(graph):
    """
    Returns the number of events

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of events

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction, and
    guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    nodelist = [node[1] for node in graph.nodes(data='type') if str(node[1]).endswith('Event')]

    return len(nodelist)


def tasks(graph):
    """
    Returns the number of tasks

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of tasks

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction, and
    guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    nodelist = [node[1] for node in graph.nodes(data='type')]

    return nodelist.count('task')


def and_splits(graph):
    """
    Returns the number of and splits

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of and_splits

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction, and
    guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """

    and_split = [node[1] for node in graph.nodes(data='type') if
                 node[1] == 'parallelGateway' and graph.out_degree(node[0]) > 1]

    return len(and_split)


def and_joins(graph):
    """
    Returns the number of and joins

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of and_joins

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction, and
    guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """

    and_join = [node[1] for node in graph.nodes(data='type') if
                node[1] == 'parallelGateway' and graph.in_degree(node[0]) > 1]

    return len(and_join)


def xor_splits(graph):
    """
    Returns the number of xor splits

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of xor_splits

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """

    xor_split = [node[1] for node in graph.nodes(data='type') if
                 node[1] == 'exclusiveGateway' and graph.out_degree(node[0]) > 1]

    return len(xor_split)


def xor_joins(graph):
    """
    Returns the number of xor joins

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of xor_joins

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    xor_join = [node[1] for node in graph.nodes(data='type') if
                node[1] == 'exclusiveGateway' and graph.in_degree(node[0]) > 1]

    return len(xor_join)


def or_splits(graph):
    """
    Returns the number of or splits

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of or_splits

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    or_split = [node[1] for node in graph.nodes(data='type') if
                node[1] == 'inclusiveGateway' and graph.out_degree(node[0]) > 1]

    return len(or_split)


def or_joins(graph):
    """
    Returns the number of or joins

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of or_joins

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    xor_join = [node[1] for node in graph.nodes(data='type') if
                node[1] == 'inclusiveGateway' and graph.in_degree(node[0]) > 1]

    return len(xor_join)


def connectors(graph):
    """
    Returns the number of connectors

    Parameters
    ----------
    graph : networkx.DiGraph


    Returns
    -------
    int
        number of connectors

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    nodelist = [node[1] for node in graph.nodes(data='type') if str(node[1]).endswith('Gateway')]
    # TODO: would the in Gateway.__Members__ option be faster?

    return len(nodelist)


def nodes(graph):
    """
    Returns the number of nodes

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of nodes

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    return graph.number_of_nodes()


def edges(graph):
    """
    Returns the number of edges

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        number of edges

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    return graph.number_of_edges()


def diameter(graph):
    """
    Returns the diameter

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        the length of the longest path

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """

    # List with endEvents to start the loop with
    endlist = [node[0] for node in graph.nodes(data='type') if node[1] == 'endEvent']

    # List with the connectors to exclude them later
    conlist = [node[0] for node in graph.nodes(data='type') if str(node[1]).endswith('Gateway')]

    # Recursiv function to find the longest path

    def countpaths(nodeslist):
        """
            counts all paths

            Parameters
            ----------
            nodeslist : list

            Returns
            -------
            int
                the max counter
            """
        maxcounter = 1

        for n in nodeslist:
            if n in conlist:
                counter = 0
            else:
                counter = 1

            if (list(graph.predecessors(n)) == []):

                return counter
            else:
                counter = counter + countpaths((list(graph.predecessors(n))))
                if maxcounter < counter:
                    maxcounter = counter
        return maxcounter

    return countpaths(endlist)


def density_1(graph):
    """
    Returns the density 1 according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    float
        the density_1

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.

    """
    return graph.number_of_edges() / (graph.number_of_nodes() * (graph.number_of_nodes() - 1))


def density_2(graph):
    """
    Returns the density 2 according to [1]_

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    float
        density_2

    References
    ==========
    [1] Mendling, J. (2006). Testing density as a complexity metric for EPCs. In German EPC workshop on density of
    process models (Vol. 19).

    """
    if connectors(graph) % 2 == 0:
        cmaxeven = ((connectors(graph) / 2) + 1) ** 2
        dens = (edges(graph) - (nodes(graph) - 1)) / \
               (cmaxeven + (2 * (events(graph) + tasks(graph))) - (nodes(graph) - 1))
    else:
        cmaxodd = (((connectors(graph) - 1) / 2) + 1) ** 2
        dens = (edges(graph) - (nodes(graph) - 1)) / \
               (cmaxodd + (2 * (events(graph) + tasks(graph))) - (nodes(graph) - 1))
    return dens


def density_vogelaar(graph):
    """
    Returns the density according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    float
        density_vogelaar

    References
    ==========
    [1] Vogelaar, J. J. C. L., Verbeek, H. M. W., Luka, B., & van der Aalst, W. M. (2011, August).
    Comparing business processes to determine the feasibility of configurable models: a case study.
    In International Conference on Business Process Management (pp. 50-61). Springer, Berlin, Heidelberg.

    """
    return (edges(graph) - tasks(graph) - events(graph)) / (connectors(graph) * (connectors(graph) - 1))


def coefficient_of_connectivity(graph):
    """
    Returns the coefficient of connectivity according to [1]_

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    float
        ratio of edges to nodes

    References
    ----------
    [1] Latva-Koivisto, A. M. (2001). Finding a complexity measure for business process models.
    Helsinki University of Technology, Systems Analysis Laboratory.
    """
    return graph.number_of_edges() / graph.number_of_nodes()


def coefficient_of_network_complexity(graph):
    """
    Returns the coefficient of network complexity according to [1]_

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    float
        ratio of arcs to the square to nodes

    References
    ----------
    [1] Latva-Koivisto, A. M. (2001). Finding a complexity measure for business process models.
    Helsinki University of Technology, Systems Analysis Laboratory.
    """
    return (graph.number_of_edges() ** 2) / graph.number_of_edges()


def cyclomatic_number(graph):
    """
    Returns the cyclomatic number according to [1]_

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        the number of independent cycles in a graph

    References
    ----------
    [1] Latva-Koivisto, A. M. (2001). Finding a complexity measure for business process models.
    Helsinki University of Technology, Systems Analysis Laboratory.
    """
    return graph.number_of_edges() - graph.number_of_nodes() + 1


# implementation according to Mendling (2008)
def avg_connector_degree(graph):
    """
    Returns the average degree of connectors

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    float
        the number of nodes a connector is in average connected to

    """
    mm = Mismatch(graph)
    mm.sort_cons()

    sum_degrees = 0
    for node in mm.connectors():
        sum_degrees = sum_degrees + mm.degree(node)

    return (1 / connectors(graph)) * sum_degrees


def max_connector_degree(graph):
    """
    Returns the maximum connector degree

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        The maximum degree of a connector

    """
    mm = Mismatch(graph)
    mm.sort_cons()

    max_degree = 0
    for node in mm.connectors():
        if mm.degree(node) > max_degree:
            max_degree = mm.degree(node)

    return max_degree


def cut_vertices(graph):
    """
    Returns the number of cut vertices

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        the number of cut-vertices

    """

    return len(list(nx.articulation_points(graph.to_undirected())))


def separability(graph):
    """
    Returns the separability according to [1]_

    Parameters
    ----------
    graph: collaboration_model
        the process model


    Returns
    -------
    float
        the number of cut-vertices to the number of nodes

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.
    """

    return (cut_vertices(graph)) / (nodes(graph) - 2)


def sequentiality(graph):
    """
    Returns the sequentiality according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    float
        the number of arcs between non-connector nodes divided by the number of arcs.

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.
    """
    counter = 0
    all_edges = edges(graph)
    if all_edges == 0:
        return 0
    edgese = graph.edges()
    type_list = ["inclusiveGateway", "exclusiveGateway", "parallelGateway", "eventBasedGateway", "complexGateway"]
    for edge in edgese:
        start = edge[0]
        end = edge[1]
        type1 = graph.nodes()[start]['type']
        type2 = graph.nodes()[end]['type']
        if type1 in type_list or type2 in type_list:
            continue
        else:
            counter = counter + 1

    return counter / all_edges


def depth(graph):
    """
    Returns the depth of the model according to [1]_

    Parameters
    ----------
    graph : networkx.DiGraph

    Returns
    -------
    int
        the depth of the model

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.
    """
    nodes = graph.nodes(data='type')
    startlist = []
    for node in nodes:
        if node[1] == 'startEvent':
            startlist.append(node[0])
    mm = Mismatch(graph)
    mm.sort_cons()
    splitlist = []
    joinlist = []
    if mm.and_splits():
        splitlist.extend(mm.and_splits())
    if mm.or_splits():
        splitlist.extend(mm.or_splits())
    if mm.xor_splits():
        splitlist.extend(mm.xor_splits())

    if mm.and_joins():
        joinlist.extend(mm.and_joins())
    if mm.or_joins():
        joinlist.extend(mm.or_joins())
    if mm.xor_joins():
        joinlist.extend(mm.xor_joins())

    id_splitlist = []
    id_joinlist = []
    for n in splitlist:
        id_splitlist.append(n[0])
    for n in joinlist:
        id_joinlist.append(n[0])

    def recursiv(no):
        """
        recursive help function
        Parameters
        ----------
        no: node

        Returns
        -------

        """
        counter = 0
        maxcounter = 0

        if (no in id_splitlist):
            counter = counter + 1
        if (no in id_joinlist):
            counter = counter - 1
        if (counter > maxcounter):
            maxcounter = counter
        for succ in graph.successors(no):

            new_max = maxcounter + recursiv(succ)

            if new_max > maxcounter:
                maxcounter = new_max
        return maxcounter

    max_ = 0
    for s in startlist:

        new_max = recursiv(s)
        if new_max > max_:
            max_ = new_max
    return max_


def mismatch(graph):
    """
    Returns the connector mismatch according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        the sum of mismatches for each connector type

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.
    """
    mm = Mismatch(graph)
    mm.sort_cons()
    return mm.mismatch()


def heterogeneity(graph):
    """
    Returns the heterogeneity according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    float
        entropy over the diﬀerent connector types

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.
    """
    mm = Mismatch(graph)
    mm.sort_cons()

    and_num = len(mm.and_joins()) + len(mm.and_splits())
    xor_num = len(mm.xor_joins()) + len(mm.xor_splits())
    or_num = len(mm.or_joins()) + len(mm.or_splits())

    con_num = and_num + xor_num + or_num

    p1 = and_num / con_num
    p2 = xor_num / con_num
    p3 = or_num / con_num

    try:
        r1 = p1 * math.log(p1, 3)
    except ValueError:
        r1 = 0

    try:
        r2 = p2 * math.log(p2, 3)
    except ValueError:
        r2 = 0

    try:
        r3 = p3 * math.log(p3, 3)
    except ValueError:
        r3 = 0

    result = r1 + r2 + r3

    return -1 * result


# TODO implement cyclicity
def cyclicity(graph):
    """
        Returns the number cyclicity

        Parameters
        ----------
        graph: networkx.DiGraph

    """

    pass


def token_splits(graph):
    """
    Returns the number of token splits according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        the sum of the output-degree of AND-joins and OR-joins minus one

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.
    """
    mm = Mismatch(graph)
    mm.sort_cons()

    result = 0

    for conn in mm.and_splits():
        result = result + (mm.out_degree(conn) - 1)

    for conn in mm.or_splits():
        result = result + (mm.out_degree(conn) - 1)

    return result


def control_flow_complexity(graph):
    """
    Returns the control flow complexity according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        the control flow complexity as an integer

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.
    """
    mm = Mismatch(graph)
    mm.sort_cons()

    sum_and = len(mm.and_splits())
    sum_xor = 0
    sum_or = 0

    for conn in mm.xor_splits():
        sum_xor = sum_xor + mm.out_degree(conn)

    for conn in mm.or_splits():
        sum_or = sum_or + (2 ** mm.out_degree(conn)) - 1

    return sum_and + sum_xor + sum_or


def join_complexity(graph):
    """
    Returns the join complexity according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    float
        The sum of the join connectors weighted by the paths they join

    References
    ==========
    [1] Mendling, J. (2008). Metrics for process models: empirical foundations of verification, error prediction,
    and guidelines for correctness (Vol. 6). Springer Science & Business Media.
    """
    mm = Mismatch(graph)
    mm.sort_cons()

    sum_and = len(mm.and_joins())
    sum_xor = 0
    sum_or = 0

    for conn in mm.xor_joins():
        sum_xor = sum_xor + mm.in_degree(conn)

    for conn in mm.or_joins():
        sum_or = sum_or + (2 ** mm.in_degree(conn)) - 1

    return sum_and + sum_xor + sum_or


def rpst_polygons(graph):
    """
    Returns the amount of rpst polygons

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        the number of rpst polygons
    """
    rpst = RPST(graph)
    return len(rpst.fragments("polygon", data=True))


def rpst_bonds(graph):
    """
    Returns the amount of rpst bonds

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        the number of rpst bonds
    """
    rpst = RPST(graph)
    return len(rpst.fragments("bond", data=True))


def rpst_rigids(graph):
    """
    Returns the amount of rpst rigids

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        the number of rpst elements

    """

    rpst = RPST(graph)
    return len(rpst.fragments("rigid", data=True))


def weighted_coupling(graph):
    """
    Returns the weighted coupling according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    float
        number of all pairs of activities in a process model that are connected to each other with their weights

    References
    ----------
    [1] Vanderfeesten, I. T., Cardoso, J. S., & Reijers, H. A. (2007). A weighted coupling metric for
    business process models. In CAiSE Forum (Vol. 247, pp. 41-44).
    """

    def equal(nodetype):
        """
        Checks for equal type of node

        Parameters
        ----------
        nodetype: string
            the enum type of a node


        Returns
        -------
        String
            equals the event and function related types


        """
        switcher = {
            "function": "task",
            "task": "task",
            "userTask": "task",
            "serviceTask": "task",
            "manualTask": "task",
            "sendTask": "task",
            "receiveTask": "task",
            "event": "task",
            "startEvent": "task",
            "intermediateCatchEvent": "task",
            "endEvent": "task",
            "intermediateThrowEvent": "task",
            "boundaryEvent": "task",
            "inclusiveGateway": "inclusiveGateway",
            "exclusiveGateway": "exclusiveGateway",
            "parallelGateway": "parallelGateway",
            "eventBasedGateway": "eventBasedGateway",
            "complexGateway": "complexGateway",
        }
        return switcher.get(nodetype, "no valid task")

    def recursiv(nodelist):
        """
        Recursively calculates the weight if each node

        Parameters
        ----------
        nodelist: string list
            list of node_ids


        Returns
        -------
        float
            calculated weight of each node


        """
        counter = 0

        for node in nodelist:

            thistype = equal(get_node_by_id(node, graph)[1])
            if thistype == 'inclusiveGateway':
                ## OR SPLIT
                m = len(list(graph.predecessors(node)))
                n = len(list(graph.successors(node)))

                formula = 1 / ((2 ** m - 1) * (2 ** n - 1)) + ((2 ** m - 1) * (2 ** n - 1) - 1) / \
                          ((2 ** m - 1) * (2 ** n - 1)) * 1 / (m * n)

                counter = counter + n * m * formula + recursiv(list(graph.successors(node)))

            if thistype == 'exclusiveGateway':
                ## XOR split
                m = len(list(graph.predecessors(node)))
                # m ingoing arcs
                n = len(list(graph.successors(node)))
                # n outgoing arcs
                formula = 1 / (m * n)
                counter = counter + n * m * formula + recursiv(
                    list(graph.successors(node)))
                # *n for each outgoing arch

            if thistype == 'parallelGateway':
                ## AND split
                m = len(list(graph.predecessors(node)))
                # m ingoing arcs
                n = len(list(graph.successors(node)))
                # n outgoing arcs
                counter = counter + n * m * 1 + recursiv(list(graph.successors(node)))

            k = list(graph.predecessors(node))[0]

            typebefore = equal(get_node_by_id(k, graph)[1])

            if (thistype == 'task' and typebefore == 'task'):
                nodebefore = get_node_by_id(list(graph.predecessors(node))[0], graph)

                if (node != nodebefore):
                    counter = counter + 1 + recursiv(list(graph.successors(node)))
                else:
                    counter = counter + 0 + recursiv(list(graph.successors(node)))
            tuplee = ['inclusiveGateway', 'exclusiveGateway', 'parallelGateway']
            if thistype == 'task' and typebefore in tuplee:
                counter = counter + 0 + recursiv(list(graph.successors(node)))

        return counter

    nodes = graph.nodes(data='type')

    starteventlist = []
    for n in nodes:
        if n[1] == 'startEvent':
            starteventlist.append(n[0])
    startlist = []

    for n in starteventlist:
        # get the succesors since the startevents dont count

        startlist.extend(list(graph.successors(n)))
    startlist = list(dict.fromkeys(startlist))
    # remove duplicates

    T = tasks(graph) + events(graph)
    return recursiv(startlist) / (T * (T - 1))


def cross_connectivity(graph):
    """
    Returns the cross connectivity according to [1]_

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    float
        the maximal weights for any path between every
        two nodes and divided by the number of paths between
        every two nodes

    References
    ----------
    [1] Vanderfeesten, I., Reijers, H. A., Mendling, J., van der Aalst,
    W. M., & Cardoso, J. (2008, June). On a quest for good process models:
     the cross-connectivity metric. In International Conference on Advanced
     Information Systems Engineering (pp. 480-494). Springer,
     Berlin, Heidelberg.
    """
    mm = Mismatch(graph)
    mm.sort_cons()

    def edge_list(pathlist):
        """
        Returns a list of edges given a certain path

        Parameters
        ----------
        pathlist: node list list
            list of paths


        Returns
        -------
        list
            a list of edge_paths given a list of node_paths


        """
        list_ = []
        for i in range(0, len(pathlist) - 1):
            edge = graph[pathlist[i]][pathlist[i + 1]]['id']
            list_.append(edge)
        return list_

    def weight_of_node(node):
        """
        Returns the weight of the node

        Parameters
        ----------
        node: node
            node object

        Returns
        -------
        float
            the weight of a node

        """
        switcher = {
            "inclusiveGateway": 1 / (2 ** mm.degree(node) - 1) + (2 ** mm.degree(node) - 2) /
                                (2 ** mm.degree(node) - 1) * 1 / mm.degree(node),
            "exclusiveGateway": 1 / mm.degree(node),
            "parallelGateway": 1,
            "task": 1,
            "function": 1,
            "userTask": 1,
            "serviceTask": 1,
            "manualTask": 1,
            "sendTask": 1,
            "receiveTask": 1,
            "event": 1,
            "startEvent": 1,
            "intermediateCatchEvent": 1,
            "endEvent": 1,
            "intermediateThrowEvent": 1,
            "boundaryEvent": 1,

        }
        return switcher.get(node[1], "no matching type")

    def max_weight_paths(pathlist):
        """
        Returns the max weight found in the list of paths

        Parameters
        ----------
        pathlist: node list list
            list with paths


        Returns
        -------
        float
            the max. weight found in list of paths

        """
        max_weight = 0
        current_weight = 1
        for path in pathlist:
            edge_path = edge_list(path)

            for i, item in enumerate(edge_path):
                current_weight = current_weight * edge_dict.get(item)
            if (current_weight > max_weight):
                max_weight = current_weight
        return max_weight

    nodeslist = graph.nodes()

    edges = graph.edges(data='id')
    edge_dict = {}
    # create empty dictionary
    for tuple in edges:
        # fills the dict with edges and their value
        firstnode = get_node_by_id(tuple[0], graph)
        secondnode = get_node_by_id(tuple[1], graph)
        edge_id = tuple[2]
        weight_edge = weight_of_node(firstnode) * weight_of_node(secondnode)
        edge_dict[edge_id] = weight_edge
    # f = list(nx.all_simple_paths(model.process_graph, 'A', 'or'))
    # print(f)

    resultcounter = 0
    # sum up matrix

    for n1 in nodeslist:
        for n2 in nodeslist:
            all_path_list = list(nx.all_simple_paths(graph, n1, n2))

            max_weight = max_weight_paths(all_path_list)
            resultcounter = resultcounter + max_weight

    return resultcounter / (nodes(graph) * (nodes(graph) - 1))


def process_variants(graph):
    """
    Returns the amount of process variants

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        number of process variants


    """
    graph2 = copy.deepcopy(graph)
    model = CollaborationModel()
    model.process_graph = graph2
    trace_ex = TraceExtractor(model, "Xor")
    traces = trace_ex.main(trace_ex.get_entry_nodes())
    return len(traces)


# TODO implement number_cycles_multiple
def number_cycles_multiple(graph):
    """
       Returns the number of multiple cycles

       Parameters
       ----------
       graph: networkx.DiGraph

    """
    pass


def number_cycles_single(graph):
    """
    Returns the amount of single cycles

    Parameters
    ----------
    graph: networkx.DiGraph

    Returns
    -------
    int
        number of single cycles


    """
    return len(list(nx.simple_cycles(graph)))


def number_graph_components(graph):
    """
    Returns the amount of graph components

    Parameters
    ----------
        graph : networkx.DiGraph


    Returns
    -------
    int
        The number of independent graph components

    """
    return nx.number_weakly_connected_components(graph)


# TODO implement structuredness
def structuredness(graph):
    """
       Returns the structuredness

       Parameters
       ----------
       graph: networkx.DiGraph

    """
    pass


def alternating(graph):
    """
    Returns the node that is followed by a node of the same type

    Parameters
    ----------
    graph : networkx.DiGraph


    Returns
    -------
    node
        the node that is followed by a node of same type or None if such a node does not exist

    """
    events = []
    functions = []
    nodes = graph.nodes(data='type')
    for node in nodes:
        if (node[1] == 'startEvent' or node[1] == 'boundaryEvent' or node[1] == 'intermediateThrowEvent'
                or node[1] == 'intermediateCatchEvent' or node[1] == 'endEvent'):
            events.append(node[0])
        if (node[1] == 'task' or node[1] == "function" or node[1] == "userTask" or node[1] == "serviceTask"
                or node[1] == "manualTask" or node[1] == "sendTask" or node[1] == "receiveTask"):
            functions.append(node[0])

    def sucnode(node, nodetype):
        """
        Returns a list of successor nodes of the given node and type

        Parameters
        ----------
        node
            the given node
        nodetype
            the type of the given node
        Returns
        -------
        the successor node
        """
        suc = list(graph.successors(node))
        return_node = node
        for s in suc:
            if s not in events and s not in functions:
                return_node = sucnode(s, nodetype)
            else:
                if s in events and nodetype == "Event":
                    return return_node
                if s in functions and nodetype == "Function":
                    return return_node
        return None

    for event in events:
        return_node = sucnode(event, "Event")
        if return_node is not None:
            return return_node, "Event"
    for function in functions:
        return_node = sucnode(function, "Function")
        if return_node is not None:
            return return_node, "Function"

    return None
