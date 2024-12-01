"""
Utils for process models
"""
from rmm4py.models.graph_representation.node_types import Gateway, Event
import uuid


def syntactical_fix(graph):
    """
    Syntactically fixes a given process model, so that each node has not multiple inputs AND outputs
    Parameters
    ----------
    graph : nx.DiGraph
        graph to fix
    """
    all_nodes = list(graph.nodes)

    for node in all_nodes:
        if graph.has_node(node):
            predecessors = list(graph.predecessors(node))
            successors = list(graph.successors(node))

            if len(predecessors) > 1 and len(successors) > 1:

                node_id = str(uuid.uuid1())
                graph.add_node(node_id)
                graph.nodes[node_id]['id'] = node_id

                if 'type' in graph.nodes[node]:

                    node_type = graph.nodes[node]['type']

                    if node_type in Gateway.__members__:
                        graph.nodes[node_id]['type'] = node_type
                    else:
                        graph.nodes[node_id]['type'] = Gateway.inclusiveGateway.value

                graph.add_edge(node_id, node)
                graph[node_id][node]['id'] = node_id + "_" + str(node)

                for predecessor in predecessors:
                    graph.add_edge(predecessor, node_id)
                    graph[predecessor][node_id]['id'] = str(predecessor) + "_" + node_id
                    graph.remove_edge(predecessor, node)


def remove_intermediate_events(graph):
    """
    Removes all intermediate events from a process model
    Parameters
    ----------
    graph : networkx graph
        given networkx graph
    """

    all_nodes = list(graph.nodes)

    for node in all_nodes:
        node_type = graph.nodes[node]['type']
        if node_type in Event.__members__ and node_type != Event.startEvent.value and node_type != Event.endEvent.value:
            predecessors = list(graph.predecessors(node))
            successors = list(graph.successors(node))

            graph.remove_node(node)

            for predecessor in predecessors:

                for successor in successors:
                    graph.add_edge(predecessor, successor)
                    graph[predecessor][successor]['id'] = str(predecessor) + "_" + str(successor)
