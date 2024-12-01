"""
Internal representation of BPMNs and EPCs
"""
import networkx as nx


class CollaborationModel(object):
    """
    Internal representation of BPMNs and EPCs
    """

    def __init__(self):
        """
        Initializes a BPMN or EPC
        """
        self.process_graph = nx.DiGraph()
        self.processes = {}
        self.name = ""
        self.collaboration_id = ""
        self.pools = {}
        self.subprocesses = {}
        self.additional_nodes = []
        self.lanes = {}
        self.message_flows = {}

    def get_entry_nodes(self):
        """
        Computes all entry nodes of the graph

        Returns
        -------
        entry_nodes: list of networkx nodes
            all entry nodes
        """

        result = []
        for n in self.process_graph.nodes:
            if len(list(self.process_graph.predecessors(n))) == 0:
                result.append(n)

        return result

    def get_exit_nodes(self):
        """
        Computes all exit nodes of the graph

        Returns
        -------
        exit_nodes: list of networkx nodes
            all exit nodes
        """
        result = []
        for n in self.process_graph.nodes:
            if len(list(self.process_graph.successors(n))) == 0:
                result.append(n)

        return result

    def get_nodes_by_type(self, type):
        """
        Returns all nodes of the graph of a specific type

        Parameters
        ----------
        type: str
            type to tutor

        Returns
        -------
        result_nodes : list of networkx nodes
            all nodes of given type
        """
        result = []

        for node in self.process_graph.nodes:
            node_type = self.process_graph.nodes[node]['type']

            if node_type == type:
                result.append((node,self.process_graph.nodes(data=True)[node]))

        return result

    def get_flow_by_id(self, id):
        """
        Returns an edge of the graph with given id

        Parameters
        ----------
        id : str
            id to tutor

        Returns
        -------
        edge: networkx edge
            edge with the given id

        """
        for edge in self.process_graph.edges(data=True):
            if edge[2]['id'] == id:
                return edge
