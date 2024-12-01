"""
Imports .pnml files

Notes
_____
Based on [1] http://www.pnml.org/
"""

from xml.etree import ElementTree as ET
from ....rmm4py.models.graph_representation.collaboration_model import CollaborationModel


def load_diagram_from_pnml(filepath):
    """
    Loads a pnml file and creates internal representations of the petri nets (collaboration_model).

    Parameters
    ----------
    filepath : str
        path to pnml file

    Returns
    -------
    processes : list
        nested list of all collaboration models of the given pnml file
    """
    tree = ET.iterparse(filepath)
    for _, el in tree:
        prefix, has_namespace, postfix = el.tag.partition('}')
        if has_namespace:
            # strip all namespaces
            el.tag = postfix
    root = tree.root

    processes = []

    for petrinet in root.findall('net'):
        processes.append(load_petrinet(petrinet))

    return processes

def load_petrinet(petrinet):
    """
    Parses a pbml petri net

    Parameters
    ----------
    petrinet : ET xml element
        petri net xml element

    Returns
    -------
    process_model : collaboration_model
        collaboration model of the given petri net element
    """
    process_model = CollaborationModel()
    petrinet_id = petrinet.attrib['id']
    process_model.processes[petrinet_id] = {'id': petrinet_id}
    #, 'name': petrinet_name}

    for page in petrinet:

        for element in page:

            tag_name = element.tag

            if tag_name == "place" or tag_name == "transition":
                import_flown_node(element, process_model)

            if tag_name == "arc":
                source_id = element.attrib['source']
                target_id = element.attrib['target']
                process_model.process_graph.add_edge(source_id, target_id, id=element.attrib['id'])

    entry_nodes = process_model.get_entry_nodes()
    exit_nodes = process_model.get_exit_nodes()

    all_events = [x for x, y in process_model.process_graph.nodes(data=True) if y['type'] == 'startEvent']

    for event in all_events:
        if event in exit_nodes:
            process_model.process_graph.nodes[event]['type'] = "endEvent"
        elif not (event in entry_nodes):
            process_model.process_graph.nodes[event]['type'] = "intermediateCatchEvent"

    return process_model

def import_flown_node(node, process_model):
    """
    Parses a pnml flow node and adds it to the existing collaboration model

    Parameters
    ----------
    node : ET xml element
        node xml element
    process_model : collaboration_model
        existing collaboration model to add node to
    """
    node_id = node.attrib['id']
    process_model.process_graph.add_node(node_id)

    tag_name = node.tag

    if tag_name == "place":
        process_model.process_graph.nodes[node_id]['type'] = "startEvent"
        for initial_marking in node.findall('initialMarking'):
            for text in initial_marking.findall('text'):
                process_model.process_graph.nodes[node_id]['initialMarking'] = text.text
    elif tag_name == "transition":
        process_model.process_graph.nodes[node_id]['type'] = "task"

    process_model.process_graph.nodes[node_id]['process'] = list(process_model.processes.keys())[0]
    process_model.process_graph.nodes[node_id]['id'] = node_id

    for name in node.findall('name'):
        for text in name.findall('text'):
            process_model.process_graph.nodes[node_id]['name'] = text.text

    for attribute_tag in node.findall('attribute'):
        attribute = {
            'ref': attribute_tag.attrib['typeRef'],
            'value': attribute_tag.attrib['value']
        }
        process_model.process_graph.nodes[node_id]['attribute'] = attribute

        if 'defRef' in node.attrib:
            process_model.process_graph.nodes[node_id]['defRef'] = node.attrib['defRef']
