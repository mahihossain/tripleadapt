"""
Imports .epml files

Notes
-----
Based on [1] Mendling, J., & Nüttgens, M. (2006). EPC markup language (EPML): an XML-based interchange format for
event-driven process chains (EPC). Information systems and e-business management, 4(3), 245-263.
"""
import uuid
from xml.etree import ElementTree as ET
from ....rmm4py.models.graph_representation.collaboration_model import CollaborationModel
import os


def load_epml_directory(directory, recursive=False, randomize_ids=False):
    """
    Loads a directory with .epml files and creates internal representations of the BPMNs (collaboration_model).
    Parameters
    ----------
    directory : str
        path to the directory
    recursive : boolean, optional
        if set true, imports subdirectories
    randomize_ids : bool, optional
        if set true, randomizes all id's used in the epmls

    Returns
    -------
    list of collaboration models
        imported EPMLs

    """
    epmls = []

    for root, dirs, files in os.walk(directory):
        epmls += [load_diagram_from_epml(os.path.join(root, f), randomize_ids) for f in files if f.endswith('.epml')]
        if not recursive:
            break

    return epmls


def load_diagram_from_epml(filepath, randomize_ids=False):
    """
    Loads an epml file and creates internal representations of the EPCs (collaboration_model).

    Parameters
    ----------
    filepath : str
        path to .epml file
    randomize_ids : bool, optional
        if set true, randomizes all id's used in the epmls

    Returns
    -------
    processes : list
        list of all collaboration models of the given epml file
    """

    tree = ET.iterparse(filepath)
    for _, el in tree:
        prefix, has_namespace, postfix = el.tag.partition('}')
        if has_namespace:
            # strip all namespaces
            el.tag = postfix
    root = tree.root

    definitions = []
    attribute_types = []
    processes = []

    for definitions_tag in root.findall('definitions'):
        for definition_tag in definitions_tag.findall('definition'):
            definition = {'defId': definition_tag.attrib['defId']}

            for name in definition_tag.findall('name'):
                definition['name'] = name.text
            for description in definition_tag.findall('description'):
                definition['description'] = description.text

            definitions.append(definition)

    for attribute_types_tag in root.findall('attributeTypes'):
        for attribute_type_tag in attribute_types_tag.findall('attributeType'):
            attribute_type = {'typeId': attribute_type_tag.attrib['typeId']}

            for description in attribute_type_tag.findall('description'):
                attribute_type['description'] = description.text

            attribute_types.append(attribute_type)

    for directory in root.findall('directory'):
        processes.extend(load_directory(directory, definitions, randomize_ids))

    for epc in root.findall('epc'):
        processes.append(load_epc(epc, randomize_ids))

    #unpack the list of list to become a single list
    #process_list = list(np.concatenate(processes))
    process_list = [i for i in iter_flatten(processes)]

    return process_list


def load_directory(directory, definitions, randomize_ids=False):
    """
    Parses an epml directory

    Parameters
    ----------
    directory : ET xml element
        directory xml element
    definitions : list
        list of epml definitions
    randomize_ids : bool, optional
        if set true, randomizes all id's used in the epml

    Returns
    -------
    models : list
        list of all collaboration models of the given directory element
    """

    models = []

    for epc in directory.findall("epc"):
        models.append(load_epc(epc, randomize_ids))

    for sub_directory in directory.findall("directory"):
        models.extend(load_directory(sub_directory, definitions, randomize_ids))

    return models


def load_epc(epc, randomize_ids=False):
    """
    Parses an epml epc

    Parameters
    ----------
    epc : ET xml element
        epc xml element
    randomize_ids : bool, optional
        if set true, randomizes all id's used in the epmls

    Returns
    -------
    process_model : collaboration_model
        collaboration model of the given epc element
    """

    process_model = CollaborationModel()

    epc_id = epc.attrib['epcId']

    if randomize_ids:
        epc_id = str(uuid.uuid1())

    epc_name = epc.attrib['name']

    process_model.name = epc_name
    process_model.processes[epc_id] = {'id': epc_id, 'name': epc_name}

    #save node_ids and randomized node_ids in dictionary
    id_pair = {}


    roles = []
    for child in epc:
        for role in child.findall('role'):
            if randomize_ids:
                part = {
                    'id': str(uuid.uuid1()),
                    'name': role.find('name').text
                }
                id_pair[role.attrib['id']] = part['id']
            else:
                part = {
                    'id': role.attrib['id'],
                    'name': role.find('name').text
                }
            roles.append(part)

        for participant in child.findall('participant'):
            if randomize_ids:
                part = {
                    'id': str(uuid.uuid1()),
                    'name': participant.find('name').text
                }
                id_pair[participant.attrib['id']] = part['id']
            else:
                part = {
                    'id': participant.attrib['id'],
                    'name': participant.find('name').text
                }

            roles.append(part)

    for child in epc:

        tag_name = child.tag

        if tag_name in ("event", "function", "processInterface", "and", "or", "xor"):
            id_pair = import_flown_node(child, process_model, randomize_ids, id_pair)

        if tag_name in ("application", "dataField", "object"):
            id_pair = import_additional_node(child, process_model, randomize_ids, id_pair)

        if tag_name == "relation":
            source_id = child.attrib['from']
            target_id = child.attrib['to']

            source_flow_nodes = [x for x, y in process_model.process_graph.nodes(data=True) if y['id'] == source_id]
            source_additional_nodes = [x for x, y in process_model.additional_nodes(data=True) if y['id'] == source_id]
            target_flow_nodes = [x for x, y in process_model.process_graph.nodes(data=True) if y['id'] == target_id]
            target_additional_nodes = [x for x, y in process_model.additional_nodes(data=True) if y['id'] == target_id]

            if len(source_flow_nodes) != 0:
                target_additional_node = target_additional_nodes[0]
                if target_additional_node['type'] == "dataObject":
                    process_model.process_graph.nodes[source_id]['data_output'] = target_id
                else:
                    #TODO: application etc
                    process_model.process_graph.nodes[source_id]['role'] = target_id
            else:
                source_additional_node = source_additional_nodes[0]
                if source_additional_node['type'] == "dataObject":
                    process_model.process_graph.nodes[target_id]['data_input'] = source_id
                else:
                    # TODO: application etc
                    process_model.process_graph.nodes[target_id]['role'] = source_id

            #TODO

        if tag_name == "arc":
            for flow in child.findall('flow'):
                source_id = flow.attrib['source']
                target_id = flow.attrib['target']
                if randomize_ids:
                    process_model.process_graph.add_edge(id_pair[source_id], id_pair[target_id], id=str(uuid.uuid1()))
                else:
                    process_model.process_graph.add_edge(source_id, target_id, id=child.attrib['id'])

            for relation in child.findall('relation'):
                source_id = relation.attrib['source']
                target_id = relation.attrib['target']
                relation_type = relation.attrib['type']

                if randomize_ids:
                    if relation_type == 'input':
                        process_model.process_graph.nodes[id_pair[target_id]]['data_input'] = id_pair[source_id]
                    elif relation_type == 'output':
                        process_model.process_graph.nodes[id_pair[source_id]]['data_output'] = id_pair[target_id]
                    elif relation_type == 'role':
                        process_model.process_graph.nodes[id_pair[source_id]]['role'] = id_pair[target_id]

                else:
                    if relation_type == 'input':
                        process_model.process_graph.nodes[target_id]['data_input'] = source_id
                    elif relation_type == 'output':
                        process_model.process_graph.nodes[source_id]['data_output'] = target_id
                    elif relation_type == 'role':
                        process_model.process_graph.nodes[source_id]['role'] = target_id

    entry_nodes = process_model.get_entry_nodes()
    exit_nodes = process_model.get_exit_nodes()

    all_events = [x for x, y in process_model.process_graph.nodes(data=True) if y['type'] == 'startEvent']

    for event in all_events:
        if event in exit_nodes:
            process_model.process_graph.nodes[event]['type'] = "endEvent"
        elif not (event in entry_nodes):
            process_model.process_graph.nodes[event]['type'] = "intermediateCatchEvent"

    return process_model


def import_flown_node(node, process_model, randomize_ids, id_pair):
    """
    Parses an epml flow node and adds it to the existing collaboration model

    Parameters
    ----------
    id_pair
    node : ET xml element
        node xml element
    process_model : collaboration_model
        existing collaboration model to add node to
    randomize_ids : bool, optional
        if set true, randomizes all id's used in the epmls
    id_pair : dict
        keeps track of original nodeIDs and randomized counterparts.
    """
    if randomize_ids:
        node_id = str(uuid.uuid1())
        id_pair[node.attrib['id']] = node_id
    else:
        node_id = node.attrib['id']

    process_model.process_graph.add_node(node_id)

    tag_name = node.tag

    if tag_name == "event":
        process_model.process_graph.nodes[node_id]['type'] = "startEvent"
    elif tag_name == "function":
        process_model.process_graph.nodes[node_id]['type'] = "task"
    elif tag_name == "and":
        process_model.process_graph.nodes[node_id]['type'] = "parallelGateway"
    elif tag_name == "or":
        process_model.process_graph.nodes[node_id]['type'] = "inclusiveGateway"
    elif tag_name == "xor":
        process_model.process_graph.nodes[node_id]['type'] = "exclusiveGateway"
    elif tag_name == "processInterface":
        process_model.process_graph.nodes[node_id]['type'] = "subProcess"

    process_model.process_graph.nodes[node_id]['process'] = list(process_model.processes.keys())[0]
    process_model.process_graph.nodes[node_id]['id'] = node_id

    for name in node.findall('name'):
        process_model.process_graph.nodes[node_id]['name'] = name.text

    for attribute_tag in node.findall('attribute'):
        attribute = {
            'ref': attribute_tag.attrib['typeRef'],
            'value': attribute_tag.attrib['value']
        }
        process_model.process_graph.nodes[node_id]['attribute'] = attribute

        if 'defRef' in node.attrib:
            process_model.process_graph.nodes[node_id]['defRef'] = node.attrib['defRef']

    return id_pair


def import_additional_node(node, process_model, randomize_ids, id_pair):
    """
    Parses an additional (non-flow) node and adds it to the existing collaboration model

    Parameters
    ----------
    node : ET xml element
        node xml element
    process_model : collaboration_model
        existing collaboration model to add node to
    randomize_ids : bool, optional
        if set true, randomizes all id's used in the epmls
    id_pair : dict
        keeps track of original nodeIDs and randomized counterparts.
    """

    additional_node = {}

    if randomize_ids:
        additional_node['id'] = str(uuid.uuid1())
        id_pair[node.attrib['id']] = additional_node['id']
    else:
        additional_node['id'] = node.attrib['id']

    tag_name = node.tag

    if tag_name in ("dataField", "object"):
        additional_node['type'] = "dataObject"

        # TODO: application
        # elif tag_name == "application":
        #    pool_process.process_graph.nodes[node_id][consts.Consts.type] = "startEvent"

    if 'name' in node.attrib:
        additional_node['name'] = node.attrib['name']

    #TODO: range?

    if tag_name == "object":
        object_consumed = node.attrib['consumed']
        object_id = node.attrib['id']
        object_optional = node.attrib['optional']
        # object_type = node.attrib['type']
        # z.B. Input
        object_name = node.find('name').text
        #TODO: object

    return id_pair


def iter_flatten(iterable):
    """
    This helper function helps to flatten the list of processes, without running into recursion errors.
    Based on http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html

    Parameters
    ----------
    iterable

    Returns
    -------

    """
    it = iter(iterable)
    for e in it:
        if isinstance(e, (list)):
            for f in iter_flatten(e):
                yield f
        else:
            yield e
