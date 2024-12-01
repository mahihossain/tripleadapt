"""
Exports Collaboration Models as .epml file
"""
import xml.etree.cElementTree as eTree
from rmm4py.models.graph_representation.node_types import Gateway, Event, Task
from rmm4py.models.graph_representation.collaboration_model import CollaborationModel
from rmm4py.models.exporter.indent import indent


def export_epml(epml2, file):
    """
    Exports a collaboration model as a .epml file

    Parameters
    ----------
    epml2 : collaboration_model or list of collaboration_models
        given collaboration model

    file : string
        path to an .epml file to export the collaboration model into

    Returns
    -------
    epml file
    """

    root = create_definitions_element()

    # if imported file is bpmn
    if isinstance(epml2, CollaborationModel):
        collaboration_models = [epml2]

    # if imported file is epml
    else:
        collaboration_models = epml2

        # if imported file is epml with various processes.
        if not isinstance(epml2[0], CollaborationModel):
            collaboration_models = epml2[0]
            collaboration_models = collaboration_models[0]

    directory = eTree.SubElement(root, "directory", {"name": "root"})

    for i in range(len(collaboration_models)):

        epml = collaboration_models[i]

        epc = eTree.SubElement(directory, "epc")
        epc.set("epcId", epml.processes[next(iter(epml.processes))]['id'])
        epc.set("name", epml.name)

        graph = epml.process_graph

        for node in graph.nodes:

            typ = graph.nodes[node]['type']

            if typ in Event.__members__:
                event = eTree.SubElement(epc, "event", {"id": graph.nodes[node]['id']})
                name = eTree.SubElement(event, "name", attrib={}, )

            elif typ in Task.__members__:
                function = eTree.SubElement(epc, "function", {"id": graph.nodes[node]['id']})
                name = eTree.SubElement(function, "name", attrib={}, )

            elif typ in Gateway.__members__:
                if (Gateway[typ] is Gateway.AND) or (Gateway[typ] is Gateway.parallelGateway):
                    and_gate = eTree.SubElement(epc, "and", {"id": graph.nodes[node]['id']})
                    name = eTree.SubElement(and_gate, "name", attrib={}, )

                elif (Gateway[typ] is Gateway.XOR) or (Gateway[typ] is Gateway.exclusiveGateway) or \
                        (Gateway[typ] is Gateway.eventBasedGateway):
                    xor_gate = eTree.SubElement(epc, "xor", {"id": graph.nodes[node]['id']})
                    name = eTree.SubElement(xor_gate, "name", attrib={}, )

                elif (Gateway[typ] is Gateway.OR) or (Gateway[typ] is Gateway.complexGateway) \
                        or (Gateway[typ] is Gateway.inclusiveGateway):
                    or_gate = eTree.SubElement(epc, "or", {"id": graph.nodes[node]['id']})
                    name = eTree.SubElement(or_gate, "name", attrib={}, )

                else:
                    or_gate = eTree.SubElement(epc, "or", {"id": graph.nodes[node]['id']})
                    name = eTree.SubElement(or_gate, "name", attrib={}, )

            else:
                raise ValueError

            # TODO: adjust for BPMN
            if 'name' in graph.nodes[node]:
                name.text = graph.nodes[node]['name']

            elif typ == Gateway.parallelGateway:
                name.text = "∧"

            elif typ == Gateway.exclusiveGateway or Gateway.eventBasedGateway:
                name.text = "x"

            else:
                # TODO: replace with real sign.
                name.text = "∨"

        for edge in graph.edges:

            arc = eTree.SubElement(epc, "arc", {"id": graph.edges[edge]['id']})
            name = eTree.SubElement(arc, "flow", attrib={"source": edge[0], "target": edge[1]}, )

    indent(root)
    tree = eTree.ElementTree(root)
    tree.write(file, encoding='utf-8', xml_declaration=True)


def create_definitions_element():
    """
    Creates the epml root element

    Returns
    -------
    root : ET XML element
        epml xml root element
    """

    root = eTree.Element("epml:epml")
    root.set("xmlns:epml", "http://www.epml.de")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:schemaLocation", "epml_1_draft.xsd")
    return root

