"""
Exports Collaboration Models as .pnml file
"""
import xml.etree.cElementTree as eTree
from rmm4py.models.graph_representation.node_types import Event, Task
from rmm4py.models.exporter.indent import indent


def export_pnml(pnml2, file):
    """
    Exports a collaboration model as a .pnml file

    Parameters
    ----------
    pnml : collaboration_model or list of collaboration_models
        given collaboration model

    file : string
        path to an .pnml file to export the collaboration model into

    Returns
    -------
    pnml file
    """

    root = create_definitions_element()
    collaboration_models = pnml2

    for i in range(len(collaboration_models)):

        pnml = collaboration_models[i]

        petrinet = eTree.SubElement(root, "net")
        petrinet.set("id", pnml.processes[next(iter(pnml.processes))]['id'])

        page = eTree.SubElement(petrinet, "page")
        page.set("id", "0")

        graph = pnml.process_graph

        for node in graph.nodes:

            node_type = graph.nodes[node]['type']

            if node_type in Event.__members__ :
                event = eTree.SubElement(page, "place", {"id": graph.nodes[node]['id']})
                name = eTree.SubElement(event, "name", attrib={}, )
                text = eTree.SubElement(name, "text", attrib={}, )
                if 'initialMarking' in graph.nodes[node]:
                    initial_marking = eTree.SubElement(event, "initialMarking", attrib={}, )
                    text2 = eTree.SubElement(initial_marking, "text", attrib={}, )
                    text2.text = graph.nodes[node]['initialMarking']

            elif node_type in Task.__members__ :
                function = eTree.SubElement(page, "transition", {"id": graph.nodes[node]['id']})
                name = eTree.SubElement(function, "name", attrib={}, )
                text = eTree.SubElement(name, "text", attrib={}, )

            else:
                raise ValueError

            if 'name' in graph.nodes[node]:
                text.text = graph.nodes[node]['name']

        for edge in graph.edges:

            arc = eTree.SubElement(page, "arc", {"id": graph.edges[edge]['id'], "source":edge[0],"target":edge[1]})

    indent(root)
    tree = eTree.ElementTree(root)
    tree.write(file, encoding='utf-8', xml_declaration=True)


def create_definitions_element():
    """
    Creates the pnml root element

    Returns
    -------
    root : ET XML element
        pnml xml root element
    """

    root = eTree.Element("pnml")

    return root
