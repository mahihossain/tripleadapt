"""
MIT License

Copyright (c) 2020 Philip Hake

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import uuid
import networkx as nx
import random


def sources(graph):
    """
    Parameters
    ----------
    graph : nx.DiGraph

    Returns
    -------
    list of str
        Sources of a graph.
    """
    return [n for n in graph.nodes if graph.in_degree(n) < 1]


def sinks(graph):
    """
    Parameters
    ----------
    graph : nx.DiGraph

    Returns
    -------
    list of str
        Sinks of a graph.
    """
    return [n for n in graph.nodes if graph.out_degree(n) < 1]


def connect(graph, u_nodes, v_nodes):
    """
    Connects each node of u_nodes with each node of v_nodes using a directed edge.

    Parameters
    ----------
    graph :  nx.Graph
        The graph from which the edges are removed.
    u_nodes : list of str
        A list of node ids of the provided graph.
    v_nodes : list of str
        A list of node ids of the provided graph.
    Returns
    -------
    list of tuple
        A list of the added edges.
    """
    edges = []
    for u in u_nodes:
        for v in v_nodes:
            graph.add_edge(u, v)
            edges.append((u, v))
    return edges


def disconnect(graph, u_nodes, v_nodes):
    """
    Removes all directed edges between the nodes in u_nodes and the nodes in v_nodes.

    Parameters
    ----------
    graph :  nx.Graph
        The graph from which the edges are removed.
    u_nodes : list of str
        A list of node ids of the provided graph.
    v_nodes : list of str
        A list of node ids of the provided graph.
    Returns
    -------
    list of tuple
        Returns the edges that have been removed.

    """
    edges = []
    for u in u_nodes:
        for v in v_nodes:
            graph.remove_edge(u, v)
            edges.append((u, v))
    return edges


def virtual_entry_exit(graph, source=None, sink=None):
    """
    If the provided graph exhibits multiple or missing sinks or sources, virtual_entry_exit adds
    additional nodes to the graph. These nodes are called virtual nodes.
    The resulting graph contains only one sink and only one source.

    Parameters
    ----------
    graph : networkx.DiGraph
    source : str
        The id of a graph node. If provided, a virtual source node is added to the graph.
        The virtual sink is connected to the provided node.
    sink : str
        The id of a graph node. If provided, a virtual sink node is added to the graph.
        The provided node is connected to the virtual sink.

    Returns
    -------
    tuple of str
        Returns a tuple containing the original sink and source and if added also the virtual sink and source.
    """
    if source is None:
        source_nodes = sources(graph)
        if not source_nodes:
            raise Exception("No entry node identified. Please fix the graph or specify an entry node.")

    else:
        source_nodes = [source]
    if sink is None:
        sink_nodes = sinks(graph)
        if not sink_nodes:
            raise Exception("No exit node identified. Please fix the graph or specify an exit node.")
    else:
        sink_nodes = [sink]

    orig_source = None if len(source_nodes) > 1 else source_nodes[0]
    orig_sink = None if len(sink_nodes) > 1 else sink_nodes[0]
    virtual_source = orig_source
    virtual_sink = orig_sink

    if orig_source is None:
        virtual_source = "SRC"
        graph.add_node(virtual_source)
        connect(graph, [virtual_source], source_nodes)

    if orig_sink is None:
        virtual_sink = "SNK"
        graph.add_node(virtual_sink)
        connect(graph, sink_nodes, [virtual_sink])

    return orig_source, orig_sink, virtual_source, virtual_sink


def graph_copy_id(graph):
    """
    Generates a copy of the provided graph.
    The method only copies the hashable identifiers of the graphs nodes
    and the edges based on these identifiers.
    Additional node and edge data is not copied.

    Parameters
    ----------
    graph

    Returns
    -------
    networkx.Graph
        Returns a new Graph containing only the original hashable identifiers.
    """
    g = nx.DiGraph()
    g.add_nodes_from(graph.nodes)
    for n in graph.nodes:
        g.add_node(n)
    g.add_edges_from(graph.edges)
    return g


def add_edge_ids(graph, identifier=uuid.uuid1):
    """
    Adds an id to each edge of the graph based on the identifier generator provided.
    The dictionary of each edge is extended by a "id" key and maps "id" to
    an id. If the key "id" already exists the value is overwritten.


    Parameters
    ----------
    graph : networkx.Graph
    identifier : Function that provides a str identifier if called.

    """
    for e in list(graph.edges):
        graph[e[0]][e[1]]["id"] = str(identifier())


def normalize(graph, entry_node=None, exit_node=None):
    """
    The resulting graph contains a single source and a single sink.
    By adding virtual nodes, normalize ensures that either the out degree or the in degree
    of a node is at most 1.

    Parameters
    ----------
    graph : networkx.DiGraph()
    entry_node
    exit_node

    Returns
    -------
    tuple of object
        Returns a tuple containing the original sink and source and if added also the virtual sink and source.
        Also returns a dictionary mapping virtual nodes to the nodes they substitute.
    """
    node_map = dict()

    orig_entry, orig_exit, virt_source, virt_sink = virtual_entry_exit(graph, entry_node, exit_node)

    if virt_source != orig_entry:
        node_map[virt_source] = orig_entry

    if virt_sink != orig_exit:
        node_map[virt_sink] = orig_exit

    for node in list(graph.nodes):

        predecessors = list(graph.predecessors(node))
        successors = list(graph.successors(node))

        if len(predecessors) > 1 and len(successors) > 1:
            virt_internal = "VIRT_INT_" + str(uuid.uuid1())
            graph.add_node(virt_internal, id=str(uuid.uuid1()))

            graph.add_edge(node, virt_internal, id=str(uuid.uuid1()))
            node_map[virt_internal] = node
            for successor in successors:
                graph.remove_edge(node, successor)
                graph.add_edge(virt_internal, successor, id=str(uuid.uuid1()))

    return orig_entry, orig_exit, virt_source, virt_sink, node_map


def move_node(graph, node_id, remove_edge=False):
    """
    Moves a node of a graph to a random position in the graph.

    Parameters
    ----------
    graph : networkx.Graph
        The graph that is manipulated.
    node_id : str
        The id of the node that is moved.
    remove_edge : bool
        Removes edges the preceding and succeeding node at the nodes new position.

    """
    node = dict(graph.nodes(data=True)).get(node_id)
    remove_node(graph, node_id, reconnect=True)

    node_list = list(graph.nodes())
    ran_node = random.choice(node_list)
    insert_node_after(graph, node, ran_node, remove_edge=remove_edge)


def move_ran_nodes(graph, percentage=0.1, n=0, p=0.0, reconnect=True, node_types=None):
    """
    Moves random nodes to a random position within the graph.

    Parameters
    ----------
    graph : networkx.Graph
    percentage : float
        The percentage of nodes that is randomly moved. Either percentage, n or p should
        be set to a value > 0. Otherwise the order of argument usage is percentage, p, n.
    n : int
        The number of nodes that is randomly moved.
    p : float
        The probability that a node from the graph is moved.
    reconnect : bool
        If set to True, the predecessors of the node is connected with the successors
        of the removed node. Thus, move_ran_nodes results in a connected graph if the
        input graph is connected.
    node_types : list of str
        The type of nodes that are moved.

    """
    move = []
    for t in node_types:
        move += random_nodes(graph, percentage, n, p, t)

    for node in move:
        remove_node(graph, node, reconnect=reconnect)


def remove_ran_nodes(graph, percentage=0.1, n=0, p=0.0, reconnect=True, node_types=None):
    """
    Removes random nodes from a graph and edges connected to these nodes. Removing a node results in a
    connected graph if the input graph is connected.

    Parameters
    ----------
    graph : networkx.Graph
        The graph from which the nodes are removed.
    percentage : float
        The percentage of nodes that is randomly removed. Either percentage, n or p should
        be set to a value > 0. Otherwise the order of argument usage is percentage, p, n.
    n : int
        The number of nodes that is randomly removed.
    p : float
        The probability that a node from the graph is removed.
    reconnect : bool
        If set to True, the predecessors of the node is connected with the successors
        of the removed node. Thus, remove_node results in a connected graph if the
        input graph is connected.
    node_types : list of str
        The type of nodes that are removed.

    Returns
    -------

    """
    remove = []
    for t in node_types:
        remove += random_nodes(graph, percentage, n, p, t)

    for node in remove:
        remove_node(graph, node, reconnect=reconnect)


def remove_sese_subgraph(graph, subgraph, entry_node, exit_node, reconnect=False):
    """

    Parameters
    ----------
    graph : networkx.DiGraph
    subgraph : networkx.DiGraph
    reconnect : bool

    """

    if reconnect:

        predecessors = list(graph.predecessors(entry_node))
        successors = list(graph.successors(exit_node))

        for p in predecessors:
            for s in successors:
                graph.add_edge(p, s)

    graph.remove_nodes_from(subgraph.nodes)


def insert_subgraph(graph, subgraph, ref_entries, ref_exits, sub_entries, sub_exits, remove_edge=False):
    """
    Inserts a single entry single exit (SESE) subgraph in between two given nodes. The entry and exit
    nodes of the inserted SESE subgraph are connected to a succeeding and preceding node.
    Either the preceding or the succeeding node can be omitted. If both are omitted
    the SESE subgraph is not inserted. Removing direct edges between the preceding and
    the succeeding node is optional.

    Parameters
    ----------
    graph : networkx.DiGraph
        The networkx graph of a Collaboration Model.
    subgraph : networkx.Graph
        SESE subgraph that is inserted into the given graph.
    entry_node: str
        The subgraphs entry node id.
    exit_node : str
        The subgraphs exit node id.
    pre_node : str
        The id of the preceding node.
    suc_node : str
        The id of the succeeding node.
    remove_edge : bool, optional
        If set to True, existing edges (pre_node, suc_node) are removed from the graph.

    """

    if ref_entries is not None and ref_exits is not None:
        if remove_edge:
            disconnect(graph, ref_entries, ref_exits)
        graph.add_nodes_from(subgraph.nodes(data=True))
        graph.add_edges_from(subgraph.edges(data=True))
        if len(ref_entries) > 0:
            connect(graph, ref_entries, sub_entries)
        if len(ref_exits) > 0:
            connect(graph, sub_exits, ref_exits)


def insert_subgraph_after(graph, subgraph, sub_entries, sub_exits, ref_node, remove_edge=False):
    """
    Inserts a given single entry single exit (SESE) subgraph after a reference node.
    A directed edge is added between the reference node and the entry node of the subgraph.
    Also, the exit node of the subgraph is connected to a randomly sampled node
    from the successors of the reference node. The directed edge between the the reference node and
    the randomly sampled node can be removed.

    Parameters
    ----------
    graph : networkx.DiGraph
    subgraph : networkx.DiGraph
        SESE subgraph that is inserted into the given graph.
    sub_entries: str
        The subgraphs entry node id.
    sub_exits : str
        The subgraphs exit node id.
    ref_node : str
        The id of the networkx reference node. The SESE subgraph is inserted after the reference node.
    remove_edge : bool, optional
        If set to True, the edge between the ref_node and the randomly sampled node is
        removed (the default is False).

    """
    suc = list(graph.successors(ref_node))
    insert_subgraph(graph, subgraph, [ref_node], suc, sub_entries, sub_exits, remove_edge)


def insert_subgraph_before(graph, subgraph, sub_entries, sub_exits, ref_node, remove_edge=False):
    """
    Inserts a given single entry single exit (SESE) subgraph before a reference node.
    A directed edge is added between the exit node of the SESE subgraph and
    the reference node.  Also, a randomly sampled node from the successors of the reference node
    is connected to the entry node of the subgraph. The directed edge between the randomly sampled node
    and the reference node can be removed.

    Parameters
    ----------
    graph : networkx.DiGraph
    subgraph : networkx.DiGraph
        SESE subgraph that is inserted into the given graph.
    sub_entries: str
        The subgraphs entry node id.
    sub_exits : str
        The subgraphs exit node id.
    ref_node : str
        The id of the networkx reference node. The SESE subgraph is inserted after the reference node.
    remove_edge : bool, optional
        If set to True, the edge between the ref_node and the randomly sampled node is
        removed (the default is False).

    """

    pre = list(graph.pre(ref_node))
    insert_subgraph(graph, subgraph, pre, [ref_node], sub_entries, sub_exits, remove_edge)


def remove_node(graph, node, reconnect=False):
    """
    Removes a node from a graph and all connected edges.

    Todo: Also remove nodes that are connected to the node using other edge types than SequenceFlow

    Parameters
    ----------
    graph : networkx.DiGraph
        The graph from which the node is removed.
    node : str
        The node id of the networkx node that is removed.
    reconnect : bool
        If set to True, the predecessors of the node is connected with the successors
        of the removed node. Thus, remove_node results in a connected graph if the
        input graph is connected.
    """

    if reconnect:
        graph.add_edges_from(reconnect_edges(graph, node))

    graph.remove_node(node)


def reconnect_edges(graph, node_id):
    """
    Generates directed edges between all predecessors and successors of a given node.

    Parameters
    ----------
    graph
    node_id

    Returns
    -------

    """
    predecessors = list(graph.predecessors(node_id))
    successors = list(graph.successors(node_id))
    edges = []
    for p in predecessors:
        for s in successors:
            edges += (p[0], s[0])
    return edges


def get_nodes(graph, node_type=None):
    """
    Returns all node ids of the type node_type from a given graph.

    Parameters
    ----------
    graph : networkx.Graph
    node_type : str
        Specifies the the subset of nodes that is returned.

    Returns
    -------
    list of tuple of int and dict
        Returns a list of networkx nodes of the type node_type.

    """

    if node_type is None:
        return list(graph.nodes)
    else:
        nodes = graph.nodes(data="type")
        return [n[0] for n in nodes if n[1]["type"] == node_type]


def random_nodes(graph, percentage=0.1, n=0, p=0.0, node_type=None):
    """
    Returns a list of sampled nodes without replacement.
    If an absolute number n is provided random_nodes returns n samples.
    Parameters
    ----------
    graph : networkx.Graph
        The graph from which the nodes are sampled.

    percentage : float
        If the percentage is set to a value > 0 random_nodes returns a percentage of sampled nodes
        (the default is 0.1).
    n : int
        The number of nodes that is randomly sampled.
    p : float
        If a probability p > 0 is provided each node of the graph is sampled with the probability p.
    node_type : str
        The type of nodes that should be considered for sampling.


    Returns
    -------
    list of tuple of int and dict
        Returns a list of networkx nodes.
    """

    node_list = get_nodes(graph, node_type)

    if percentage > 0:
        n = int(round((percentage * len(node_list))))
    elif p > 0:
        return [n for n in node_list if random.random() < p]

    return random.sample(node_list, n)


def insert_node(graph, node, pre_node, suc_node, remove_edge=False):
    """
    Inserts a node in between two given nodes. The inserted node is connected to a succeeding
    and a preceding node. Either the preceding or the succeeding node can be omitted. If both are omitted
    the node is not inserted. Removing direct edges between the preceding and the succeeding node is optional.

    Parameters
    ----------
    graph : networkx.Graph
        The networkx graph of a Collaboration Model.
    node : tuple of int and dict
        Node that is inserted in the graph.
    pre_node : str
        The id of the preceding node.
    suc_node : str
        The id of the succeeding node.
    remove_edge : bool, optional
        If set to True, existing edges (pre_node, suc_node) are removed from the graph

    """
    if not (pre_node is None and suc_node is None):
        graph.add_node(node)
        if suc_node is not None:
            graph.add_edge(node[0], suc_node)
        if pre_node is not None:
            graph.add_edge(pre_node, node[0])
        if remove_edge:
            graph.remove_edge(pre_node, suc_node)


def insert_node_after(graph, node, ref_node, remove_edge=False):
    """
    Inserts a given node after a reference node. A directed edge is added
    between the reference node and the inserted node. Also, the node is connected to a randomly
    sampled node from the successors of the reference node. Edges between the
    the reference node and the randomly sampled nodes can be removed.

    Parameters
    ----------
    graph : networkx.DiGraph
    node : tuple of int and dict
        networkx node that is inserted.
    ref_node : str
        The id of the networkx reference node. The node is inserted after the reference node.
    remove_edge : bool, optional
        If set to True, edges between the ref_node and the randomly sampled node are
        removed (the default is False).

    """
    suc_nodes = list(graph.successors(ref_node))
    suc_node = None if len(suc_nodes) == 0 else random.choice(suc_nodes)
    insert_node(graph, node, ref_node, suc_node, remove_edge)


def insert_node_before(graph, node, ref_node, remove_edge=False):
    """
    Inserts a given node before a reference node. A directed edge is added
    between the node and the reference node. Also, a randomly
    sampled node from the predecessors of the reference node is connected to the node.
    Edges between the randomly sampled node and the reference node can be removed.

    Parameters
    ----------
    graph : networkx.DiGraph
    node : tuple of int and dict
        networkx node that is inserted.
    ref_node : str
        The id of the networkx reference node. The node is inserted before the reference node.
    remove_edge : bool, optional
        If set to True, edges between the ref_node and the randomly sampled node are
        removed (the default is False).

    """
    pre_nodes = list(graph.predecessors(ref_node))
    pre_node = None if len(pre_nodes) == 0 else random.choice(pre_nodes)
    insert_node(graph, node, pre_node, ref_node, remove_edge)
