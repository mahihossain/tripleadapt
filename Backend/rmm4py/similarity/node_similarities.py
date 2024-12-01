"""
Module implements different node similarities and helper functions.
"""
import copy
import rmm4py.similarity.word_similarities as ws
from nltk.corpus import wordnet as wn
from copy import deepcopy
from rmm4py.models.graph_representation.node_types import Event, Task, Others, Gateway
from rmm4py.similarity import language_utils as node_utils
from rmm4py.similarity.language_utils import Language, tokenize, stem_tokens, remove_special_chars, check_synonym, \
    nounify, verbify
from rmm4py.similarity.language_utils import remove_stopwords as rs
from nltk.stem import PorterStemmer

__msg = "Set data=True in graph.nodes(data=True)"


def get_graph_for_node(node, set_of_graphs):
    """
    Finds the graph that contains a node.

    Parameters
    ----------
    node : networkx.Graph.NodeDataView
        NodeDataView
    set_of_graphs : list of networkx.DiGraph

    Returns
    -------
    networkx.DiGraph
    """
    graphs = [graph for graph in set_of_graphs if node[0] in graph]
    graph = graphs[0]

    return graph


def role_sim(set_of_graphs, discriminative_cutoff):
    """
    Functions returns the function calculate_role_similarity which just requires two nodes as inputs,
    with parameters graph1, graph2 and discriminative_cutoff set.

    Parameters
    ----------
    set_of_graphs : list of networkx.DiGraph
        node1 and node2 need to be contained in the graphs from the list.
    discriminative_cutoff : float
            Value between 0.0 and 1.0.
            Adjustment highly recommended.

    Returns
    -------
    function

    """

    def define_node_role(graph, node_id):
        """
        Function defines a node as a start, stop, join, split or regular node based on the number of successors and
        predecessors. Each node can be assigned more than one role_sim.

        Parameters
        ----------
        graph : networkx.DiGraph
        node_id : networkx.Graph.NodeView from the graph

        Returns
        -------
        List of str
            The strings stand for the node roles, e. g. "start"

        References
        ----------
        [1] Z. Yan, R. Dijkman and P. W. P. J. Grefen,
        "Fast Business Process Similarity Search with Feature-Based Similarity Estimation",
        In R. Meersman, T. Dillon and P. Herrero (Eds.),
        Proceedings of the 18th international conference on cooperative information systems
        (Vol. 1, pp. 60-77). (Lecture Notes in Computer Science; Vol. 6426), 2010.
        DOI: 10.1007/978-3-642-16934-2_8
        """

        role = []

        predecessors = list(graph.predecessors(node_id))
        successors = list(graph.successors(node_id))

        # a node without predecessors is a start node
        if not predecessors:
            role.append('start')

        # a node without successors is a stop node
        if not successors:
            role.append('stop')

        # a node with two or more predecessors is a join node
        if len(predecessors) >= 2:
            role.append('join')

        # a node with two or more successors is a split node
        if len(successors) >= 2:
            role.append('split')

        # a node with exactly one successor and one predecessor is a regular node
        if len(predecessors) == 1 and len(successors) == 1:
            role.append('regular')

        return role

    def discriminative_roles(graph_1, graph_2):
        """
        Function determines which roles of nodes have which percentage in the given graphs.
        Returns a list of node roles which have a prevalence in percent below the discriminative
        cutoff and can be used for further role_sim similarity estimations.

        Parameters
        ----------
        graph_1 : networkx.DiGraph
        graph_2 : networkx.DiGraph

        Returns
        -------
        List of strings
            Strings contain names of node roles which have discriminative power.

        See Also
        --------
        define_node_role()

        References
        ----------
        [1] Z. Yan, R. Dijkman and P. W. P. J. Grefen, "Fast Business Process Similarity Search with Feature-Based
        Similarity Estimation", In R. Meersman, T. Dillon and P. Herrero (Eds.), Proceedings of the 18th international
        conference on cooperative information systems (Vol. 1, pp. 60-77).
        (Lecture Notes in Computer Science; Vol. 6426), 2010.
        DOI: 10.1007/978-3-642-16934-2_8

        """

        n_start, n_stop, n_split, n_join, n_regular = 0, 0, 0, 0, 0

        # counts the roles of the nodes for both graphs
        for node1 in graph_1.nodes:
            role1 = define_node_role(graph_1, node1)
            if 'start' in role1:
                n_start = n_start + 1

            if 'stop' in role1:
                n_stop = n_stop + 1

            if 'split' in role1:
                n_split = n_split + 1

            if 'regular' in role1:
                n_regular = n_regular + 1

            if 'join' in role1:
                n_join = n_join + 1

        for node2 in graph_2.nodes:
            role2 = define_node_role(graph_2, node2)
            if 'start' in role2:
                n_start = n_start + 1

            if 'stop' in role2:
                n_stop = n_stop + 1

            if 'split' in role2:
                n_split = n_split + 1

            if 'regular' in role2:
                n_regular = n_regular + 1

            if 'join' in role2:
                n_join = n_join + 1

        # determines the fraction of the nodes with each specific role_sim and appends
        # the role_sim to disc_roles if the fraction is below the given threshold.
        disc_roles = []
        n_nodes = graph_1.number_of_nodes() + graph_2.number_of_nodes()
        if n_start / n_nodes <= discriminative_cutoff:
            disc_roles.append('start')

        if n_stop / n_nodes <= discriminative_cutoff:
            disc_roles.append('stop')

        if n_split / n_nodes <= discriminative_cutoff:
            disc_roles.append('split')

        if n_regular / n_nodes <= discriminative_cutoff:
            disc_roles.append('regular')

        if n_join / n_nodes <= discriminative_cutoff:
            disc_roles.append('join')

        return disc_roles

    def calculate_role_similarity(node1, node2):
        """
        Function determines the role_sim similarity of the two given nodes based on their position
        in the graphs and the percentage of nodes with the same role_sim.
        If the roles of the nodes are not of discriminative power, the function returns zero.

        Parameters
        ----------
        node1 : networkx.Graph.NodeDataView
        node2 : networkx.Graph.NodeDataView

        Returns
        -------
        float
            Similarity value between 0 and 1.

        See Also
        --------
        define_node_role()
        discriminative_roles()

        References
        ----------
        [1] Z. Yan, R. Dijkman and P. W. P. J. Grefen,
        "Fast Business Process Similarity Search with Feature-Based Similarity Estimation",
        In R. Meersman, T. Dillon and P. Herrero (Eds.),
        Proceedings of the 18th international conference on cooperative information systems
        (Vol. 1, pp. 60-77). (Lecture Notes in Computer Science; Vol. 6426), 2010.
        DOI: 10.1007/978-3-642-16934-2_8
        """

        if (isinstance(node1, tuple) or isinstance(node2, tuple)) is False:
            raise TypeError(__msg)

        graph1 = get_graph_for_node(node1, set_of_graphs)
        graph2 = get_graph_for_node(node2, set_of_graphs)

        # determines the role_sim of the nodes and the number of successors and predecessors.
        role1 = define_node_role(graph1, node1[0])
        predecessors1 = [pred for pred in graph1.predecessors(node1[0])]
        successors1 = [suc for suc in graph1.successors(node1[0])]
        no_pred1 = len(predecessors1)
        no_suc1 = len(successors1)

        role2 = define_node_role(graph2, node2[0])
        predecessors2 = [pred for pred in graph2.predecessors(node2[0])]
        successors2 = [suc for suc in graph2.successors(node2[0])]
        no_pred2 = len(predecessors2)
        no_suc2 = len(successors2)

        # determines which roles the two nodes have in common
        croles = [value for value in role1 if value in role2]
        # determines which roles are of discriminative power from the two graphs
        disc_roles = discriminative_roles(graph1, graph2)

        # calculation of the role_sim similarity based on the common roles of the nodes
        # and the amount of successors and predecessors.
        if 'start' in croles and 'stop' in croles:
            # special case of a graph with one node.
            rsim = 1

        elif 'start' in croles and 'stop' not in croles:
            rsim = 1 - (abs(no_suc1 - no_suc2) / (2 * (no_suc1 + no_suc2)))

        elif 'start' not in croles and 'stop' in croles:
            rsim = 1 - (abs(no_pred1 - no_pred2) / (2 * (no_pred2 + no_pred1)))

        else:
            rsim = 1 - (abs(no_suc1 - no_suc2) / (2 * (no_suc1 + no_suc2))) \
                   - (abs(no_pred1 - no_pred2) / (2 * (no_pred2 + no_pred1)))

        # determination of the role_sim similarity taking into account the discriminative roles
        # just if all roles the nodes share are also of discriminative power, the role_sim similarity
        # is returned. Otherwise the method returns 0.
        if all(roles in disc_roles for roles in croles):
            rdsim = rsim

        else:
            rdsim = 0

        return rdsim

    return calculate_role_similarity


def equal_label_sim():
    """
    Functions returns the function calculate_equal_label_similarity which just requires two nodes as inputs,
    with parameters graph1 and graph2 set.

    Returns
    -------
    function

    """

    def calculate_equal_label_similarity(node1, node2):
        """
        Function compares the labels of different nodes. If the labels are identical, it returns one, otherwise zero.
        If the nodes have no label (e. g. Gateways) the type is compared. If the type is identical, returns 1,
        otherwise 0.

        Parameters
        ----------
        node1 : networkx.Graph.NodeDataView
        node2 : networkx.Graph.NodeDataView

        Returns
        -------
        float
           Value is 0.0 or 1.0
        """

        if (isinstance(node1, tuple) or isinstance(node2, tuple)) is False:
            raise TypeError(__msg)

        name1 = ""
        name2 = ""

        if 'name' in node1[1]:
            name1 = node1[1]['name']

        if 'name' in node2[1]:
            name2 = node2[1]['name']

        if name1 == name2:

            if name1 == "":
                type1 = node1[1]['type']
                type2 = node2[1]['type']

                if type1 != type2:
                    return 0.0

            return 1.0

        return 0.0

    return calculate_equal_label_similarity


def la_rosa_sim(set_of_graphs, sim):
    """
    Functions returns the function calculate_la_rosa_similarity which just requires two nodes as inputs,
    with parameters graph1, graph2 and sim set.

    Parameters
    ----------
    set_of_graphs : list of networkx.DiGraph
        node1 and node2 need to be contained in the graphs from the list
    sim : function
        node similarity function, accepting only two nodes as inputs

    Returns
    -------
    function
    """

    def get_type(graph, node):
        """
        Returns the type of a node

        Parameters
        ----------
        graph : networkx.DiGraph
            graph the node is contained
        node : networkx.Graph.NodeDataView
            node to check type

        Returns
        -------
        type: str
            type of the node
        """
        node_type = node[1]['type']

        if node_type in Event.__members__:
            return Event.event

        elif node_type in Task.__members__:
            return Task.function

        elif node_type in Others.__members__:
            return "other"

        else:
            successor_length = len(list(graph.successors(node[0])))

            if successor_length > 1:
                return "split"
            else:
                return "join"

    def calculate_la_rosa_similarity(node1, node2):
        """
        Calculates the La Rosa Similarity of two nodes

        Parameters
        ----------
        node1 : networkx.Graph.NodeDataView
        node2 : networkx.Graph.NodeDataView

        Returns
        -------
        similarity: float
            resulting La Rosa Similarity

        Notes
        -----
        Based on [1] La Rosa, M., Dumas, M., Uba, R., & Dijkman, R. (2010, October). Merging business process models.
        In OTM Confederated International Conferences" On the Move to Meaningful Internet Systems" (pp. 96-113).
        Springer, Berlin, Heidelberg.

        """

        graph1 = get_graph_for_node(node1, set_of_graphs)
        graph2 = get_graph_for_node(node2, set_of_graphs)

        if not graph1.has_node(node1[0]):
            return calculate_la_rosa_similarity

        type1 = get_type(graph1, node1)
        type2 = get_type(graph2, node2)

        if type1 != type2 or type1 == "other":
            return 0

        if 'name' not in node1[1]:
            return 'CONTEXT'

        else:
            return sim(node1, node2)

    return calculate_la_rosa_similarity


def bag_of_words_sim(word_sim=ws.levenshtein_sim(), stemming=False, stemmer=None,
                     remove_stopwords=False, lang=None):
    """
    Functions returns the function calculate_bow_similarity which just requires two nodes as inputs,
    with parameters graph1, graph2, word_sim, stemming, stemmer, remove_stopwords and lang set.

    Parameters
    ----------
    word_sim : function
        word similarity function, accepting only two words as inputs
    stemming : bool, optional
        If set true, words will be stemmed before similarity computation
    stemmer : stemmer, optional
        stemmer to use
    remove_stopwords : bool, optional
        If set true, stopwords will be removed
    lang : language, optional
        language to use

    Returns
    -------
    function
    """

    def calculate_bow_similarity(node1, node2):
        """
        Calculates the Bag Of Words Similarity of two nodes

        Parameters
        ----------
        node1 : networkx.Graph.NodeDataView
            first node
        node2 : networkx.Graph.NodeDataView
            second node

        Returns
        -------
        similarity : float
            resulting Bag Of Words similarity
        """

        if (isinstance(node1, tuple) and isinstance(node2, tuple)) is False:
            raise TypeError(__msg)

        tokens1 = node_utils.tokenize(node1[1]['name'])
        tokens2 = node_utils.tokenize(node2[1]['name'])

        if remove_stopwords:
            tokens1 = rs(tokens1, lang)
            tokens2 = rs(tokens2, lang)

        if stemming:
            tokens1 = stem_tokens(tokens1, lang, stemmer)
            tokens2 = stem_tokens(tokens2, lang, stemmer)

        cum_sim = 0

        for token1 in tokens1:

            max_sim = 0

            for token2 in tokens2:
                sim = word_sim(token1, token2)
                max_sim = max(sim, max_sim)

            cum_sim = cum_sim + max_sim

        for token2 in tokens2:

            max_sim = 0

            for token1 in tokens1:
                sim = word_sim(token1, token2)
                max_sim = max(sim, max_sim)

            cum_sim = cum_sim + max_sim

        return cum_sim / (len(tokens1) + len(tokens2))

    return calculate_bow_similarity


def context_sim(set_of_graphs, mapping):
    """
    Functions returns the function calculate_bow_similarity which just requires two nodes as inputs,
    with parameters graph1, graph2, mapping set.

    Parameters
    ----------
    set_of_graphs : list of networkx graph
        node1 and node2 need to be contained in the graphs from the list.
    mapping : dict
        mapping of graph1 and graph2

    Returns
    -------
    function
    """

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
            node_type = graph.nodes[predecessor]['type']

            if node_type in Gateway.__members__ or 'name' not in graph.nodes[predecessor]:
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
            node_type = graph.nodes[successor]['type']

            if node_type in Gateway.__members__ or 'name' not in graph.nodes[successor]:
                recursive = get_successors(successor, graph, visited)

                for n in recursive:
                    if n not in result:
                        result.append(n)

            else:
                result.append(successor)

        return result

    def calculate_context_similarity(node1, node2):
        """
        Calculates the context_sim similarity of two nodes

        Parameters
        ----------
        node1 : networkx.Graph.NodeDataView
        node2 : networkx.Graph.NodeDataView

        Returns
        -------
        similarity : float
            resulting context_sim similarity
        Notes
        _____
        Based on [1] La Rosa, M., Dumas, M., Uba, R., & Dijkman, R. (2010, October).
        Merging business process models. In OTM Confederated International Conferences"
        On the Move to Meaningful Internet Systems" (pp. 96-113). Springer, Berlin, Heidelberg.
        """
        if (isinstance(node1, tuple) or isinstance(node2, tuple)) is False:
            raise TypeError(__msg)

        graph1 = get_graph_for_node(node1, set_of_graphs)
        graph2 = get_graph_for_node(node2, set_of_graphs)

        node1_predecessors = get_predecessors(node1[0], graph1, [])
        node2_predecessors = get_predecessors(node2[0], graph2, [])

        node1_successors = get_successors(node1[0], graph1, [])
        node2_successors = get_successors(node2[0], graph2, [])

        map1 = []
        map2 = []

        pre1_matches = []
        succ1_matches = []

        for pre1 in node1_predecessors:
            if pre1 in mapping.keys():
                for match in mapping[pre1]:
                    pre1_matches.append(match[0])

        for succ1 in node1_successors:
            if succ1 in mapping.keys():
                for match in mapping[succ1]:
                    succ1_matches.append(match[0])

        for pre2 in node2_predecessors:
            if pre2 in pre1_matches:
                map1.append(pre2)

        for succ2 in node2_successors:
            if succ2 in succ1_matches:
                map2.append(succ2)

        dividor = (max(node1_predecessors.__len__(), node2_predecessors.__len__())
                   + max(node1_successors.__len__(), node2_successors.__len__()))

        if dividor == 0:
            return 0

        context = (map1.__len__() + map2.__len__()) / dividor

        return context

    return calculate_context_similarity


def porter_sim(set_of_graphs, remove_character_list=None, words_ignore_list=None):
    """
        Functions returns the function calculate_porter_similarity which just requires two nodes as inputs,
        with parameters set_of_graphs, remove_character_list and words_ignore_list.

        Parameters
        ----------
        set_of_graphs : list of networkx.DiGraph
            node1 and node2 need to be contained in the graphs from the list.
        remove_character_list : string list
            optional: list of characters to remove
        words_ignore_list : string list
            optional: list of words to ignore

        Returns
        -------
        function
    """

    if remove_character_list is None:
        remove_character_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "!", "?", "%", "'", "'s", "*",
                                 "<", ">", "(", ")", "/", ";", ",", "."]
    if words_ignore_list is None:
        words_ignore_list = ["to", "and", "or", "of", "for", "by", "is", "if", "then", "else", "is", "are", "the",
                             "with", "on", "has", "have", "about", "above", "within", "top", "letter", "a", "as", "in",
                             "other", "according"]
    builder = dict()

    def are_antonyms(wordstems1, wordstems2, synonyms1, synonyms2, antonyms1, antonyms2):
        """
            Checks if two words are antonyms

            Parameters
            ----------
            wordstems1 : dict
                the wordstems of the first word
            wordstems2 : dict
                the wordstems of the second word
            synonyms1 : dict
                the synonymsof the first word
            synonyms2 : dict
                the synonyms of the second word
            antonyms1 : dict
                the antonyms of the first word
            antonyms2 : dict
                the antonyms of the second word

            Returns
            -------
                False if they are not antonyms, else True
        """
        if "not" in wordstems1 and not "not" in wordstems2:
            return True
        if "not" in wordstems2 and not "not" in wordstems1:
            return True
        for syns in synonyms1.values():

            syns2 = set(syns)
            for ants in antonyms2.values():
                ants2 = set(ants)
                # same elements

                num_intersection = len(list(syns2 & ants2))
                if num_intersection > 0:
                    return True
        for ants in antonyms1.values():
            ants2 = set(ants)
            for syns in synonyms2.values():
                syns2 = set(syns)
                # same elements
                num_intersection = len(list(syns2 & ants2))
                if num_intersection > 0:
                    return True
        return False

    def build(label):
        """
            Builds the synonyms,antonyms and wordstems of a label

            Parameters
            ----------
            label : string
                a label of a node
            Returns
            -------
                synonyms, antonyms, wordstems
        """

        synonyms = dict()
        antonyms = dict()
        nouns = dict()
        verbs = dict()
        wordstems = []
        original_words = dict()

        label.lower()
        label.replace("\n", " ")
        label.replace("\r", " ")

        label_components = label.split(" ")
        label_components2 = []
        for word in label_components:
            word.strip()
            for char in remove_character_list:
                word.replace(char, "")
            if word not in words_ignore_list:
                label_components2.append(word)
        label_components = label_components2

        for component in label_components:
            ps = PorterStemmer()
            wordstem = ps.stem(component)

            wordstems.append(wordstem)
            original_words[wordstem] = component

            wn_synset = wn.synsets(component)

            verbify_syns_of_noun = []
            noun_wn_syns = []

            verb_wn_syns = []
            nounify_syns_of_verb = []
            antonyms1 = []
            synonyms[wordstem] = []
            antonyms[wordstem] = []
            nouns[wordstem] = []
            verbs[wordstem] = []

            if wn_synset:
                for s in wn_synset:
                    if s.name().split('.')[1] == 'n':
                        for l in s.lemmas():
                            noun_wn_syns.append(l.name())
                            verbify_syns_of_noun = verbify_syns_of_noun + (verbify(component))

                            if l.antonyms():
                                antonyms1.append(l.antonyms()[0].name())
                    if s.name().split('.')[1] == 'v':
                        for l in s.lemmas():
                            verb_wn_syns.append(l.name())
                            nounify_syns_of_verb = nounify_syns_of_verb + (nounify(component))

                            if l.antonyms():
                                antonyms1.append(l.antonyms()[0].name())

                nouns[wordstem] = verbify_syns_of_noun
                for syn in noun_wn_syns:
                    if syn not in list(nouns.values()):
                        nouns[wordstem].append(syn)
                    if syn not in list(synonyms.values()):
                        synonyms[wordstem].append(syn)

                verbs[wordstem] = nounify_syns_of_verb
                for syn in verb_wn_syns:
                    if syn not in list(verbs.values()):
                        verbs[wordstem].append(syn)
                    if syn not in list(synonyms.values()):
                        synonyms[wordstem].append(syn)

                # antonyms
                antonyms1 = list(set(antonyms1))
                if antonyms1:
                    antonyms[wordstem] = antonyms1
        return synonyms, antonyms, wordstems

    def calculate_porter_similarity(node1, node2):
        """
        Function calculates the porter similarity of two nodes.

        Parameters
        ----------
        node1: networkx.Graph.NodeDataView
            Label representation of the node of the process model.
        node2: networkx.Graph.NodeDataView
            Label representation of the node of the process model.
        set_of_graphs : list of networkx.DiGraph
        remove_character_list : string list
            list of characters to remove
        words_ignore_list : string list
            list of words to ignore
        builder : dict
            a dict containing words and their synonyms

        Returns
        -------
            similarity: float
                Degree of similarity, based on equivalence between the wordstems of words they consist of.
        """
        if (isinstance(node1, tuple) or isinstance(node2, tuple)) is False:
            raise TypeError(__msg)

        graph1 = get_graph_for_node(node1, set_of_graphs)
        try:
            label1 = graph1.nodes()[node1[0]]['name']
        except KeyError:
            return 0.0
        graph2 = get_graph_for_node(node2, set_of_graphs)
        try:
            label2 = graph2.nodes()[node2[0]]['name']
        except KeyError:
            return 0.0

        if (graph1, node1) in builder:
            wert_tupel = builder[(graph1, node1)]
            synonyms1 = wert_tupel[0]
            antonyms1 = wert_tupel[1]
            wordstems1 = wert_tupel[2]
        else:
            synonyms1, antonyms1, wordstems1 = build(label1)
            builder[(graph1, node1)] = (synonyms1, antonyms1, wordstems1)
        if (graph2, node2) in builder:
            wert_tupel = builder[(graph2, node2)]
            synonyms2 = wert_tupel[0]
            antonyms2 = wert_tupel[1]
            wordstems2 = wert_tupel[2]
        else:
            synonyms2, antonyms2, wordstems2 = build(label2)
            builder[(graph2, node2)] = (synonyms2, antonyms2, wordstems2)
        tup1 = (synonyms1, antonyms1, wordstems1)
        tup2 = (synonyms2, antonyms2, wordstems2)
        ignore = "This_node_had_no_label_"
        if label1.startswith(ignore) or label2.startswith(ignore):
            return 0.0
        if label1 == label2:
            return 100.0
        if are_antonyms(wordstems1, wordstems2, synonyms1, synonyms2, antonyms1, antonyms2):
            return 0.0

        # compare wordstems and generated synonym lists
        number_wordstems_word1 = len(wordstems1)
        number_wordstems_word2 = len(wordstems2)
        if number_wordstems_word1 > number_wordstems_word2:
            # order
            node_temp = copy.deepcopy(tup1)
            tup1 = copy.deepcopy(tup2)
            tup2 = copy.deepcopy(node_temp)
        count_wordstem_mappings = 0
        for wordstem1 in tup1[2]:
            for wordstem2 in tup2[2]:

                if wordstem1 == wordstem2:
                    count_wordstem_mappings = count_wordstem_mappings + 1
                    break
                else:
                    # take synonymes into account
                    synnn = tup1[0]
                    for synonym in synnn[wordstem1]:
                        if synonym == wordstem2:
                            count_wordstem_mappings = count_wordstem_mappings + 1
                            break
        similarity = round((2 * count_wordstem_mappings / (number_wordstems_word1 + number_wordstems_word2)) * 100, 2)
        return similarity

    return calculate_porter_similarity


def semantic_sim(lang=Language.ENGLISH,
                 remove_spec_chars=True,
                 remove_all_stopwords=True,
                 stemmed=True):
    """
    Functions returns the function calculate_semantic_similarity which just requires two nodes as inputs
    and specification of relevant flags.

    Parameters
    ----------
    lang: language
        Language of the string to be analysed.
    remove_spec_chars: bool
        If true, special characters such as ".,'{[' will be removed.
    remove_all_stopwords: bool
        If true, stopwords will be removed.
    stemmed: bool
        If true, function will be stemmed.

    Returns
    -------
    Function - calculate_syntactic_similarity().
    """

    def calculate_semantic_similarity(node1, node2):
        """
        Function calculates Semantic Similarity of two nodes.

        Parameters
        ----------
        node1: networkx.Graph.NodeDataView
            Label representation of the node of the process model.
        node2: networkx.Graph.NodeDataView
            Label representation of the node of the process model.

        Returns
        -------
            similarity: float
                Degree of similarity, based on equivalence between the words they consist of.
                An exact match is assumed to be preferred over a match on synonyms.
        """
        if (isinstance(node1, tuple) or isinstance(node2, tuple)) is False:
            raise TypeError(__msg)

        name1 = str(node1[1]['name'])
        name2 = str(node2[1]['name'])

        token1 = tokenize(name1.lower())
        token2 = tokenize(name2.lower())

        max_length = max(len(token1), len(token2))

        if max_length == 0:
            print("ZeroDivisionError - no of items of the max label cannot be 0")
            raise ZeroDivisionError

        if remove_spec_chars:
            token1 = remove_special_chars(token1)
            token2 = remove_special_chars(token2)

        if remove_all_stopwords:
            token1 = rs(token1, lang)
            token2 = rs(token2, lang)

        if stemmed:
            stemmed1 = stem_tokens(token1, lang)
            stemmed2 = stem_tokens(token2, lang)
        else:
            # deepcopy to assure reference to a separate list
            stemmed1 = deepcopy(token1)
            stemmed2 = deepcopy(token2)

        same_strings = 0
        factor = 0
        for i, this_word in enumerate(stemmed1, start=0):
            for j, other_word in enumerate(stemmed2, start=0):
                if this_word == other_word:
                    del token1[i - factor]
                    del token2[j - factor]
                    same_strings += 1
                    factor += 1

        synonyms = 0
        for this_word in token1:
            for other_word in token2:
                if check_synonym(this_word, other_word):
                    synonyms += 1

        return ((1.0 * same_strings) + (0.75 * synonyms)) / max_length

    return calculate_semantic_similarity


def syntactic_sim(remove_spec_chars=True):
    """
    Functions returns the function calculate_syntactic_similarity which just requires two nodes as inputs
    and specification of the remove special characters flag.

    Parameters
    ----------
    remove_spec_chars : bool
        If true, special characters such as ".,'{[' will be removed.

    Returns
    -------
    Function - calculate_syntactic_similarity().
    """

    def calculate_syntactic_similarity(node1, node2):
        """
        Function calculates Syntactic Similarity of two nodes.

        Parameters
        ----------
        node1: networkx.Graph.NodeDataView
            Label representation of the node of the process model.
        node2: networkx.Graph.NodeDataView
            Label representation of the node of the process model.

        Returns
        -------
            similarity: float
                Degree of similarity as measured by the string-edit distance.
        """
        if (isinstance(node1, tuple) or isinstance(node2, tuple)) is False:
            raise TypeError(__msg)

        name1 = str(node1[1]['name'])
        name2 = str(node2[1]['name'])

        token1 = tokenize(name1)
        token2 = tokenize(name2)

        if remove_spec_chars:
            token1 = remove_special_chars(token1)
            token2 = remove_special_chars(token2)

        string1 = ' '.join(token1).lower()
        string2 = ' '.join(token2).lower()

        dist_fun = ws.levenshtein_dist()
        string_distance = dist_fun(string1, string2)
        max_length = max(len(string1), len(string2))

        if max_length == 0:
            print("ZeroDivisionError - at least one of the strings (labels) must be not empty")
            raise ZeroDivisionError
        else:
            return 1 - (string_distance / max_length)

    return calculate_syntactic_similarity
