"""Function creates the similarities of two models without matching."""

import rmm4py.similarity.word_similarities as ws
import rmm4py.similarity.node_similarities as ns
import copy
from rmm4py.models.graph_representation.node_types import Gateway, Event, Task


def __compute_nodes_edges(graph, events, tasks, gateways):
    """
    Function that calculates a new graph as well as the nodes and edges, including and excluding specified node types.

    Parameters
    ----------
    graph : networkx.DiGraph
    events : bool
    tasks : bool
    gateways : bool

    Notes
    -----
    Node types with the value True are included in the graph and the list, new edges are drawn between the successors
    and predecessors of removed nodes.

    Returns
    -------
    graph : networkx.DiGraph
    list : list of networkx.DiGraph.nodes
    list : list of networkx.DiGraph.edges

    """
    # if every node type is included, the graph is returned unchanged.
    if events and tasks and gateways:
        nodes = list(graph.nodes(data=True))
        edges = list(graph.edges)
        return graph, nodes, edges

    else:

        alternative_graph = copy.deepcopy(graph)

        all_nodes = list(alternative_graph.nodes(data=True))

        # for all nodes of the deepcopy it is checked whether they belong to a type that should be removed.
        # if so, the node is removed and new edges are drawn between the predecessors and successors.
        for node in all_nodes:

            typ = node[1]['type']

            if typ in Event.__members__ and not events \
                    or typ in Task.__members__ and not tasks \
                    or typ in Gateway.__members__ and not gateways:

                predecessors = list(alternative_graph.predecessors(node[0]))
                successors = list(alternative_graph.successors(node[0]))

                alternative_graph.remove_node(node[0])

                for predecessor in predecessors:
                    for successor in successors:
                        alternative_graph.add_edge(predecessor, successor)

        return alternative_graph, list(alternative_graph.nodes(data=True)), list(alternative_graph.edges)


def __create_matching(graph1, graph2, sim, threshold):
    """
    Function creates a matching between the lists of nodes of two graphs with a given similarity method above a certain
    threshold. Returns matching as a dictionary including the nodes as keys and values and the value of the similarity.

    Parameters
    ----------
    graph1 : networkx.DiGraph
    graph2 : networkx.DiGraph
    sim : similarity method without parameters
        If None, equal label similarity will be used.
    threshold : float
                Value between 0 and 1.

    Returns
    -------
    dict

    Notes
    -----
    Matched nodes from both graphs are returned as keys and values.

    """

    if sim is None:
        sim = ns.equal_label_sim()

    matching = {}

    graph1_nodes = list(graph1.nodes(data=True))
    graph2_nodes = list(graph2.nodes(data=True))

    for node1 in graph1_nodes:

        for node2 in graph2_nodes:

            sim_n1_n2 = sim(node1, node2)

            if sim_n1_n2 >= threshold:

                if node1[0] in matching:
                    matching[node1[0]].append((node2[0], sim_n1_n2))

                    new_match_inverted = (node1[0], sim_n1_n2)
                    if node2[0] in matching:
                        matching[node2[0]].append(new_match_inverted)
                    else:
                        matching[node2[0]] = [new_match_inverted]

                else:
                    matching[node1[0]] = [(node2[0], sim_n1_n2)]
                    matching[node2[0]] = [(node1[0], sim_n1_n2)]

    return matching


def __is_matched(node_id1, node_id2, matching):
    """
    Function checks for two nodes if they are defined as a match in the matching.

    Parameters
    ----------
    node_id1 : networkx.DiGraph.node
    node_id2 : networkx.DiGraph.node
    matching : dict

    Returns
    -------
    bool

    """

    if matching.keys() >= {node_id1, node_id2}:

        for match in matching[node_id1]:
            match_node = match[0]
            if match_node == node_id2:
                return True

    return False


def __compute_sn(graph1_nodes, graph2_nodes, matching):
    """
    Function splits a list of all nodes from two graphs into a list containing the matched nodes and a list containing
    the nodes that were not matched.

    Parameters
    ----------
    graph1_nodes : list of networkx.DiGraph.nodes or networkx.DiGraph
    graph2_nodes : list of networkx.DiGraph.nodes or networkx.DiGraph
    matching : dict

    Returns
    -------
    list, list
        list of matched nodes, list of unmatched nodes

    """
    all_nodes = list(copy.deepcopy(graph1_nodes))
    all_nodes.extend(graph2_nodes)

    node_ids = [x[0] for x in all_nodes]
    sub = [node_id for node_id in node_ids if node_id in matching]

    sn = [node_id for node_id in node_ids if node_id not in sub]

    return sub, sn


def __compute_se(graph1_edges, graph2_edges, matching):
    """
    Function splits a list of all edges from two graphs into a list containing the matched edges and a list containing
    the edges that were not matched.

    Parameters
    ----------
    graph1_edges : list of networkx.DiGraph.edges
    graph2_edges : list of networkx.DiGraph.edges
    matching : dict

    Returns
    -------
    list, list
        list of matched edges, list of unmatched edges
    """

    sub = []

    for edge1 in graph1_edges:

        for edge2 in graph2_edges:

            if edge2 in sub:
                continue

            edge1_1 = edge1[0]
            edge1_2 = edge1[1]
            edge2_1 = edge2[0]
            edge2_2 = edge2[1]

            if __is_matched(edge1_1, edge2_1, matching) \
                    and __is_matched(edge1_2, edge2_2, matching):
                sub.append(edge1)
                sub.append(edge2)
                break

    all_edges = list(copy.deepcopy(graph1_edges))
    all_edges.extend(graph2_edges)

    se = [x for x in all_edges if x not in sub]

    return sub, se


def common_percentage_sim(matching=None, sim=None, threshold=1.00, nodes=True, edges=False, events=True, tasks=True,
                          gateways=False):
    """
    Function returns the function calculate_common_percentage which just requires two graphs as inputs,
    with other parameters set.

    Parameters
    ----------
    matching : dict, optional
        If None, a matching is created by create_matching
    sim : similarity method, optional
         If None, equal label similarity will be used.
    threshold : float, optional
        Default is 1.00
    nodes : bool
        Default True
    edges : bool
        Default False
        These booleans let the user define whether just nodes, just edges or both should be compared.
    events : bool
    tasks : bool
    gateways : bool
        These booleans define which node types will be taken into account.

    Returns
    -------
    function
    """

    def calculate_common_percentage_similarity(graph1, graph2):
        """
        Function calculates the percentage of matched nodes of defined types and/or edges of two graphs and returns
        a similarity value between 0 and 1.

        Parameters
        ----------
        graph1 : networkx.DiGraph
        graph2 : networkx.DiGraph

        Returns
        -------
        float
            Value between 0 and 1

        See Also
        --------
        create_matching
        compute_sn
        compute_se

        """

        alt_graph2, graph1_nodes, graph1_edges = __compute_nodes_edges(graph1, events, tasks,
                                                                       gateways)
        alt_graph1, graph2_nodes, graph2_edges = __compute_nodes_edges(graph2, events, tasks,
                                                                       gateways)

        nonlocal matching
        if matching is None:
            matching = __create_matching(alt_graph1, alt_graph2, sim, threshold)

        if nodes:
            sub_n, sn = __compute_sn(graph1_nodes, graph2_nodes, matching)
            common_nodes = len(sub_n) / (alt_graph1.number_of_nodes() + alt_graph2.number_of_nodes())

            if edges:
                sub_e, se = __compute_se(graph1_edges, graph2_edges, matching)
                common_edges = len(sub_e) / (alt_graph1.number_of_edges() + alt_graph2.number_of_edges())

                return (common_nodes + common_edges) / 2
            else:
                return common_nodes

        elif edges:
            sub_e, se = __compute_se(graph1_edges, graph2_edges, matching)
            common_edges = len(sub_e) / (alt_graph1.number_of_edges() + alt_graph2.number_of_edges())
            return common_edges

        return 0

    return calculate_common_percentage_similarity


def node_matching_sim(matching=None, sim=None, threshold=1.00, events=True, tasks=True, gateways=False):
    """
    Returns calculate_node_matching_similarity function which just requires two graphs as input, with the rest of the
    parameters set.

    Parameters
    ----------
    matching : dict, optional
        Either matching or threshold need to have a value.
    sim : label similarity measurement method
    threshold : float, optional
        Only necessary, if no matching is given
        Default is 1.0
    events : bool
        Default is True
    tasks : bool
        Default is True
    gateways : bool
        Default is False
        These booleans define which node types will be taken into account.

    Returns
    -------
    function
    """

    def calculate_node_matching_similarity(graph1, graph2):
        """
        Function sums up the similarity values of matched nodes of specific types. If no matching is passed,
        one is created with create_matching and the passed threshold.

        Parameters
        ----------
        graph1 : networkx.DiGraph
        graph2 : networkx.DiGraph

        Returns
        -------
        float
            Value between 0 and 1.

        References
        ----------
        [1] R. Dijkman et al., "Similarity of business process models: Metrics and evaluation", Information Systems,
        vol. 36, pp. 498-516, 2011.

        """
        alt_graph1, graph1_nodes, graph1_edges = __compute_nodes_edges(graph1, events, tasks,
                                                                       gateways)
        alt_graph2, graph2_nodes, graph2_edges = __compute_nodes_edges(graph2, events, tasks,
                                                                       gateways)
        node_matching_similarity = 0

        nonlocal sim
        if sim is None:
            sim = ns.bag_of_words_sim()

        nonlocal matching
        if matching is None:
            node_matching_sim.matching = __create_matching(alt_graph1, alt_graph2, sim, threshold)

        if node_matching_sim.matching is not None:

            sum_label_similarity_scores = 0

            # for all combinations of nodes the similarities of the matched nodes are summed up
            for node1 in graph1_nodes:

                for node2 in graph2_nodes:

                    if __is_matched(node1[0], node2[0], node_matching_sim.matching):
                        sum_label_similarity_scores += sim(node1, node2)
                        break

            # normalization of node matching similarity
            node_matching_similarity = 2 * sum_label_similarity_scores\
                / (graph1.number_of_nodes() + graph2.number_of_nodes())

        else:
            print("No calculation of node matching similarity possible")

        return node_matching_similarity

    return calculate_node_matching_similarity


def graph_edit_dist(matching=None, sim=None, threshold=1.00, events=True, tasks=True, gateways=False):
    """
    Function returns calculate_graph_edit_distance function which just requires two graphs as arguments, with the rest
    of the parameters set.

    Parameters
    ----------
    matching : dict, optional
        Any previously performed matching can be added here.
        Default is None.
        If None, matching is created.
    sim : similarity method, optional
        Default is None.
        If None, the equal label similarity is used.
    threshold : float, optional
        Value between 0 and 1.
        Default is 1.0.
    events : bool, optional
        Default is True.
    tasks : bool, optional
        Default is True.
    gateways : bool, optional
        Default is False.
        The boolean values events, tasks and gateways allow the user to include or exclude these from the further
        measuring of similarities

    Returns
    -------
    function

    References
    ----------
    [1] R. Dijkman et al., "Similarity of business process models: Metrics and evaluation", Information Systems,
    vol. 36, pp. 498-516, 2011.
    """

    matching_new = matching
    sim_new = sim

    def calculate_graph_edit_distance(graph1, graph2):
        """
        Function computes the graph edit distance, normalized to the number of nodes in the two graphs in total.

        Parameters
        ----------
        graph1 : networkx.DiGraph
        graph2 : networkx.DiGraph

        Returns
        -------
        float
            Normalized value for the distance between 0 and 1.

        References
        ----------
        [1] R. Dijkman et al., "Similarity of business process models: Metrics and evaluation", Information Systems,
        vol. 36, pp. 498-516, 2011.


        """

        alt_graph1, graph1_nodes, graph1_edges = __compute_nodes_edges(graph1, events, tasks, gateways)
        alt_graph2, graph2_nodes, graph2_edges = __compute_nodes_edges(graph2, events, tasks, gateways)

        nonlocal matching_new
        nonlocal sim_new
        if matching_new is None:
            matching_new = __create_matching(alt_graph1, alt_graph2, sim_new, threshold)

        sub_n, sn = __compute_sn(graph1_nodes, graph2_nodes, matching_new)
        sub_e, se = __compute_se(graph1_edges, graph2_edges, matching_new)

        snv = len(sn) / (len(list(graph1_nodes)) + len(list(graph2_nodes)))
        if not graph1_edges and not graph2_edges:
            sev = 0
        else:
            sev = len(se) / (len(list(graph1_edges)) + len(list(graph2_edges)))

        sbv = 0

        for matched_node in matching_new:
            sim = matching_new[matched_node][0][1]
            sbv = sbv + (1 - sim)

        if sbv != 0:
            sbv = sbv / (alt_graph1.number_of_nodes() + alt_graph2.number_of_nodes() - len(sn))

        distance = (snv + sev + sbv) / 3

        return distance

    return calculate_graph_edit_distance


def graph_edit_dist_sim(matching=None, sim=None, threshold=1.0, events=True, tasks=True, gateways=False):
    """
    Function returns function calculate_graph_edit_distance_similarity, which just requires two graphs as input,
    with other parameters set.

    Parameters
    ----------
    matching : dict, optional
        Any previously performed matching can be added here.
        Default is None.
        If None, matching is created.
    sim : similarity method, optional
        Default is None.
        If None, the equal label similarity is used.
    threshold : float, optional
        Value between 0 and 1.
        Default is 1.0.
    events : bool, optional
        Default is True.
    tasks : bool, optional
        Default is True.
    gateways : bool, optional
        Default is False.
        The boolean values events, tasks and gateways allow the user to include or exclude these from the further
        measuring of similarities

    Returns
    -------
    function
    """

    def calculate_graph_edit_distance_similarity(graph1, graph2):
        """
        Function computes the graph_edit_dist_sim of two networkx.DiGraphs based on the compute_graph_edit_distance
         method.

        Parameters
        ----------
        graph1 : networkx.DiGraph
        graph2 : networkx.DiGraph

        Returns
        -------
        float
            Similarity value between 0 and 1.

        See Also
        --------
        compute_graph_edit_distance

        """
        dist_fun = graph_edit_dist(matching, sim, threshold, events, tasks, gateways)
        return 1 - dist_fun(graph1, graph2)

    return calculate_graph_edit_distance_similarity


def feature_based_sim(label_sim_outer=None, threshold_labels_high=1.0, threshold_labels_medium=0.6,
                      threshold_roles=1.0, discriminative_cutoff=0.5, events=True, tasks=True,
                      gateways=False):
    """
    Functions returns the function calculate_feature_based_similarity just requires two graphs as inputs,
    with other parameters set.

    Parameters
    ----------
    label_sim_outer : similarity method, optional
        similarity measure to compare node labels as two strings, if None it will be set to the Levenshtein distance.
    threshold_labels_high : float, optional
        Threshold of label similarity for which nodes will be considered corresponding wo further tests.
        Value between 0 and 1, default is one.
    threshold_labels_medium : float, optional
        If this threshold is met, nodes are considered corresponding iff the role_sim similarity is equal or above
        threshold_roles.
        Value between 0 and 1, lower than threshold_labels_high.
        Default is 0.6.
    threshold_roles : float, optional
        Threshold for the role_sim similarity.
        Default is 1.0.
    discriminative_cutoff : float, optional
        Node roles that are very frequent in the process models lack discriminative power. If the fraction of nodes with
        a specific role_sim exceeds the specified cutoff, the nodes will no longer be considered for the determination
        of the role_sim similarity.
        Default is 0.5.
    events : bool
        Default is True.
    tasks : bool
        Default is True.
    gateways : bool
        Default is False.
        The boolean values events, tasks and gateways allow the user to include or exclude these from the further
        measuring of similarities

    Returns
    -------
    function
    """
    label_sim = label_sim_outer

    def calculate_feature_based_similarity(graph1, graph2):
        """
        Function computes feature based similarity as described by Yan et al. (2010). Similarity of two process models
        is determined by comparing the labels of two nodes in a first step. If the high threshold is met, the nodes are
        considered as corresponding, if the medium threshold is met and the nodes exhibit similar role_sim features and
        discriminative roles, the nodes are also considered as corresponding nodes. The fraction of corresponding nodes
        wrt the total number of nodes is the similarity.
        This variant is the node-based variant and the implemented features are the node labels and the node roles.

        Parameters
        ----------
        graph1 : networkx.DiGraph
            graphical representation of a Process Model
        graph2 : networkx.DiGraph
            graphical representation of a second Process Model

        Returns
        -------
        float
            Similarity value between 0 and 1.

        Notes
        -----
        The thresholds all have default values. However, adjustment is highly recommended.
        Nodes without the attribute "name" will not be matched.

        References
        ----------
        [1] Z. Yan, R. Dijkman and P. W. P. J. Grefen, "Fast Business Process Similarity Search with Feature-Based
        Similarity Estimation",
        In R. Meersman, T. Dillon and P. Herrero (Eds.), Proceedings of the 18th international conference on cooperative
        information systems (Vol. 1, pp. 60-77). (Lecture Notes in Computer Science; Vol. 6426), 2010.
        DOI: 10.1007/978-3-642-16934-2_8

        """
        # computes alternative graphs including only the types of nodes specified by the user.
        graph1, _, _ = __compute_nodes_edges(graph1, events, tasks, gateways)
        graph2, _, _ = __compute_nodes_edges(graph2, events, tasks, gateways)

        # list of corresponding nodes
        corr_nodes = []

        # if no similarity was chosen, the levenshtein_sim similarity is set.
        nonlocal label_sim
        if label_sim is None:
            label_sim = ws.levenshtein_sim()

        # role_sim similarity function is mapped.
        rs = ns.role_sim([graph1, graph2], discriminative_cutoff)

        # checks for every combination of nodes, if they can be matched. If they can be matched,
        # they are added to the list of corresponding nodes. 1:n matches are possible, but every node will just be
        # added once to corr_nodes
        for node1 in graph1.nodes(data=True):

            for node2 in graph2.nodes(data=True):

                levenshtein = 0

                if 'name' in node1[1] and 'name' in node2[1]:
                    label1 = node1[1].get('name', "")
                    label2 = node2[1].get('name', "")
                    levenshtein = label_sim(label1, label2)

                if levenshtein >= threshold_labels_high:

                    if (node1, 1) not in corr_nodes:
                        corr_nodes.append((node1, 1))
                    if (node2, 2) not in corr_nodes:
                        corr_nodes.append((node2, 2))

                elif levenshtein >= threshold_labels_medium:

                    rdsim = rs(node1, node2)

                    if rdsim >= threshold_roles:

                        if (node1, 1) not in corr_nodes:
                            corr_nodes.append((node1, 1))
                        if (node2, 2) not in corr_nodes:
                            corr_nodes.append((node2, 2))

        # The similarity measure is the fraction of matched nodes of the total amount of nodes.
        return len(corr_nodes) / (graph1.number_of_nodes() + graph2.number_of_nodes())

    return calculate_feature_based_similarity
