"""
Internal representation of HERAKLIT artifacts
"""

import networkx as nx
import uuid


class Module:
    """
    Internal representation of HERAKLIT modules
    """

    def __init__(self, label, inner, left_interface, right_interface):
        """
        Initializes a HERAKLIT module

        Parameters
        ----------
        label: str
            the name of the module
        inner: Scheme
            the inner of the module
        left_interface: list of Node
            a list of nodes representing the left interface
        right_interface: list of Node
            a list of nodes representing the right interface
        """
        self.id = uuid.uuid4()
        self.label = label
        self.inner = inner
        self.left_interface = left_interface
        self.right_interface = right_interface
        self.submodules = []


class Signature:
    """
    Internal representation of a HERAKLIT signature
    """

    def __init__(self, terms, functions):
        """
        Initializes a HERAKLIT signature

        Parameters
        ----------
        terms: dict or None
            a dictionary containing a list for each term e.g. variables or sorts
        functions: dict or None
            a dictionary containing available functions in the signature
        """
        self.id = uuid.uuid4()
        self.terms = terms
        self.functions = functions


class Scheme:
    """
    Internal representation of a HERAKLIT scheme
    """

    def __init__(self, graph, signature):
        """
        Initializes a HERAKLIT scheme

        Parameters
        ----------
        graph: networkx.DiGraph or None
            a graph of type DiGraph
        signature: Signature
            the signature for the scheme
        """
        self.id = uuid.uuid4()
        self.nodes = []
        self.edges = []
        if graph is None:
            self.graph = nx.DiGraph()
        else:
            self.graph = graph
            for node in graph.nodes(data=True):
                if node[1]['attributes']['type'] == 'place':
                    self.nodes.append(Place(label=node[1]['attributes']['name'],
                                            content=node[1]['attributes']['content'],
                                            capacity=node[1]['attributes']['capacity']))
                elif node[1]['attributes']['type'] == 'transition':
                    self.nodes.append(Transition(label=node[1]['attributes']['name'],
                                                 condition=node[1]['attributes']['condition']))
            for edge in graph.edges(data=True):
                self.edges.append(Edge(source=edge[0], target=edge[1], term=edge[2]['attributes']['term']))
        self.signature = signature

    def add_node(self, node):
        """
        Inserts a new node to the scheme

        Parameters
        ----------
        node: Node
            the node to be added to the scheme
        """
        if node not in self.nodes:
            self.nodes.append(node)
            if type(node) == Transition:
                self.graph.add_node(node.id, attributes={'type': 'transition', 'name': node.label,
                                                         'condition': node.condition})
            elif type(node) == Place:
                self.graph.add_node(node.id, attributes={'type': 'place', 'name': node.label, 'content': node.content,
                                                         'capacity': node.capacity})

    def add_edge(self, source, target, term):
        """
        Inserts a new edge to the scheme

        Parameters
        ----------
        source: Node
            the source node to generate an edge from
        target: Node
            the target node to generate an edge to
        term
            a lambda function representing a term for the edge

        Returns
        -------
        object
        """
        edge = Edge(source=source.id, target=target.id, term=term)
        self.edges.append(edge)
        if source not in self.nodes:
            self.nodes.append(source)
            self.add_node(source)
        if target not in self.nodes:
            self.nodes.append(target)
            self.add_node(target)
        self.graph.add_edge(source.id, target.id, attributes={'term': term})


class Node:
    """
    Internal representation of basic Nodes
    """

    def __init__(self, label):
        """
        Initializes a basic node

        Parameters
        ----------
        label: str
            the label for the node
        """
        self.label = label
        self.id = uuid.uuid4()


class Place(Node):
    """
    Internal representation of places
    """

    def __init__(self, label, content, capacity):
        """
        Initializes a place

        Parameters
        ----------
        label: str
            the label for the place
        content: object
            the content of the place
        capacity: int or None
            the capacity of the place
        """
        super().__init__(label)
        self.content = content
        self.capacity = capacity


class Transition(Node):
    """
    Internal representation of transitions
    """

    def __init__(self, label, condition):
        """
        Initializes a transition

        Parameters
        ----------
        label: str
            the label for the transition
        condition
            a lambda function returning a boolean value
        """
        super().__init__(label)
        self.condition = condition


class Edge:
    """
    Internal representation of edges
    """

    def __init__(self, source, target, term):
        """
        Initializes an edge

        Parameters
        ----------
        source: node
            the source node
        target: node
            the target node
        term
            a lambda function representing a term for the edge
        """
        self.id = uuid.uuid4()
        self.source = source
        self.target = target
        self.term = term
        self.label = "."


def compose(module1, module2):
    """
    Composes two modules based on the right interface of module1 and the left interface of module2

    Parameters
    ----------
    module1: Module
        the first module
    module2: Module
        the second module

    Returns
    -------
    composition: Module
        the composed module of module1 and module2
    """
    # merge signature terms
    terms = {}
    if module1.inner.signature.terms is not None:
        if module2.inner.signature.terms is not None:
            for t in module1.inner.signature.terms:
                terms[t] = module1.inner.signature.terms[t]
            for t in module2.inner.signature.terms:
                if t not in terms.keys():
                    terms[t] = module2.inner.signature.terms[t]
                else:
                    for e in module2.inner.signature.terms[t]:
                        terms[t].append(e)
        else:
            terms = module1.inner.signature.terms
    elif module2.inner.signature.terms is not None:
        terms = module2.inner.signature.terms

    # merge signature functions
    functions = {}
    if module1.inner.signature.functions is not None:
        if module2.inner.signature.functions is not None:
            for f in module1.inner.signature.functions:
                functions[f] = module1.inner.signature.functions[f]
            for f in module2.inner.signature.functions:
                if f not in functions.keys():
                    functions[f] = module2.inner.signature.functions[f]
                else:
                    for e in module2.inner.signature.functions[f]:
                        functions[f].append(e)
        else:
            functions = module1.inner.signature.functions
    elif module2.inner.signature.functions is not None:
        functions = module2.inner.signature.functions

    # create new signature
    signature = Signature(terms=terms, functions=functions)

    # merge the two graphs
    # create mapping to change the node id of the connections
    mapping = {}

    # create left and right interface
    r_interface = module1.right_interface + module2.right_interface
    l_interface = module1.left_interface + module2.left_interface

    for n1 in module1.right_interface:
        for n2 in module2.left_interface:
            if n1.label == n2.label:
                mapping[n2.id] = n1.id
                r_interface.remove(n1)
                l_interface.remove(n2)

    # compose the two graphs based on the connections
    graph = nx.compose(module1.inner.graph, nx.relabel_nodes(module2.inner.graph, mapping))

    # create new scheme
    scheme = Scheme(graph=graph, signature=signature)

    # create the composed module
    composition = Module(label=module1.label + " ⋅ " + module2.label, inner=scheme, right_interface=r_interface,
                         left_interface=l_interface)

    # add submodels to composed module
    composition.submodules = [module1, module2]

    return composition
