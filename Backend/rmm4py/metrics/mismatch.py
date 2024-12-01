"""
Calculates the connector mismatch for process models
"""


class Mismatch:
    """
    Class that computes mismatches
    """
    def __init__(self, graph):
        """

        Parameters
        ----------
        model
            the process model
        """

        self.graph = graph
        self.and_splits_list = []
        self.and_joins_list = []
        self.or_splits_list = []
        self.or_joins_list = []
        self.xor_splits_list = []
        self.xor_joins_list = []
        self.connectors_list = []

    def and_splits(self):

        """

        Returns
        -------
            the list of and splits
        """
        return self.and_splits_list

    def and_joins(self):
        """

        Returns
        -------
            the list of and joins
        """
        return self.and_joins_list

    def or_splits(self):
        """

        Returns
        -------
            the list of or splits
        """
        return self.or_splits_list

    def or_joins(self):
        """

        Returns
        -------
            the list of or joins
        """
        return self.or_joins_list

    def xor_splits(self):
        """

        Returns
        -------
            the list of xor splits
        """
        return self.xor_splits_list

    def xor_joins(self):
        """

        Returns
        -------
            the list of xor joins
        """
        return self.xor_joins_list

    def connectors(self):
        """

        Returns
        -------
            the list of all connectors
        """
        return self.connectors_list

    def sort_cons(self):
        """
        Initializes the lists of split and join connectors.
        """

        for node in self.graph.nodes(data='type'):
            in_degree = self.in_degree(node)
            out_degree = self.out_degree(node)
            if node[1] == 'parallelGateway' and out_degree > 1:
                self.and_splits_list.append(node)
                self.connectors_list.append(node)
            elif node[1] == 'parallelGateway' and in_degree > 1:
                self.and_joins_list.append(node)
                self.connectors_list.append(node)
            elif node[1] == 'exclusiveGateway' and out_degree > 1:
                self.xor_splits_list.append(node)
                self.connectors_list.append(node)
            elif node[1] == 'exclusiveGateway' and in_degree > 1:
                self.xor_joins_list.append(node)
                self.connectors_list.append(node)
            elif node[1] == 'inclusiveGateway' and out_degree > 1:
                self.or_splits_list.append(node)
                self.connectors_list.append(node)
            elif node[1] == 'inclusiveGateway' and in_degree > 1:
                self.or_joins_list.append(node)
                self.connectors_list.append(node)

    def mismatch(self):

        """

        Returns
        -------
            the mismatch of the model as an integer
        """

        # AND connectors
        sum1 = 0
        sum2 = 0
        for node in self.and_splits_list:
            sum1 = sum1 + self.out_degree(node)

        for node in self.and_joins_list:

            sum2 = sum2 + self.in_degree(node)

        abs1 = abs(sum1-sum2)

        # OR connectors
        sum1 = 0
        sum2 = 0
        for node in self.or_splits_list:
            sum1 = sum1 + self.out_degree(node)

        for node in self.or_joins_list:
            sum2 = sum2 + self.in_degree(node)

        abs2 = abs(sum1-sum2)

        # XOR connectors
        sum1 = 0
        sum2 = 0
        for node in self.xor_splits_list:
            sum1 = sum1 + self.out_degree(node)

        for node in self.xor_joins_list:
            sum2 = sum2 + self.in_degree(node)

        abs3 = abs(sum1-sum2)

        return abs1 + abs2 + abs3

    def in_degree(self, node):

        """

        Parameters
        ----------
        node
            the specific node

        Returns
        -------
            the in degree of the node
        """
        return int(str(self.graph.in_degree(node)).split(', ')[1].split(')')[0])

    def out_degree(self, node):
        """

        Parameters
        ----------
        node
            the specific node

        Returns
        -------
            the out degree of the node
        """
        return int(str(self.graph.out_degree(node)).split(', ')[1].split(')')[0])

    def degree(self, node):
        """

        Parameters
        ----------
        node
            the specific node

        Returns
        -------
            the degree of the node
        """

        return self.in_degree(node) + self.out_degree(node)
