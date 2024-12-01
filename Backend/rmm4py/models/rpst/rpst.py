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

import networkx as nx
import uuid
from rmm4py.models.rpst.tri_connected_components import create_tcc
import rmm4py.models.graph_util as gu


class RPST(object):
    """
    Class to represent the redefined process structure tree.
    """
    def __init__(self, graph, entry_node=None, exit_node=None):
        """
        Parameters
        ----------
        graph : networkx.DiGraph
        entry_n : str
        exit_n : str
        """
        self.graph = graph
        self.tree = nx.DiGraph()
        edges = list(graph.edges())
        if len(edges) == 1:
            e = edges[0]
            self.root_id = uuid.uuid1()
            self.add_child(None, self.root_id, "trivial", e[0], e[1], (e[0], e[1]), [e[0], e[1]])
        else:
            self.root_id = self._compute_rpst(entry_node, exit_node)

    def _compute_rpst(self, entry_n, exit_n):
        """
        Creates a RPST based on cls.graph.

        Parameters
        ----------
        entry_n : str
        exit_n : str

        Returns
        -------
        str
            Returns the id of the root node.
        """

        graph = gu.graph_copy_id(self.graph)
        orig_entry, orig_exit, virt_entry, virt_exit, node_map = gu.normalize(graph, entry_n, exit_n)
        gu.add_edge_ids(graph)

        initial_multi_graph, root_edge = self._initial_multi_graph(graph, virt_entry, virt_exit)

        tc_components = create_tcc(virt_exit, initial_multi_graph)

        self._build_rpst(tc_components, node_map, root_edge, virt_entry, virt_exit)
        self._fix_single_child_fragments(root_edge)
        root_edge = gu.sources(self.tree)[0]
        self._fix_sese(orig_entry, root_edge)

        return root_edge

    @staticmethod
    def _component_map(tc_components):
        tc_edge = dict()
        for tcc in tc_components:
            for edge in tcc[1]:
                if edge[2].get("virtual"):
                    tcs = tc_edge.get(edge[2].get("id"), [])
                    tcs.append(tcc)
                    tc_edge[edge[2].get("id")] = tcs
        return tc_edge

    def _build_rpst(self, tc_components, node_map, root_edge, entry_n, exit_n):
        """
        Builds a fragment tree based on the provided 3-connected components
        Parameters
        ----------
        tc_components
        node_map

        Returns
        -------

        """
        component_map = self._component_map(tc_components)
        root_component = component_map[root_edge][0]
        components = [(root_component, root_edge, None, entry_n, exit_n)]
        while components:
            tcc, fragment_id, parent_id, entry_n, exit_n = components.pop()
            entry_n = node_map.get(entry_n, entry_n)
            exit_n = node_map.get(exit_n, exit_n)
            fragment_type = tcc[0]
            self.add_child(parent_id, fragment_id, fragment_type, entry_n, exit_n)
            for e in tcc[1]:
                if not e[2].get("virtual"):
                    self._add_trivial(e, node_map, fragment_id)
                else:
                    sub_fragment_id = e[2].get("id")
                    if fragment_id != sub_fragment_id:
                        parent_child_components = component_map.get(sub_fragment_id, [])
                        if len(parent_child_components) > 1:
                            sub_tcc = [c for c in parent_child_components if c != tcc][0]
                            components.append((sub_tcc, sub_fragment_id, fragment_id, e[0], e[1]))

    def _add_trivial(self, e, node_map, fragment_id):
        """
        Adds a trivial node to the rpst based on a tcc edge
        Parameters
        ----------
        e : tuple of object
        node_map : dict
        fragment_id : str

        Returns
        -------

        """
        if not (e[0] in node_map and e[1] in node_map):
            u = node_map.get(e[0], e[0])
            v = node_map.get(e[1], e[1])

            if u != v and u is not None and v is not None:
                if (u, v) not in self.graph.edges:
                    u, v = v, u
                self.add_child(fragment_id, e[2]["id"], "trivial", u, v, [u, v], [(u, v)])

    @staticmethod
    def _initial_multi_graph(graph, virt_entry, virt_exit):
        undirected_graph = nx.MultiGraph()
        undirected_graph.add_nodes_from(graph.nodes.data())
        undirected_graph.add_edges_from(graph.edges.data())
        root_edge = str(uuid.uuid1())
        undirected_graph.add_edge(virt_entry, virt_exit, id=root_edge, virtual=True, sese=True)
        return undirected_graph, root_edge

    def _fix_single_child_fragments(self, frag_id):
        """
        Recursively removes fragments with only one child and fixes the tree edges.

        Parameters
        ----------
        frag_id

        Returns
        -------

        """
        node = self.tree.nodes[frag_id]
        if node["fragment_type"] != "trivial":
            c_nodes = self.children(frag_id)
            parent = self.parent(frag_id)
            if len(c_nodes) < 2:
                child = c_nodes[0]
                if parent is not None:
                    self.tree.add_edge(parent, child)
                self.tree.remove_node(frag_id)
            else:
                for c in c_nodes:
                    self._fix_single_child_fragments(c)

    def _fix_sese(self, p_entry, f_id):
        """
        Recursively checks if all SESE nodes of a fragment are set correctly and fixes inverted ones.

        Parameters
        ----------
        rpst: RPST
            The RPST to fix
        """

        f_entry = self.tree.nodes[f_id]["entry_node"]
        f_graph = self.subgraph(f_id)
        f_type = self.tree.nodes[f_id]["fragment_type"]
        parent_id = self.parent(f_id, data=False)

        if parent_id is None:
            if f_entry != p_entry:
                self._swap_sese(f_id)
        elif f_type != 'trivial':

            p_type = self.tree.nodes[parent_id]["fragment_type"]
            p_entry = self.tree.nodes[parent_id]["entry_node"]

            if p_type == "bond":
                f_exit = self.tree.nodes[f_id]["exit_node"]
                if not nx.has_path(f_graph, f_entry, f_exit):
                    self._swap_sese(f_id)
            else:
                p_graph = self.subgraph(parent_id)

                if p_entry is None:
                    p_entry = gu.sources(p_graph)[0]

                p_graph.remove_edges_from(f_graph.edges)
                if not nx.has_path(p_graph, p_entry, f_entry):
                    self._swap_sese(f_id)

        for child in self.children(f_id, data=False):
            self._fix_sese(self.tree.nodes[f_id]["entry_node"], child)

    def _swap_sese(self, f_id):
        """
        Swaps entry and exit of a fragment.

        Parameters
        ----------
        f_id : str
            The id of the fragment.

        """
        f_exit = self.tree.nodes[f_id]["exit_node"]
        f_entry = self.tree.nodes[f_id]["entry_node"]
        self.tree.nodes[f_id]["exit_node"] = f_entry
        self.tree.nodes[f_id]["entry_node"] = f_exit

    def add_to_parent(self, fragment_id, parent_id):
        """
        Assigns a fragment that is contained in the tree a parent fragment.
        Updates the edge and node lists of the fragment with the id parent_id and all it's ancestors.

        Parameters
        ----------
        fragment_id : str
            The id of the fragment that is added to a parent fragment.
        parent_id : str
            The id of the parent fragment to which the fragment is added.

        """
        self.tree.add_edge(parent_id, fragment_id)
        add_nodes = [cn for cn in self.tree.nodes[fragment_id]['nodes']]
        add_edges = [cn for cn in self.tree.nodes[fragment_id]['edges']]
        ance = self.ancestors(parent_id, data=False)
        ance.append(parent_id)
        for ancestor in ance:
            self.tree.nodes[ancestor]['nodes'] += [n for n in add_nodes if n not in self.tree.nodes[ancestor]['nodes']]
            self.tree.nodes[ancestor]['edges'] += [e for e in add_edges if e not in self.tree.nodes[ancestor]['edges']]

    def add_child(self, parent_id, node_id, fragment_type="", entry_node=None, exit_node=None, nodes=None, edges=None):
        """
        Adds a rpst node to the tree.

        Parameters
        ----------
        parent_id : str
            Adds the rpst node as a child of fragment with the id parent_id.
            If parent_id is None only the rpst node is added. Updates the edge and node lists of the fragment
            with the id parent_id and all it's ancestors.

        node_id : str
            A unique node id within the RPST tree. Usage of uuid.uuid1() is recommended
        fragment_type
        entry_node
        exit_node
        nodes
        edges

        Returns
        -------

        """
        nodes = [] if nodes is None else nodes
        edges = [] if edges is None else edges
        self.tree.add_node(node_id, fragment_id=node_id, fragment_type=fragment_type, entry_node=entry_node,
                           exit_node=exit_node, nodes=nodes, edges=edges)
        if parent_id is not None:
            self.add_to_parent(node_id, parent_id)

    def descendants(self, fragment, data=False):
        """
        Returns all descendants of a fragment.
        Parameters
        ----------
        fragment : str or tuple of object
            Either the fragment id or the fragment (rpst node) itself can be provided.
        data : bool
            Returns also the data dictionaries of the rpst nodes if set to True. Otherwise only
            the ids are returned.
        Returns
        -------
        list of str or list of dict
        """
        node_id = self._fragment_id(fragment)
        desc = list(nx.algorithms.dag.descendants(self.tree, node_id))
        return [self.fragment(c) for c in desc] if data else desc

    def ancestors(self, fragment, data=False):
        """
        Returns all ancestors of a fragment.
        Parameters
        ----------
        fragment : str or tuple of object
            Either the fragment id or the fragment (rpst node) itself can be provided.
        data : bool
            Returns also the data dictionaries of the rpst nodes if set to True. Otherwise only
            the ids are returned.
        Returns
        -------
        list of str or list of dict
        """
        node_id = self._fragment_id(fragment)
        ance = list(nx.algorithms.dag.ancestors(self.tree, node_id))
        return [self.fragment(c) for c in ance] if data else ance

    def children(self, fragment, data=False):
        """
        Returns the children of a fragment. If the RPST is sorted the children are returned
        ordered.

        Parameters
        ----------
        fragment : str or tuple of object
            Either the fragment id or the fragment (rpst node) itself can be provided.
        data : bool
            Returns also the data dictionaries of the rpst nodes if set to True. Otherwise only
            the ids are returned.
        Returns
        -------
        list of str or list of dict
        """
        f_id = self._fragment_id(fragment)
        succ = list(self.tree.successors(f_id))
        sorted_succ = sorted(succ, key=lambda f: self.fragment(f).get("pos", 0))
        return [self.fragment(c) for c in sorted_succ] if data else sorted_succ

    def siblings(self, fragment, data=False):
        """
        Returns the siblings of a fragment.

        Parameters
        ----------
        fragment : str or tuple of object
            Either the fragment id or the fragment (rpst node) itself can be provided.
        data : bool
            Returns also the data dictionaries of the rpst nodes if set to True. Otherwise only
            the ids are returned.
        Returns
        -------
        list of str or list of dict
        """
        f_id = self._fragment_id(fragment)
        p = self.parent(f_id)
        if p is None:
            return None
        else:
            return self.children(p, data=data)

    @staticmethod
    def _fragment_id(fragment):
        if isinstance(fragment, dict):
            fragment = fragment["fragment_id"]
        return fragment

    def parent(self, fragment, data=False):
        """
        Returns the parent of a fragment.

        Parameters
        ----------
        fragment : str or tuple of object
            Either the fragment id or the fragment (rpst node) itself can be provided.
        data : bool
            Returns also the data dictionaries of the rpst node if set to True. Otherwise only
            the ids are returned.
        Returns
        -------
        str or dict
            Returns the parent id or the dictionary of the parent fragment.
        """
        f_id = self._fragment_id(fragment)
        pred = list(self.tree.predecessors(f_id))
        if pred:
            return self.fragment(pred[0]) if data else pred[0]
        else:
            return None

    def root(self):
        """
        Root fragment.
        Returns
        -------
        str
            Returns the id of the RPST root fragment.

        """
        return self.root_id

    def fragment(self, fragment):
        """
        Returns the fragment with the id f_id.
        Parameters
        ----------
        f_id : str

        Returns
        -------
        dict
            Returns the dictionary of a RPST node.
        """
        f_id = self._fragment_id(fragment)
        return self.tree.nodes[f_id]

    def fragments(self, fragment_type=None, data=False):
        """
        Returns all fragments with the specified type.

        Parameters
        ----------
        fragment_type : str or list of str
            Either a single type or a list of types can be provided.
        data : bool
            If set to True, the dictionary of the fragments are returned. Otherwise only
            the ids are returned.

        Returns
        -------
        list of str or list of dict
            Returns a list of fragments with the specified types.
        """
        types = ["trivial", "polygon", "bond", "rigid"]
        if fragment_type is not None:
            if isinstance(fragment_type, str):
                types = [fragment_type]
            elif isinstance(fragment_type, list):
                types = fragment_type

        typed_nodes = []
        for ft in self.tree.nodes(data="fragment_type"):
            if ft[1] in types:
                typed_nodes.append(ft[0])
        return [self.fragment(t) for t in typed_nodes] if data else typed_nodes

    def subgraph(self, fragment):
        """
        Returns a graph based on the nodes and edges contained in the fragment. The graph returned is
        a subgraph of cls.graph. It also contains the dictionaries associated with the nodes and edges
        of cls.graph.

        Parameters
        ----------
        fragment : str or dict
            Either the fragment id or the fragment (dictionary) can be provided.

        Returns
        -------
        networkx.DiGraph
            Returns a subgraph.
        """
        f_id = self._fragment_id(fragment)
        nodes = self.tree.nodes[f_id]['nodes']
        sg = nx.DiGraph()
        sg.add_nodes_from((n, self.graph.nodes[n]) for n in nodes)
        sg.add_edges_from((u, v, d) for u, v in self.graph.adj.items() if u in nodes
                          for v, d in v.items() if v in nodes)
        return sg

    def sort(self, fragment):
        """
        Sorts the fragments of an RPST fragment.
        Parameters
        ----------
        fragment : str or dict
            Either the fragment id or the fragment (dictionary) can be provided.

        """
        f_id = self._fragment_id(fragment)
        fragment = self.fragment(f_id)
        fragments = self.children(fragment, data=True)
        if fragments:
            for f in fragments:
                self.sort(f)
            self._sort_fragments(fragments, fragment)

    def _sort_fragments(self, fragments, parent):
        parent_type = parent["fragment_type"]
        if parent_type == "polygon":
            graph = nx.DiGraph()
            parent_entry = parent["entry_node"]
            graph.add_node(parent_entry)
            for fragment in fragments:
                u = fragment["entry_node"]
                v = fragment["exit_node"]
                graph.add_node(v)
                graph.add_edge(u, v)
            nodes = list(nx.algorithms.topological_sort(graph))

            for i, fragment in enumerate(sorted(fragments, key=lambda f: nodes.index(f["entry_node"]))):
                fragment["pos"] = i

        elif parent_type == "bond":
            trivials = sorted([f for f in fragments if f["fragment_type"] == 'trivial'],
                              key=lambda t: self.fragment_to_string(t))
            polygons = sorted([f for f in fragments if f["fragment_type"] == 'polygon'],
                              key=lambda t: self.fragment_to_string(t))
            bonds = sorted([f for f in fragments if f["fragment_type"] == 'bond'],
                           key=lambda t: self.fragment_to_string(t))
            rigids = sorted([f for f in fragments if f["fragment_type"] == 'rigid'],
                            key=lambda t: self.fragment_to_string(t))

            sorted_fragments = polygons + rigids + bonds + trivials
            for i, f in enumerate(sorted_fragments):
                f["pos"] = i
        else:
            """
            graph = nx.DiGraph()
            parent_entry = parent["entry_node"]
            graph.add_node(parent_entry)
            entry_map = dict()

            for fragment in fragments:
                u = fragment["entry_node"]
                v = fragment["exit_node"]
                graph.add_node(v)
                graph.add_edge(u, v)
            """
            # TODO: implement rigid sorting
            pass

    def fragment_to_string(self, f):
        """
        Generates a description of a fragment.

        Parameters
        ----------
        f : str or dict
            Either the fragment id or the fragment (dictionary) can be provided.

        Returns
        -------
        str
            String description of a fragment.
        """
        f = self._fragment_id(f)
        frag = self.fragment(f)
        ft = frag["fragment_type"]
        if ft == "trivial":
            return "(T "+self.graph.nodes[frag["entry_node"]].get("name", "") + " " + \
                   self.graph.nodes[frag["exit_node"]].get("name", "")+" T)"
        else:
            if ft == "polygon":
                ft_string = "P"
            elif ft == "bond":
                ft_string = "B"
            else:
                ft_string = "R"
            string = "("+ft_string+" "

        for child in self.children(f, data=True):

            string += self.fragment_to_string(child)

        string += " "+ft_string+")"
        return string
