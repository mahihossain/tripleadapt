"""
Module to compute triconnected components of a networkx graph
"""

import networkx as nx
import copy
import uuid


def update_lowpts(dfs_tree, node, neighbor, frond):
    """
    updates the lowpts of the dfs algorithms
    Parameters
    ----------
    dfs_tree: nx.DiGraph
        current dfs tree
    node: node
        current node to update
    neighbor: node
        neighbor node of node
    frond: bool
        True if current edge is a frond
    """
    node_value = dfs_tree.nodes[node]['value']
    current_lowpt1 = dfs_tree.nodes[node]['lowpt1']
    current_lowpt2 = dfs_tree.nodes[node]['lowpt2']

    if frond:
        neighbor_lowpt1 = dfs_tree.nodes[neighbor]['value']
        neighbor_lowpt2 = dfs_tree.nodes[neighbor]['value']
    else:
        neighbor_lowpt1 = dfs_tree.nodes[neighbor]['lowpt1']
        neighbor_lowpt2 = dfs_tree.nodes[neighbor]['lowpt2']

    if neighbor_lowpt1 < node_value:
        if neighbor_lowpt1 < current_lowpt1:
            dfs_tree.nodes[node]['lowpt1'] = neighbor_lowpt1
            current_lowpt2 = current_lowpt1
            current_lowpt1 = neighbor_lowpt1
            dfs_tree.nodes[node]['lowpt2'] = current_lowpt2
        else:
            if neighbor_lowpt1 != current_lowpt1:
                neighbor_lowpt2 = neighbor_lowpt1
        if neighbor_lowpt2 < node_value and (neighbor_lowpt2 != current_lowpt1 and neighbor_lowpt2 < current_lowpt2):
                dfs_tree.nodes[node]['lowpt2'] = neighbor_lowpt2


def dfs_1(root, graph):
    """
    Calls the first depth first search

    Parameters
    ----------
    root : networkx node
        root node of the graph
    graph : networkx graph
        networkx graph to iterate over

    Returns
    -------
    dfs_tree: networkx graph
        resulting depth first search tree
    n_adjacent_map : dictionary
        node adjacency map
    n_desc_map : dictionary
        map of descendends of all nodes
    """

    all_edges = list(graph.edges.data())
    dfs_tree = nx.MultiDiGraph()

    adjacency_map = {}

    for edge in list(graph.edges(data=True)):
        source = edge[0]
        target = edge[1]
        if source in adjacency_map:
            adjacency_map[source].append(edge)
        else:
            adjacency_map[source] = [edge]

        if target in adjacency_map:
            adjacency_map[target].append(edge)
        else:
            adjacency_map[target] = [edge]

    dfs_algorithm_1(root, dfs_tree, all_edges, adjacency_map, 1, True)

    n_adjacent_map = {}
    n_desc_map = {}

    for node in dfs_tree.nodes:
        n_adjacent = dfs_tree.nodes[node]['adjacent']
        n_desc = dfs_tree.nodes[node]['ND']

        n_adjacent_map[node] = n_adjacent
        n_desc_map[node] = n_desc

    return dfs_tree, n_adjacent_map, n_desc_map


def dfs_algorithm_1(node, dfs_tree, all_edges, adjacency_map, path_number, starts_path):
    """
    Recursively computes the first depth first search

    Parameters
    ----------
    node : networkx node
        current networkx node to check
    dfs_tree : networkx graph
        current state of the depth first search tree
    all_edges : list of networkx edges
        all edges left to visit
    adjacency_map : dictionary
        adjacency map
    path_number : int
        current number of the path
    starts_path : bool
        True if edge starts a new path

    Returns
    -------
    starts_path : bool
        true if edge started a new path
    """

    if node not in dfs_tree.nodes:
        dfs_tree.add_node(node)
        i = len(dfs_tree.nodes)
        dfs_tree.nodes[node]['value'] = i
        dfs_tree.nodes[node]['lowpt1'] = i
        dfs_tree.nodes[node]['lowpt2'] = i
        dfs_tree.nodes[node]['high'] = []
        dfs_tree.nodes[node]['ND'] = 0
        dfs_tree.nodes[node]['adjacent'] = 0

    if node in adjacency_map:

        neighbors = []

        for e in adjacency_map[node]:
            source = e[0]
            target = e[1]

            if source == node:
                neighbors.append(target)
            else:
                neighbors.append(source)

        for neighbor in neighbors:

            if neighbor in dfs_tree.nodes:
                for edge in all_edges:
                    if (edge[0] == node and edge[1] == neighbor) or (edge[1] == node and edge[0] == neighbor):
                        dfs_tree.add_edge(node, neighbor, id=edge[2]['id'], type='frond', path_number=path_number,
                                          starts_path=starts_path, virtual=edge[2].get('virtual', False),
                                          sese=edge[2].get('sese', False))

                        dfs_tree.nodes[node]['adjacent'] = dfs_tree.nodes[node]['adjacent'] + 1
                        dfs_tree.nodes[neighbor]['adjacent'] = dfs_tree.nodes[neighbor]['adjacent'] + 1
                        path_number = path_number + 1
                        starts_path = True
                        all_edges.remove(edge)
                        dfs_tree.nodes[neighbor]['high'].append(dfs_tree.nodes[node]['value'])

                        update_lowpts(dfs_tree, node, neighbor, True)
                        break

            else:

                dfs_tree.add_node(neighbor)
                i = len(dfs_tree.nodes)
                dfs_tree.nodes[neighbor]['value'] = i
                dfs_tree.nodes[neighbor]['lowpt1'] = i
                dfs_tree.nodes[neighbor]['lowpt2'] = i
                dfs_tree.nodes[neighbor]['high'] = []
                dfs_tree.nodes[neighbor]['ND'] = 0
                dfs_tree.nodes[neighbor]['adjacent'] = 0

                for edge in all_edges:
                    if (edge[0] == node and edge[1] == neighbor) or (edge[1] == node and edge[0] == neighbor):
                        dfs_tree.add_edge(node, neighbor, id=edge[2]['id'], type='arc', path_number=path_number,
                                          starts_path=starts_path, virtual=edge[2].get('virtual', False),
                                          sese=edge[2].get('sese', False))
                        dfs_tree.nodes[node]['adjacent'] = dfs_tree.nodes[node]['adjacent'] + 1
                        dfs_tree.nodes[neighbor]['adjacent'] = dfs_tree.nodes[neighbor]['adjacent'] + 1
                        dfs_tree.nodes[node]['ND'] = dfs_tree.nodes[node]['ND'] + 1

                        if starts_path:
                            starts_path = False

                        all_edges.remove(edge)
                        break

                starts_path, path_number = dfs_algorithm_1(neighbor, dfs_tree, all_edges, adjacency_map,
                                                           path_number, starts_path)
                dfs_tree.nodes[node]['ND'] = dfs_tree.nodes[node]['ND'] + dfs_tree.nodes[neighbor]['ND']

                update_lowpts(dfs_tree, node, neighbor, False)

        return starts_path, path_number


def dfs_2(root, graph, adjacency_map, n_adj_map, n_desc_map):
    """
    Calls the second depth first search

    Parameters
    ----------
     root : networkx node
        root node of the graph
    graph : networkx graph
        networkx graph to iterate over
    adjacency_map : dictionary
        adjacency map
    n_adj_map : dictionary
        node adjacency map
    n_desc_map : dictionary
        map of descendends of all nodes

    Returns
    -------
    dfs_tree: networkx graph
        resulting depth first search tree
    """

    all_edges = list(graph.edges.data())
    dfs_tree = nx.MultiDiGraph()

    dfs_algorithm_2(root, dfs_tree, all_edges, adjacency_map, 1, n_desc_map, n_adj_map, True, len(adjacency_map.keys()))

    return dfs_tree


def dfs_algorithm_2(node, dfs_tree, all_edges, adjacency_map, path_number, n_desc_map, n_adj_map, starts_path, m):

    """
    Recursively computes the second depth first search

    Parameters
    ----------
    node : networkx node
        current networkx node to check
    dfs_tree : networkx graph
        current state of the depth first search tree
    all_edges : list of networkx edges
        all edges left to visit
    adjacency_map : dictionary
        adjacency map
    path_number : int
        current number of the path
    n_desc_map : dictionary
        map of descendants of all nodes
    n_adj_map : dictionary
        node adjacency map
    starts_path : bool
        true if edge starts a new path
    m : int
        value of current node

    Returns
    -------
    starts_path : bool
        true if edge started a new path

       """
    if node not in dfs_tree.nodes or 'value' not in dfs_tree.nodes[node]:
        dfs_tree.add_node(node)
        value = m - n_desc_map[node]
        dfs_tree.nodes[node]['dfs_num'] = len(list(dfs_tree.nodes))
        dfs_tree.nodes[node]['value'] = value
        dfs_tree.nodes[node]['lowpt1'] = value
        dfs_tree.nodes[node]['lowpt2'] = value
        dfs_tree.nodes[node]['high'] = []
        dfs_tree.nodes[node]['ND'] = n_desc_map[node]
        dfs_tree.nodes[node]['adjacent'] = n_adj_map[node]
        dfs_tree.nodes[node]['parent'] = None

    if node in adjacency_map:

        neighbors = []

        for e in adjacency_map[node]:
            source = e[0]
            target = e[1]

            if source == node:
                neighbors.append(target)
            else:
                neighbors.append(source)

        for neighbor in neighbors:

            if neighbor in dfs_tree.nodes:
                for edge in all_edges:
                    if (edge[0] == node and edge[1] == neighbor) or (edge[1] == node and edge[0] == neighbor):
                        dfs_tree.add_edge(node, neighbor, id=edge[2]['id'], type='frond', path_number=path_number,
                                          starts_path=starts_path, virtual=edge[2].get('virtual', False),
                                          sese=edge[2].get('sese', False))
                        path_number = path_number + 1
                        starts_path = True
                        all_edges.remove(edge)
                        dfs_tree.nodes[neighbor]['high'].append(dfs_tree.nodes[node]['value'])

                        update_lowpts(dfs_tree, node, neighbor, True)
                        break

            else:

                dfs_tree.add_node(neighbor)

                for edge in all_edges:
                    if (edge[0] == node and edge[1] == neighbor) or (edge[1] == node and edge[0] == neighbor):
                        dfs_tree.add_edge(node, neighbor, id=edge[2]['id'], type='arc', path_number=path_number,
                                          starts_path=starts_path, virtual=edge[2].get('virtual', False),
                                          sese=edge[2].get('sese', False))
                        if starts_path:
                            starts_path = False

                        all_edges.remove(edge)
                        break

                starts_path, path_number = dfs_algorithm_2(neighbor, dfs_tree, all_edges, adjacency_map, path_number,
                                                           n_desc_map, n_adj_map, starts_path, m)

                dfs_tree.nodes[neighbor]['parent'] = node

                if starts_path:
                    m = m - (n_desc_map[neighbor] + 1)

                update_lowpts(dfs_tree, node, neighbor, False)

        return starts_path, path_number


def sort_edges(graph):
    """
    Sorts all edges of a networkx graph

    Parameters
    ----------
    graph : networkx graph
        networkx Graph which edges are to be sorted

    Returns
    -------
    sorted_edges: list of networkx edges
        list of sorted edges
    """
    vertex_dict = {}
    buckets = []

    counter = 1

    for node in graph.nodes:
        vertex_dict[node] = counter
        counter = counter + 1
        buckets.append([])

    for edge in graph.edges.data():
        source = edge[0]
        target = edge[1]

        min_value = min(vertex_dict[source], vertex_dict[target])

        buckets[min_value].append(edge)

    sorted_edges = []

    for edge_list in buckets:

        sorted_dict = {}

        for edge in edge_list:
            source = edge[0]
            target = edge[1]

            i = vertex_dict[source] + vertex_dict[target]

            if i not in sorted_dict:
                sorted_dict[i] = [edge]
            else:
                sorted_dict[i].append(edge)

        for key in sorted_dict:
            sorted_edge_list = sorted_dict[key]

            for edge in sorted_edge_list:
                sorted_edges.append(edge)

    return sorted_edges


def split_off_multiple_edges(graph):
    """
    Removes duplicate edges and created triconnected components off of them

    Parameters
    ----------
    graph : networkx graph
        networkx graph to examine

    Returns
    -------
    components : list of triconnected components
        resulting components
    """
    sorted_edges = sort_edges(graph)

    components = []

    comp_edges = []

    last_edge = None
    last_source = None
    last_target = None

    for edge in sorted_edges:

        current_source = edge[0]
        current_target = edge[1]

        if last_edge is not None:

            if current_source == last_source and current_target == last_target \
                    or current_source == last_target and current_target == last_source:
                comp_edges.append(last_edge)
            else:
                if len(comp_edges) > 0:
                    comp_edges.append(last_edge)

                    component = []
                    for comp_edge in comp_edges:
                        component.append(comp_edge)
                        graph.remove_edge(comp_edge[0], comp_edge[1])

                    virtual_id = uuid.uuid1()
                    graph.add_edge(last_edge[0], last_edge[1], id=virtual_id, virtual=True)

                    component.append((last_edge[0], last_edge[1], {'id': virtual_id, 'virtual': True}))
                    component = classify_component(component)
                    components.append(component)

                    comp_edges = []

        last_edge = edge
        last_source = current_source
        last_target = current_target

    if len(comp_edges) > 0:
        comp_edges.append(last_edge)

        component = []
        for comp_edge in comp_edges:
            component.append(comp_edge)
            graph.remove_edge(comp_edge[0], comp_edge[1])

        virtual_id = uuid.uuid1()
        graph.add_edge(last_edge[0], last_edge[1], id=virtual_id, virtual=True)

        component.append((last_edge[0], last_edge[1], {'id': virtual_id, 'virtual': True, 'sese': True}))
        component = classify_component(component)
        components.append(component)

    return components


def create_tcc(entry, graph):
    """
    Creates triconnected components from a graph

    Parameters
    ----------
    entry : networkx node
        entry node of the graph
    graph : networkx graph
        networkx graph to examine

    Returns
    -------
    components : list of triconnected components
        resulting components
    """
    components = split_off_multiple_edges(graph)

    dfs_tree, n_adjacent_map, n_desc_map = dfs_1(entry, graph)

    buckets = []

    for i in range(0, (3 * len(dfs_tree.nodes)) + 2):
        buckets.append([])

    for edge in list(dfs_tree.edges(data=True)):
        source = edge[0]
        target = edge[1]

        edge_type = edge[2]['type']
        lowpt_1_w = dfs_tree.nodes[target]['lowpt1']
        lowpt_2_w = dfs_tree.nodes[target]['lowpt2']
        v_value = dfs_tree.nodes[source]['value']
        w_value = dfs_tree.nodes[target]['value']

        if edge_type == 'arc':
            if lowpt_2_w < v_value:
                value = 3 * lowpt_1_w
            else:
                value = (3 * lowpt_1_w) + 2
        else:
            value = (3 * w_value) + 1

        buckets[value - 1].append(edge)

    ordered_adjacency_list = {}

    for edges in buckets:
        while len(edges) != 0:
            current_edge = edges.pop()
            source = current_edge[0]
            if source in ordered_adjacency_list:
                ordered_adjacency_list[source].append(current_edge)
            else:
                ordered_adjacency_list[source] = [current_edge]

    dfs_tree = dfs_2(entry, graph, ordered_adjacency_list, n_adjacent_map, n_desc_map)

    new_adjacency_list = {}
    for key_node in ordered_adjacency_list:

        new_adjacency_list[key_node] = []

        for edge in ordered_adjacency_list[key_node]:
            new_edge_data = dfs_tree.get_edge_data(key_node, edge[1])[0]

            new_adjacency_list[key_node].append((key_node, edge[1], new_edge_data))

    components.extend(find_split_components(entry, graph, dfs_tree, new_adjacency_list))

    components = merge_components(components)
    return components


def share_virtual_edge(component_a, component_b):
    """
    Checks if two triconnected components share a virtual edge

    Parameters
    ----------
    component_a: triconnnected component
        first component
    component_b: triconnnected component
        second component

    Returns
    -------
    shares_virtual_edge: bool
        true if the components share a virtual edge
    virt_edge:
        shared virtual edge
    """

    edges_a = component_a[1]
    edges_b = component_b[1]

    virtual_edges_a = []
    virtual_edges_b = []

    for edge in edges_a:
        if edge[2].get('virtual', False):
            virtual_edges_a.append(edge[2]['id'])

    for edge in edges_b:
        if edge[2].get('virtual', False):
            virtual_edges_b.append(edge[2]['id'])

    for virt_edge in virtual_edges_a:
        if virt_edge in virtual_edges_b:
            return True, virt_edge

    return False, None


def merge_components(components):
    """
    Merges all components with shared virtual edges

    Parameters
    ----------
    components : list of triconnected components
        all triconnected components to merge

    Returns
    -------
    merged_components : list of triconnected components
        maximally merged triconnected components
    """

    final_components = []
    removed_components = []

    final = True

    for component_a in components:

        if component_a not in removed_components:

            component_type = component_a[0]

            for component_b in components:

                if component_a != component_b and component_b not in removed_components \
                        and component_type == component_b[0]:

                    to_merge, virt_edge = share_virtual_edge(component_a, component_b)

                    if to_merge:

                        final = False

                        new_component = []

                        for a_edge in component_a[1]:
                            if a_edge[2]['id'] != virt_edge:
                                new_component.append(a_edge)

                        for b_edge in component_b[1]:
                            if b_edge[2]['id'] != virt_edge:
                                new_component.append(b_edge)

                        component_a = (component_a[0], new_component)

                        removed_components.append(component_b)
                        break

            final_components.append(component_a)

    if not final:
        return merge_components(final_components)

    return final_components


def find_split_components(root, graph, dfs_tree, adjacency_map):
    """
    Computes all minimal triconnected components

    Parameters
    ----------
    root : networkx node
        root node of the graph
    graph : networkx graph
        networkx graph to split
    dfs_tree : networkx graph
        depth first search tree of the given graph
    adjacency_map : dict
        adjacency map of the given graph

    Returns
    -------
    components : list of triconnected components
        all minimal triconnected components
    """
    t_stack = []
    t_stack.append((0, 0, 0))
    e_stack = []

    components = []

    ordered_adjacency = copy.deepcopy(adjacency_map)

    path_search(root, t_stack, e_stack, dfs_tree, adjacency_map, graph, components, ordered_adjacency, [], {}, [])

    component = []
    last_virtual = None
    for edge in e_stack:

        if edge not in component:
            if edge[2]['virtual']:
                last_virtual = edge
            component.append(edge)

        if graph.has_edge(edge[0], edge[1]):
            graph.remove_edge(edge[0], edge[1])

    if last_virtual is not None:
        last_virtual[2]['sese'] = True

    component = classify_component(component)
    components.append(component)

    return components


def get_node_by_value(dfs_tree, value):
    """
    Finds the node with a given value from a graph

    Parameters
    ----------
    dfs_tree : networkx graph
        depth first search tree
    value : int
        value to look for

    Returns
    -------
    node : networkx node
        found node
    """

    for node in dfs_tree.nodes:

        if value == dfs_tree.nodes[node]['value']:
            return node


def get_hidden_edge(edge, virtual_edge_map):
    """
    Returns hidden edges if there are multiple virtual edges mapped to the same edge

    Parameters
    ----------
    edge : networkx edge
        edge to look for
    virtual_edge_map : dict
        map of virtual edges

    Returns
    -------
    hidden_edge: networkx edge
        found hidden edge
    -------
    """

    edge_id = edge[2]['id']

    if edge_id in virtual_edge_map.keys():
        hidden_edge = virtual_edge_map[edge_id]
        return get_hidden_edge(hidden_edge, virtual_edge_map)
    else:
        return edge


def path_search(v, t_stack, e_stack, dfs_tree, map, graph, components, ordered_adjacency, visited, virtual_edge_map,
                removed_edges):
    """
    Executes a path search to find minimal triconnected components

    Parameters
    ----------
    v : networkx node
        current node
    t_stack: list of triples
        stack of possible components
    e_stack : list of networkx edges
        stack of possible edges of triconnected components
    dfs_tree : networkx graph
        depth first search tree
    map : dict
        edge adjacency map
    graph : networkx graph
        underlying graph
    components : list of triconnected components
        all currently stored components
    ordered_adjacency : dict
        ordered node adjacency map
    visited : list of networkx edges
        all visited edges
    virtual_edge_map : dict
        map of virtual edges
    removed_edges : list of networkx edges
        all removed edges
    """
    if v not in map:
        return

    for edge in map[v]:

        if edge in visited:
            continue

        visited.append(edge)
        w = edge[1]
        dfs_tree.nodes[v]['adjacent'] = dfs_tree.nodes[v]['adjacent'] - 1
        dfs_tree.nodes[w]['adjacent'] = dfs_tree.nodes[w]['adjacent'] - 1

        edge_type = edge[2]['type']
        starts_path = edge[2]['starts_path']

        value_w = dfs_tree.nodes[w]['value']
        lowpt1_w = dfs_tree.nodes[w]['lowpt1']

        value_v = dfs_tree.nodes[v]['value']

        if edge_type == 'arc':
            if starts_path:
                deleted_elements = []
                y = 0

                while len(t_stack) != 0:
                    current = t_stack[-1]
                    if current == (0, 0, 0):
                        break

                    h, a, b = current
                    a_value = dfs_tree.nodes[a]['value']

                    if a_value > lowpt1_w:
                        t_stack.pop()

                        if h > y:
                            y = h

                        deleted_elements.append(current)
                    else:
                        break

                n = get_node_by_value(dfs_tree, lowpt1_w)

                if len(deleted_elements) == 0:
                    t_stack.append((value_w + dfs_tree.nodes[w]['ND'], n, v))
                else:
                    h, a, b = deleted_elements[-1]
                    t_stack.append((max(y, value_w + dfs_tree.nodes[w]['ND']), n, b))

                t_stack.append((0, 0, 0))

            path_search(w, t_stack, e_stack, dfs_tree, map, graph, components, ordered_adjacency, visited,
                        virtual_edge_map, removed_edges)

            if edge in removed_edges:
                e_to_push = get_hidden_edge(edge, virtual_edge_map)
                e_stack.append(e_to_push)
            else:
                e_stack.append(edge)

            check_for_type_2(edge, t_stack, e_stack, dfs_tree, graph, components, ordered_adjacency, virtual_edge_map,
                             removed_edges)
            check_for_type_1(edge, e_stack, dfs_tree, graph, components, ordered_adjacency, virtual_edge_map,
                             removed_edges)

            if starts_path:
                while len(t_stack) != 0:
                    current = t_stack.pop()
                    if current == (0, 0, 0):
                        break

            while len(t_stack) != 0:
                current = t_stack[-1]
                if current == (0, 0, 0):
                    break

                h, a, b = current

                a_value = dfs_tree.nodes[a]['value']
                b_value = dfs_tree.nodes[b]['value']

                if len(dfs_tree.nodes[v]['high']) == 0:
                    high_v = 0
                else:
                    high_v = dfs_tree.nodes[v]['high'][0]

                if a_value != value_v and b_value != value_v and high_v > h:
                    t_stack.pop()
                else:
                    break

        else:

            if starts_path:
                deleted_elements = []
                y = 0

                while len(t_stack) != 0:
                    current = t_stack[-1]
                    if current == (0, 0, 0):
                        break

                    h, a, b = current
                    a_value = dfs_tree.nodes[a]['value']

                    if a_value > value_w:
                        t_stack.pop()

                        if h > y:
                            y = h

                        deleted_elements.append(current)
                    else:
                        break

                if len(deleted_elements) == 0:
                    t_stack.append((value_v, w, v))
                else:
                    h, a, b = deleted_elements[-1]
                    t_stack.append((y, w, b))

            value_parent_v = 0
            parent_v = get_parent(v, dfs_tree)

            if parent_v is not None:
                value_parent_v = dfs_tree.nodes[parent_v]['value']

            if value_w == value_parent_v:
                component = []

                edge_w_v = (w, v, copy.deepcopy(dfs_tree.get_edge_data(w, v)[0]))

                add_edge_to_component(component, edge_w_v, graph, dfs_tree, ordered_adjacency, removed_edges)

                virtual_edge = create_virtual_edge(edge_w_v, component, graph, ordered_adjacency, virtual_edge_map)

                make_tree_edge(virtual_edge, (w, v), dfs_tree, ordered_adjacency, e_stack, virtual_edge_map)

                component = classify_component(component)
                components.append(component)

            else:
                e_stack.append(edge)


def check_for_type_1(edge, e_stack, dfs_tree, graph, components, ordered_adjacency, virtual_edge_map, removed_edges):
    """
    Checks for type 1- components

    Parameters
    ----------
    edge : networkx edge
        current edge
    e_stack : list of networkx edges
        stack of possible edges of triconnected components
    dfs_tree : networkx graph
        depth first search tree
    graph : networkx graph
        underlying graph
    components : list of triconnected components
        all currently stored components
    ordered_adjacency : dict
        ordered node adjacency map
    virtual_edge_map : dict
        map of virtual edges
    removed_edges : list of networkx edges
        all removed edges
    """


    v = edge[0]
    w = edge[1]
    lowpt1_w = dfs_tree.nodes[w]['lowpt1']
    lowpt2_w = dfs_tree.nodes[w]['lowpt2']
    value_v = dfs_tree.nodes[v]['value']
    value_w = dfs_tree.nodes[w]['value']
    parent_v = get_parent(v, dfs_tree)

    if lowpt2_w >= value_v > lowpt1_w \
            and ((parent_v is None or dfs_tree.nodes[parent_v]['value'] != 1) or dfs_tree.nodes[v]['adjacent'] > 0):
        component = []

        while len(e_stack) > 0:
            x, y, _ = e_stack[-1]
            x_value = dfs_tree.nodes[x]['value']
            y_value = dfs_tree.nodes[y]['value']
            nd_w = dfs_tree.nodes[w]['ND']

            if value_w <= x_value <= (value_w + nd_w) or value_w <= y_value <= (value_w + nd_w):
                add_edge_to_component(component, e_stack.pop(), graph, dfs_tree, ordered_adjacency, removed_edges)
            else:
                break

        virtual_edge = create_virtual_edge((v, get_node_by_value(dfs_tree, lowpt1_w)), component, graph,
                                           ordered_adjacency, virtual_edge_map)

        component = classify_component(component)
        components.append(component)

        if len(e_stack) > 0:
            x, y, _ = e_stack[-1]
            x_value = dfs_tree.nodes[x]['value']
            y_value = dfs_tree.nodes[y]['value']

            if x_value == value_v and y_value == lowpt1_w or x_value == lowpt1_w and y_value == value_v:
                component = []
                add_edge_to_component(component, e_stack.pop(), graph, dfs_tree, ordered_adjacency, removed_edges)
                add_edge_to_component(component, virtual_edge, graph, dfs_tree, ordered_adjacency, removed_edges)
                virtual_edge = create_virtual_edge((v, get_node_by_value(dfs_tree, lowpt1_w)), component, graph,
                                                   ordered_adjacency, virtual_edge_map)

                component = classify_component(component)
                components.append(component)

        if lowpt1_w != dfs_tree.nodes[parent_v]['value']:
            e_stack.append(virtual_edge)
            make_tree_edge(virtual_edge, (get_node_by_value(dfs_tree, lowpt1_w), v), dfs_tree, ordered_adjacency,
                           e_stack, virtual_edge_map)

        else:
            component = []
            add_edge_to_component(component, virtual_edge, graph, dfs_tree, ordered_adjacency, removed_edges)

            add_edge_to_component(component, (get_node_by_value(dfs_tree, lowpt1_w), v), graph, dfs_tree,
                                  ordered_adjacency, removed_edges)
            virtual_edge = create_virtual_edge((get_node_by_value(dfs_tree, lowpt1_w), v), component, graph,
                                               ordered_adjacency, virtual_edge_map)

            make_tree_edge(virtual_edge, (get_node_by_value(dfs_tree, lowpt1_w), v), dfs_tree, ordered_adjacency,
                           e_stack, virtual_edge_map)
            component = classify_component(component)
            components.append(component)


def check_for_type_2(edge, t_stack, e_stack, dfs_tree, graph, components, ordered_adjacency, virtual_edge_map,
                     removed_edges):
    """
    Checks for type 2- components

    Parameters
    ----------
    edge : networkx edge
        current edge
    t_stack: list of triples
        stack of possible components
    e_stack : list of networkx edges
        stack of possible edges of triconnected components
    dfs_tree : networkx graph
        depth first search tree
    graph : networkx graph
        underlying graph
    components : list of triconnected components
        all currently stored components
    ordered_adjacency : dict
        ordered node adjacency map
    virtual_edge_map : dict
        map of virtual edges
    removed_edges : list of networkx edges
        all removed edges
    """

    v = edge[0]
    value_v = dfs_tree.nodes[v]['value']
    w = edge[1]

    while len(t_stack) > 0 and t_stack[-1] != (0, 0, 0):
        value_w = dfs_tree.nodes[w]['value']
        t_stack_top_h, t_stack_top_a, t_stack_top_b = t_stack[-1]
        t_stack_top_a_value = dfs_tree.nodes[t_stack_top_a]['value']

        w_first_child = None

        if len(ordered_adjacency[w]) > 0:
            w_first_child = ordered_adjacency[w][0][1]

        if value_v != 1 and (t_stack_top_a_value == value_v
                             or (graph.degree(w) == 2
                                 and w_first_child is not None and dfs_tree.nodes[w_first_child]['value'] > value_w)):

            parent_b = get_parent(t_stack_top_b, dfs_tree)
            parent_b_value = 0

            if parent_b is not None:
                parent_b_value = dfs_tree.nodes[parent_b]['value']

            if t_stack_top_a_value == value_v and parent_b_value == t_stack_top_a_value:
                t_stack.pop()

            else:
                edges_a_b = []

                if w_first_child is not None and graph.degree(w) == 2 \
                        and dfs_tree.nodes[w_first_child]['value'] > value_w:
                    component = []

                    current_edge = e_stack.pop()
                    add_edge_to_component(component, current_edge, graph, dfs_tree, ordered_adjacency, removed_edges)

                    current_edge = e_stack.pop()
                    add_edge_to_component(component, current_edge, graph, dfs_tree, ordered_adjacency, removed_edges)

                    virtual_edge = create_virtual_edge((v, current_edge[1]), component, graph,
                                                       ordered_adjacency, virtual_edge_map)

                    component = classify_component(component)
                    components.append(component)

                    if len(e_stack) > 0 and (
                            e_stack[-1][0] == v and e_stack[-1][1] == t_stack_top_b
                            or e_stack[-1][1] == v and e_stack[-1][0] == t_stack_top_b
                            or e_stack[-1][0] == v and e_stack[-1][1] == w_first_child
                            or e_stack[-1][1] == v and e_stack[-1][0] == w_first_child):
                        edges_a_b.append(e_stack.pop())

                else:
                    t_stack_top_h, t_stack_top_a, t_stack_top_b = t_stack.pop()
                    t_stack_top_a_value = dfs_tree.nodes[t_stack_top_a]['value']
                    component = []

                    while len(e_stack) > 0:
                        x, y, _ = e_stack[-1]

                        x_value = dfs_tree.nodes[x]['value']
                        y_value = dfs_tree.nodes[y]['value']

                        if t_stack_top_a_value <= x_value <= t_stack_top_h \
                                and t_stack_top_a_value <= y_value <= t_stack_top_h:

                            if x == t_stack_top_a and y == t_stack_top_b:
                                edges_a_b.append(e_stack.pop())
                            else:
                                add_edge_to_component(component, e_stack.pop(), graph, dfs_tree, ordered_adjacency,
                                                      removed_edges)
                        else:
                            break

                    virtual_edge = create_virtual_edge((t_stack_top_a, t_stack_top_b), component, graph,
                                                       ordered_adjacency, virtual_edge_map)

                    component = classify_component(component)
                    components.append(component)

                if len(edges_a_b) > 0:
                    component = []

                    for edge_a_b in edges_a_b:
                        add_edge_to_component(component, edge_a_b, graph, dfs_tree, ordered_adjacency, removed_edges)

                    add_edge_to_component(component, virtual_edge, graph, dfs_tree, ordered_adjacency, removed_edges)

                    virtual_edge = create_virtual_edge((v, t_stack_top_b), component, graph,
                                                       ordered_adjacency, virtual_edge_map)

                    component = classify_component(component)
                    components.append(component)

                e_stack.append(virtual_edge)

                make_tree_edge(virtual_edge, (v, t_stack_top_b), dfs_tree, ordered_adjacency, e_stack, virtual_edge_map)
                w = t_stack_top_b
                set_parent(w, v, dfs_tree)

        else:
            break


def set_parent(child, parent, dfs_tree):
    """
    Sets a new parent of a node in the dfs tree
    Parameters
    ----------
    child: Networkx.Node
        child node to set new parent
    parent: Networkx.Node
        new parent node
    dfs_tree: Networkx.Graph
        underlying dfs tree
    """
    dfs_tree.nodes[child]['parent'] = parent


def get_parent(node, dfs_tree):
    """
    Finds the parent of a node

    Parameters
    ----------
    node : networkx node
        node which parent is to find
    dfs_tree : networkx graph
        depth first search tree

    Returns
    -------
    parent: networkx node
        parent of the given node
    """

    return dfs_tree.nodes[node]['parent']


def classify_component(component):
    """
    Classifies a triconnected component

    Parameters
    ----------
    component : triconnected component
        given component

    Returns
    -------
    type : str
        classification of the component
    component : triconnected component
        given component
    """

    adj_map = {}

    for edge in component:
        if edge[0] not in adj_map:
            adj_map[edge[0]] = [edge]
        else:
            adj_map[edge[0]].append(edge)

        if edge[1] not in adj_map:
            adj_map[edge[1]] = [edge]
        else:
            adj_map[edge[1]].append(edge)

    if len(adj_map) == 2:
        return 'bond', component

    for n in adj_map:
        if len(adj_map[n]) != 2:
            return 'rigid', component

    return 'polygon', component


def add_edge_to_component(component, edge, graph, dfs_tree, ordered_adjacency, removed_edges):
    """
    Adds an edge to a component

    Parameters
    ----------
    component : triconnected component
        given component
    edge : networkx edge
        edge to add
    graph : networkx graph
        underlying graph
    dfs_tree : networkx graph
        underlying depth first search tree
    ordered_adjacency : dict
        ordered adjacency map
    removed_edges : list of networkx edges
        all removed edges
    """

    if len(edge) < 3:
        edge = (edge[0], edge[1], dfs_tree.get_edge_data(edge[0], edge[1])[0])

    removed_edges.append(edge)
    component.append(edge)

    if graph.has_edge(edge[0], edge[1]):
        graph.remove_edge(edge[0], edge[1])

    if dfs_tree.has_edge(edge[0], edge[1]):
        dfs_tree.remove_edge(edge[0], edge[1])

        if len(edge) > 2:
            edge_type = edge[2]['type']

            if edge_type == 'frond':

                v = edge[0]
                value_v = dfs_tree.nodes[v]['value']

                for node in dfs_tree.nodes:
                    current_high = dfs_tree.nodes[node]['high']

                    if not len(current_high) == 0 and value_v in current_high:
                        dfs_tree.nodes[node]['high'].remove(value_v)

    if edge in ordered_adjacency[edge[0]]:
        ordered_adjacency[edge[0]].remove(edge)

    return


def create_virtual_edge(edge, component, graph, ordered_adjacency, virtual_edge_map):
    """
    Creates a virtual edge

    Parameters
    ----------
    edge : networkx edge
        edge the virtual edge is based on
    component : triconnected component
        component the virtual edge is added to
    graph : networkx graph
        underlying graph
    dfs_tree : networkx graph
        underlying depth first search tree
    ordered_adjacency : dict
        ordered adjacency list

    Returns
    -------
    virtual_edge : networkx edge
        created virtual edge
    """

    source = edge[0]
    edge_id = str(uuid.uuid1())
    graph.add_edge(edge[0], edge[1], id=edge_id, virtual=True)

    virtual_edge = (edge[0], edge[1], {'id': edge_id, 'type': 'arc', 'path_number': 0, 'starts_path': False,
                                       'virtual': True, 'sese': False})

    ordered_adjacency[source].append(virtual_edge)

    for c_edge in component:
        virtual_edge_map[c_edge[2]['id']] = virtual_edge

    sese_component = [sc for sc in component if sc[2].get('sese', False)]

    if not sese_component:
        com_virt_edge = copy.deepcopy(virtual_edge)
        com_virt_edge[2]['sese'] = True
        component.append(com_virt_edge)

    else:
        component.append(virtual_edge)

    return virtual_edge


def make_tree_edge(virtual_edge, edge, dfs_tree, ordered_adjacency, e_stack, virtual_edge_map):
    """
    Makes an edge a new tree edge

    Parameters
    ----------
    virtual_edge : networkx edge
        Underlying virtual edge
    edge : networkx edge
        Edge to convert into tree edge
    dfs_tree : networkx graph
        underlying depth first search tree
    ordered_adjacency : dict
        ordered adjacency map
    e_stack : list of networkx edges
        stack of possible edges of triconnected components
    virtual_edge_map : dict
        map of virtual edges
    """

    source = edge[0]
    target = edge[1]

    edge_id = str(uuid.uuid1())
    if len(virtual_edge) > 2:
        edge_id = virtual_edge[2]['id']

    dfs_tree.add_edge(source, target, id=edge_id, type='arc', path_number=0, starts_path=False, virtual=True,
                      sese=False)

    ordered_adjacency[virtual_edge[0]].append(virtual_edge)

    tree_edge = (source, target, {'id': edge_id, 'type': 'arc', 'path_number': 0, 'starts_path': False, 'virtual': True,
                                  'sese': False})

    for i in range(len(e_stack)):
        edge = e_stack[i]
        if edge[2]['id'] == edge_id:
            e_stack[i] = tree_edge

    for edge in virtual_edge_map.keys():
        if virtual_edge_map[edge] == virtual_edge:
            virtual_edge_map[edge] = tree_edge


######RPST_BUILDER#########################


# def create_tlgg(rpst):
#     """
#     Creates a Top-Level Gateway Graph of a given RPST
#
#     Parameters
#     ----------
#     rpst : RPST
#         given RPST
#
#     Returns
#     -------
#     tlgg : networkx graph
#         resulting TLGG
#     sub_sese_edges : dict
#         dictionary of unfolded RPST children
#
#     """
#     tlgg = copy.deepcopy(rpst.subgraph)
#
#     sub_sese_edges = {}
#
#     for child in rpst.get_children():
#         for edge in child.get_edges(recursive=True):
#             if tlgg.has_edge(edge[0], edge[1]):
#                 tlgg.remove_edge(edge[0], edge[1])
#                 if len(list(tlgg.predecessors(edge[0]))) == len(list(tlgg.successors(edge[0]))) == 0:
#                     tlgg.remove_node(edge[0])
#
#                 if len(list(tlgg.predecessors(edge[1]))) == len(list(tlgg.successors(edge[1]))) == 0:
#                     tlgg.remove_node(edge[1])
#
#         entries, exits = child.sese
#         for entry in entries:
#             for exit in exits:
#                 tlgg.add_edge(entry, exit, fragment=child.id)
#                 sub_sese_edges[(entry, exit)] = child
#
#     return tlgg, sub_sese_edges
#
#
# def pre_process(rpst, tlgg):
#     """
#     Preprocesses the tlgg by removing cycles
#
#     Parameters
#     ----------
#     rpst : RPST
#         given RPST
#     tlgg : networkx graph
#         given TLGG
#
#     Returns
#     -------
#     reversed_edges : list of networkx edges
#         all edges which had to be reversed
#     virtual_nodes : list of networkx nodes
#         all nodes which had to be added
#
#     """
#     depth_dict = {}
#     reversed_edges = []
#     virtual_nodes = []
#
#     try:
#         entries = rpst.sese[0]
#         cycle = list(nx.find_cycle(tlgg, entries[0], orientation='original'))
#
#         for edge in cycle:
#             source = edge[0]
#             target = edge[1]
#
#             source_value = depth_dict[source]
#             target_value = depth_dict[target]
#
#             if source_value > target_value:
#                 tlgg.remove_edge(source, target)
#                 tlgg.add_edge(target, source)
#                 reversed_edges.append((source, target))
#
#         bfs(entries, tlgg, depth_dict, 1, [])
#
#     except nx.exception.NetworkXNoCycle:
#         pass
#
#     all_nodes = copy.deepcopy(tlgg.nodes)
#
#     for node in all_nodes:
#         predecessors = list(tlgg.predecessors(node))
#         successors = list(tlgg.successors(node))
#
#         if len(predecessors) > 1 and len(successors) > 1:
#             virtual_node = str(uuid.uuid1())
#             tlgg.add_node(virtual_node)
#             tlgg.add_edge(node, virtual_node)
#
#             for successor in successors:
#                 tlgg.remove_edge(node, successor)
#                 tlgg.add_edge(virtual_node, successor)
#
#             virtual_nodes.append(virtual_node)
#
#     return reversed_edges, virtual_nodes
#
#
# def bfs(current_layer, tlgg, depth_dict, counter, visited):
#     """
#     Breadth first search of a TLGG
#
#     Parameters
#     ----------
#     current_layer : list of networkx nodes
#         current node layer of the bfs
#     tlgg : networkx graph
#         given TLGG
#     depth_dict : dict
#         dictionary of all nodes mapped to the bfs layer
#     counter : int
#         current depth of the bfs
#     visited : list of networkx nodes
#         all visited nodes
#     """
#
#     if len(current_layer) == 0:
#         return
#
#     next_layer = []
#
#     for node in current_layer:
#         if node not in visited:
#             depth_dict[node] = counter
#             next_layer.extend(list(tlgg.successors(node)))
#             visited.append(node)
#
#     bfs(next_layer, tlgg, depth_dict, counter + 1, visited)
#
#
# def match_tlgg(tlgg):
#     """
#     Matches entry and goal nodes of the TLGG
#
#     Parameters
#     ----------
#     tlgg : networkx graph
#         given TLGG
#
#     Returns
#     -------
#     matches : dict
#         resulting matches
#     """
#
#     matches = {}
#
#     while len(tlgg.nodes) != 0:
#         entry_nodes, exit_nodes = get_entry_exit_nodes(tlgg)
#
#         if len(entry_nodes) == len(exit_nodes) == 1:
#             matches[entry_nodes[0]] = [exit_nodes[0]]
#             tlgg.remove_node(entry_nodes[0])
#             tlgg.remove_node(exit_nodes[0])
#
#         else:
#
#             entry_node = entry_nodes[0]
#
#             matches[entry_nodes[0]] = []
#
#             shortest_size = None
#             goals = []
#
#             for exit_node in exit_nodes:
#                 current_length = len(nx.shortest_path(tlgg, source=entry_node, target=exit_node))
#
#                 if len(goals) == 0:
#                     shortest_size = current_length
#                     goals.append(exit_node)
#                 else:
#
#                     if current_length == shortest_size:
#                         goals.append(exit_node)
#
#                     elif current_length < shortest_size:
#                         shortest_size = current_length
#                         goals = [exit_node]
#
#             tlgg.remove_node(entry_node)
#
#             for exit_node in goals:
#                 tlgg.remove_node(exit_node)
#                 matches[entry_node].append(exit_node)
#
#         simplify_graph(tlgg)
#
#     return matches
#
#
# def simplify_graph(tlgg):
#     """
#     Simplifies the TLGG
#
#     Parameters
#     ----------
#     tlgg : networkx.Graph
#         given TLGG
#     """
#     changed = True
#
#     while changed:
#
#         changed = False
#         current_nodes = copy.deepcopy(tlgg.nodes)
#
#         for node in current_nodes:
#
#             predecessors = list(tlgg.predecessors(node))
#             successors = list(tlgg.successors(node))
#
#             if len(predecessors) == 0 and len(successors) == 0:
#                 tlgg.remove_node(node)
#                 changed = True
#             elif len(predecessors) == 1 and len(successors) == 1:
#                 tlgg.add_edge(predecessors[0], successors[0])
#                 tlgg.remove_node(node)
#                 changed = True
#
#
# def get_entry_exit_nodes(tlgg):
#     """
#     Computes all entry and exit nodes of the TLGG
#
#     Parameters
#     ----------
#     tlgg : networkx graph
#         given TLGG
#
#     Returns
#     -------
#     entry_nodes : list of networkx nodes
#         all entry nodes of the TLGG
#     exit_nodes : list of networkx nodes
#         all exit node of the TLGG
#     """
#     entry_nodes = []
#     exit_nodes = []
#
#     for node in tlgg.nodes:
#         if len(list(tlgg.successors(node))) == 0:
#             exit_nodes.append(node)
#
#         elif len(list(tlgg.predecessors(node))) == 0:
#             entry_nodes.append(node)
#
#     return entry_nodes, exit_nodes
#
#
# def reconstruct_tlgg_recursive(current, matches, fixed_graph, tlgg, duplicates, all_goal_nodes, visited):
#     """
#     Recursively reconstructs the TLGG to remove all rigids
#
#     Parameters
#     ----------
#     current : networkx node
#         current node
#     matches : dict
#         matches entry and goal nodes
#     fixed_graph : networkx graph
#         reconstructed, rigid-free graph
#     tlgg : networkx graph
#         given TLGG
#     duplicates : dict
#         map of all duplicated nodes and their originals
#     all_goal_nodes : list of networkx nodes
#         all given goal nodes
#     visited : list of networkx nodes
#         all visited nodes
#     """
#     added_nodes = {}
#     visited.append(current)
#
#     goal_nodes = matches[current]
#
#     for goal_node in goal_nodes:
#
#         all_paths = list(nx.all_simple_paths(tlgg, current, goal_node))
#
#         simple_paths = []
#         complex_paths = []
#
#         for path in all_paths:
#             reaches_new_entry = len([i for i in path if i is not current and i in matches.keys()]) != 0
#             reaches_new_exit = len([i for i in path if i not in goal_nodes and i in all_goal_nodes]) != 0
#
#             if (not reaches_new_entry and not reaches_new_exit) or (reaches_new_entry and reaches_new_exit):
#                 simple_paths.append(path)
#             else:
#                 complex_paths.append(path)
#
#         for simple_path in simple_paths:
#
#             last_node = None
#             recursive = False
#             possible_end_nodes = []
#
#             for node in simple_path:
#
#                 if not (recursive and last_node not in possible_end_nodes):
#
#                     if node != current and node in matches.keys():
#                         if node not in visited:
#                             reconstruct_tlgg_recursive(node, matches, fixed_graph, tlgg, duplicates, all_goal_nodes,
#                             visited)
#
#                         possible_end_nodes = matches[node]
#                         recursive = True
#
#                     else:
#
#                         if recursive:
#                             recursive = False
#
#                         if node not in added_nodes.keys():
#
#                             if not fixed_graph.has_node(node):
#                                 fixed_graph.add_node(node)
#                                 added_nodes[node] = node
#                             else:
#                                 duplicate_node = str(uuid.uuid1())
#                                 added_nodes[node] = duplicate_node
#
#                                 if node in duplicates.keys():
#                                     duplicates[node].append(node)
#                                 else:
#                                     duplicates[node] = [duplicate_node]
#
#                             for key in tlgg.nodes[node]:
#                                 fixed_graph.nodes[added_nodes[node]][key] = tlgg.nodes[node][key]
#
#                         else:
#                             node = added_nodes[node]
#
#                     if last_node is not None:
#                         if not fixed_graph.has_edge(last_node, node):
#                             fixed_graph.add_edge(last_node, node, id=str(uuid.uuid1()))
#
#                 last_node = node
#
#         for complex_path in map(nx.utils.pairwise, complex_paths):
#             for edge in complex_path:
#                 entries = [edge[0]]
#                 exits = [edge[1]]
#
#                 if edge[0] in duplicates.keys():
#                     entries.extend(duplicates[edge[0]])
#                 if edge[1] in duplicates.keys():
#                     exits.extend(duplicates[edge[1]])
#
#                 has_edge = False
#
#                 for entry in entries:
#                     for exit in exits:
#                         if fixed_graph.has_edge(entry, exit):
#                             has_edge = True
#                             break
#                     if has_edge:
#                         break
#
#                 if has_edge:
#                     continue
#
#                 for entry in entries:
#                     if 'alternative' in fixed_graph.nodes[entry]:
#                         fixed_graph.nodes[entry]['alternative'].append(exit)
#                     else:
#                         fixed_graph.nodes[entry]['alternative'] = [exit]
#
#
# def reconstruct_tlgg(entry, matches, tlgg):
#     """
#     Reconstructs the TLGG to remove all rigids
#
#     Parameters
#     ----------
#     entry : networkx node
#         entry node of the TLGG
#     matches : dict
#         matches entry and goal nodes
#     tlgg : networkx graph
#         given TLGG
#
#     Returns
#     -------
#     fixed_graph : networkx graph
#         reconstructed, rigid-free graph
#     duplicates : dict
#         map of all duplicated nodes and their originals
#     """
#     fixed_graph = nx.DiGraph()
#     duplicates = {}
#
#     all_goal_nodes = []
#
#     for goal_nodes in matches.values():
#         all_goal_nodes.extend(goal_nodes)
#
#     reconstruct_tlgg_recursive(entry, matches, fixed_graph, tlgg, duplicates, all_goal_nodes, [])
#
#     return fixed_graph, duplicates
#
#
# def reverse_pre_processing(graph, reversed_edges, virtual_nodes, duplicates):
#     """
#     Reverses the preprocessing
#
#     Parameters
#     ----------
#     graph : networkx graph
#         graph to reconstruct
#     reversed_edges : list of networkx edges
#         all edges which had to be reversed
#     virtual_nodes : list of networkx nodes
#         all nodes which had to be added
#     duplicates : dict
#         map of all duplicated nodes and their originals
#     """
#     for reversed_edge in reversed_edges:
#         source = reversed_edge[0]
#         target = reversed_edge[1]
#
#         sources = [source]
#         targets = [target]
#
#         if source in duplicates.keys():
#             sources.extend(duplicates[source])
#
#         if target in duplicates.keys():
#             targets.extend(duplicates[target])
#
#         for s in sources:
#             for t in targets:
#
#                 if graph.has_edge(t, s):
#                     graph.remove_edge(t, s)
#                     graph.add_edge(s, t, id=str(uuid.uuid1()))
#
#     for virtual_node in virtual_nodes:
#
#         v_nodes = [virtual_node]
#
#         if virtual_node in duplicates.keys():
#             v_nodes.extend(duplicates[virtual_node])
#
#         for n in v_nodes:
#             predecessor = list(graph.predecessors(n))[0]
#             successors = list(graph.successors(n))
#
#             for successor in successors:
#                 graph.add_edge(predecessor, successor)
#
#             graph.remove_node(n)
#
#
# def add_edge_to_subgraph(subgraph, edge, original_graph):
#     """
#     Adds an edge to a RPST subgraph
#
#     Parameters
#     ----------
#     rpst : RPST
#         given RPST
#     edge : networkx edge
#         edge to add
#     original_graph : networkx graph
#         graph to add edge into
#     """
#     source = edge[0]
#     target = edge[1]
#
#     if not subgraph.has_node(source):
#         subgraph.add_node(source)
#
#         node_dict = original_graph.nodes(data=True)[source]
#
#         for key in node_dict:
#             subgraph.nodes[source][key] = node_dict[key]
#
#     if not subgraph.has_node(target):
#         subgraph.add_node(target)
#
#         node_dict = original_graph.nodes(data=True)[target]
#
#         for key in node_dict:
#             subgraph.nodes[target][key] = node_dict[key]
#
#     subgraph.add_edge(source, target)
#
#     if len(edge) > 2:
#         subgraph[source][target].update(edge[2])
#
#
# def order_bond_children(to_order):
#     """
#     Orders all bond children
#
#     Parameters
#     ----------
#     to_order : list of RPSTs
#         bonds to order
#
#     Returns
#     -------
#     ordered_list : list of RPSTs
#         ordered list of bonds
#
#     """
#     ordered_list = []
#     order = {}
#
#     for child in to_order:
#         subgraph = child.get_subgraph()
#
#         node_size = len(list(subgraph.nodes))
#
#         if node_size in order:
#             order[node_size].append(child)
#         else:
#             order[node_size] = [child]
#
#     for key in sorted(order.keys()):
#         if len(order[key]) == 1:
#             ordered_list.append(order[key][0])
#         else:
#             ordered_list.extend(tiebreak_nodes(order[key]))
#
#     return ordered_list
#
#
# def tiebreak_nodes(to_order):
#     """
#     Orders RPSTs if they need tiebreak
#
#     Parameters
#     ----------
#     to_order : list of RPST
#         RPSTs to order
#
#     Returns
#     -------
#     ordered_list : list of RPSTs
#         ordered list of RPSTs
#     """
#     ordered_list = []
#
#     string_map = {}
#
#     for child in to_order:
#         subgraph = child.get_subgraph()
#
#         nodes_string = ""
#
#         for node in subgraph.nodes:
#             if 'name' in node:
#                 nodes_string = nodes_string + node['name']
#
#         if nodes_string not in string_map:
#             string_map[nodes_string] = [child]
#         else:
#             string_map[nodes_string].append(child)
#
#     for key in sorted(string_map.keys()):
#         ordered_list.extend(string_map[key])
#
#     return ordered_list
#
#
# def dfs_edges(tlgg, node, collected_edges):
#     """
#     Depth first search on a TLGG
#
#     Parameters
#     ----------
#     tlgg : networkx graph
#         given TLGG
#     node : networkx node
#         current node
#     collected_edges : list of networkx edges
#         all visited edges
#
#     Returns
#     -------
#     updated_collected_edges : list of networkx edges
#         updated visited edges
#     """
#
#     for successor in tlgg.successors(node):
#         current_edge = (node, successor)
#
#         if current_edge not in collected_edges:
#             collected_edges.append(current_edge)
#             dfs_edges(tlgg, successor, collected_edges)
#
#     return collected_edges
#
#
# def order_rigid(entry, tlgg, sub_sese_edges):
#     """
#     Orders all fragments of a rigid
#
#     Parameters
#     ----------
#     entry : networkx node
#         entry node of the rigid
#     tlgg : networkx graph
#         given TLGG
#     sub_sese_edges : dict
#         dictionary of unfolded RPST children
#
#     Returns
#     -------
#     ordered_fragments : list of RPSTs
#         ordered fragments
#     """
#     ordered_edges = dfs_edges(tlgg, entry, [])
#
#     ordered_fragments = []
#
#     for edge in ordered_edges:
#         ordered_fragments.append(sub_sese_edges.get(edge))
#
#     return ordered_fragments
#
# def fix_rigids(cls):
#     #TODO: ADAPT TO NEW CLASS STRUCTURE
#     """
#     Iterates over and reworks all Rigid Fragments
#
#     Notes
#     -----
#     Based on [1] Qian, C., Wen, L., Wang, J., Kumar, A., & Li, H. (2017, June).
#     Structural descriptions of process models based on goal-oriented unfolding.
#     In International Conference on Advanced Information Systems Engineering (pp. 397-412). Springer, Cham.
#     """
#
#     import rmm.rmm4pycore-rmm.models.rpst.rpst_builder as builder
#
#
#     for child in cls.rootFragment.children:
#         child.fix_rigids()
#
#     if cls.type == 'Rigid':
#
#         print(cls.subgraph.edges)
#
#         tlgg, sub_sese_edges = create_tlgg(cls)
#
#         print(tlgg.edges)
#
#         #TODO: BFS?
#         reversed_edges, virtual_nodes = pre_process(cls, tlgg)
#
#         print(tlgg.edges)
#
#         matches = match_tlgg(copy.deepcopy(tlgg))
#
#         fixed_rigid, duplicates = reconstruct_tlgg(cls.sese[0][0], matches, tlgg)
#
#         print(fixed_rigid.edges)
#
#         reverse_pre_processing(fixed_rigid, reversed_edges, virtual_nodes, duplicates)
#
#         if len(list(fixed_rigid.predecessors(cls.sese[0][0]))) != 0:
#             unique_src = str(uuid.uuid1())
#             fixed_rigid.add_node(unique_src)
#
#             fixed_rigid.add_edge(unique_src, cls.sese[0][0], id=str(uuid.uuid1()))
#
#         if len(list(fixed_rigid.successors(cls.sese[1][0]))) != 0:
#             unique_snk = str(uuid.uuid1())
#             fixed_rigid.add_node(unique_snk)
#
#             fixed_rigid.add_edge(cls.sese[1][0], unique_snk, id=str(uuid.uuid1()))
#
#         fixed_bpmn = CollaborationModel()
#         fixed_bpmn.process_graph = fixed_rigid
#
#         print(fixed_rigid.edges(data=True))
#
#         fixed_rpst = builder.compute_rpst(fixed_bpmn, sese=cls.sese)
#
#         cls.type = fixed_rpst.type
#
#         cls.edges = fixed_rpst.edges
#
#         cls.children = fixed_rpst.children
#
#         cls.subgraph = fixed_rpst.subgraph
#
#         for edge in fixed_rpst.edges:
#             entry = edge[0]
#             exit = edge[1]
#
#             entries = [entry]
#             exits = [exit]
#
#             if entry in duplicates.keys():
#                 entries.extend(duplicates[entry])
#
#             if exit in duplicates.keys():
#                 exits.extend(duplicates[exit])
#
#             for entry in entries:
#                 for exit in exits:
#                     if (entry, exit) in sub_sese_edges.keys():
#                         cls.edges.remove(edge)
#                         cls.add_child(sub_sese_edges[(entry, exit)])
#
# def unfold_subgraph(cls, graph, rpst, recursive=False):
#     """
#     Unfolds a given subgraph
#     Parameters
#     ----------
#     graph : networkx.Graph
#         graph to unfold
#     rpst : RPST
#         rpst to unfold
#     recursive : bool, optional
#         true, if recursively unfolding
#
#     Returns
#     -------
#     sub_graph: networkx.Graph
#         resulting graph
#     """
#
#     graph_copy = copy.deepcopy(graph)
#     rpst_id = rpst.id
#     edges = list(graph.edges(data=True))
#     nodes = list(graph.nodes(data=True))
#
#     unfolded = False
#
#     for edge in edges:
#         if unfolded:
#             break
#         edge_data = edge[2]
#
#         if 'type' in edge_data:
#             rpst_type = edge_data['type']
#             if rpst_type == "Bond" or rpst_type == "Polygon" or rpst_type == "Rigid":
#
#                 current_rpst_id = edge_data['id']
#
#                 print(current_rpst_id)
#                 print(rpst_id)
#
#                 if current_rpst_id == rpst_id:
#                     graph_copy.remove_edge(edge[0], edge[1])
#
#                     unfolded = True
#
#                     for rpst_child in cls.children:
#                         if rpst_child.id == rpst_id:
#
#                             rpst_subgraph = rpst_child.get_subgraph(unfolded=recursive)
#
#                             for sub_edge in list(rpst_subgraph.edges(data=True)):
#                                 add_edge_to_subgraph(graph_copy, sub_edge, rpst_subgraph)
#                             break
#
#     for node in nodes:
#         node_data = node[1]
#         if 'substitue' in node_data and node_data['substitute'] == rpst_id:
#             graph_copy.remove_node(node[0])
#
#     return graph_copy



# def sort_fragment(cls):
#     """
#     Sorts the RPST
#     """
#
#     for child in cls.children:
#         child.sort_fragment()
#
#
#     if cls.type == "Bond":
#
#         to_order = []
#         to_order_backedges = []
#
#         for child in cls.children:
#             child_entry = child.sese[0][0]
#
#             if child_entry == cls.exit:
#                 to_order_backedges.append(child)
#             else:
#                 to_order.append(child)
#
#         ordered_children = order_bond_children(to_order)
#
#         if len(to_order_backedges) > 0:
#             ordered_children.extend(order_bond_children(to_order_backedges))
#
#         cls.children = ordered_children
#
#     elif cls.type == "Polygon":
#         tlgg, sub_sese_edges = create_tlgg(cls)
#
#
#
#         ordered_children = []
#
#         path = list(map(nx.utils.pairwise, nx.all_simple_paths(tlgg, source=cls.entry, target=cls.exit)))[0]
#
#         for edge in path:
#             ordered_children.append(sub_sese_edges[edge])
#
#         cls.children = ordered_children
#
#     elif cls.type == "Rigid":
#         tlgg, sub_sese_edges = create_tlgg(cls)
#
#         ordered_children = order_rigid(cls.entry, tlgg, sub_sese_edges)
#
#         cls.children = ordered_children
