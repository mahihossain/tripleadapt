"""
Applies a La Rosa Merge

Notes
_____
Based on [1] La Rosa, M., Dumas, M., Uba, R., & Dijkman, R. (2010, October). Merging business process models.
In OTM Confederated International Conferences" On the Move to Meaningful Internet Systems" (pp. 96-113). Springer,
Berlin, Heidelberg.
"""
import rmm4py.similarity.node_similarities as ns
import networkx as nx
from rmm4py.similarity.similarity_matrix import compute_similarity_matrix_2sets
from scipy.optimize import linear_sum_assignment


def one_to_one_matching(graph1, graph2, sim=ns.semantic_sim(), threshold=0.7):
    """
    Calculates a 1:1 matching based on the similarity matrix.

    Parameters
    ----------
    graph1 : networkX.DiGraph
    graph2 : networkX.DiGraph
    sim : function
        sim can be a node similarity function from rmm/similarity/node_similarities.py
    threshold : float
        only if the similarity between two nodes exceeds this threshold, the assignment is considered for the matching

    Returns
    -------
    dict
        IDs of the nodes of graph2 as keys with the IDs of the matched nodes from graph1 as values

    """
    nodes1 = list(graph1.nodes(data=True))
    nodes2 = list(graph2.nodes(data=True))
    # compute the similarity matrix to find the maximum values for matching
    matrix = compute_similarity_matrix_2sets(nodes1, nodes2, sim)
    # optimization based on scipy
    # https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
    row_ind, col_ind = linear_sum_assignment(matrix, maximize=True)
    matching = {}
    for x, y in zip(row_ind, col_ind):
        if matrix[x, y] >= threshold:
            matching[nodes2[y][0]] = nodes1[x][0]
    return matching


def merge(graph1, graph2, matching=None, sim=None, threshold=0.7):
    """
    Merges two models and returns the union.

    Parameters
    ----------
    graph1 : networkx.DiGraph
    graph2 : networkx.DiGraph
    matching : dict
        1:1 mapping of nodes from graph2 (keys) to graph1 (values).
    sim : function
        sim can be a node similarity function from rmm/similarity/node_similarities.py
    threshold : float

    Returns
    -------
    networkx.DiGraph
    """

    # default is set to semantic sim
    if sim is None:
        sim = ns.semantic_sim()

    if matching is None:
        matching = one_to_one_matching(graph1, graph2, sim, threshold)

    # before relabeling graph2, modify labels of graph1 to preserve different labels.
    # a new attribute namely "label_list" is created to keep record of all labels of nodes merged with this one.
    # key comes from graph2, values from graph1
    for key, value in matching.items():
        # if the reference model graph1 already has a label_list for a node, because it was previously
        # merged, that label list is accessed. Otherwise the label in the name property is accessed.
        try:
            labels = graph1.nodes[value]["label_list"]
        except KeyError:
            label = graph1.nodes[value]["name"]
            labels = [label]
        # check if the node label from the new model is already in the list of node labels in the
        # reference model
        label2 = graph2.nodes[key]["name"]
        if label2 not in labels:
            labels.append(label2)
        # either overwrite or add the new property "label_list" to the node.
        graph1.nodes[value]["label_list"] = labels

    # nodes in graph2 are relabeled with the labels found in the matching.
    graph2_copy = nx.relabel_nodes(graph2, matching, True)
    # Merge process. Attributes of nodes from graph1 take precedence.
    merged_graph = nx.compose(graph1, graph2_copy)

    # adding the color coding for nodes that are present in both models, in the reference only or the new model only.
    for node in merged_graph.nodes():
        if node in matching.values():
            merged_graph.nodes[node]['rgb'] = "red"
        elif node in graph1.nodes():
            merged_graph.nodes[node]['rgb'] = "green"
        elif node in graph2.nodes():
            merged_graph.nodes[node]['rgb'] = "blue"

    return merged_graph
