"""
Exports BPMNs as .bpmn file
"""
import xml.etree.cElementTree as eTree
from rmm4py.models.exporter.indent import indent

_COLLABORATION = "bpmn:collaboration"
_PARTICIPANT = "bpmn:participant"
_MESSAGE_FLOW = "bpmn:messageFlow"
_PROCESS = "bpmn:process"
_INCOMING = "bpmn:incoming"
_OUTGOING = "bpmn:outgoing"
_SEQUENCE_FLOW = "bpmn:sequenceFlow"
_CHILD_LANE_SET = "bpmn:childLaneSet"
_LANE_SET = "bpmn:laneSet"
_LANE = "bpmn:lane"
_FLOW_NODE_REF = "bpmn:flowNodeRef"

_DI_SHAPE = "bpmndi:BPMNShape"
_DI_DIAGRAM = "bpmndi:BPMNDiagram"
_DI_PLANE = "bpmndi:BPMNPlane"
_DI_EDGE = "bpmndi:BPMNEdge"
_DI_BOUNDS = "dc:Bounds"
_DI_WAYPOINT = "di:waypoint"


def export_lanes(element, lanes, bpmn):
    """
    Export the lane structure of a process

    Parameters
    ----------
    element: ET XML element
        current xml element
    lanes : list
        list of all lanes in thies layer
    bpmn : collaboration model
        bpmn to export
    """

    for lane in lanes:

        is_set = lane['isSet']

        if is_set:

            if 'parent' in lane:
                child_lane_set_element = eTree.SubElement(element, _CHILD_LANE_SET)
                child_lane_set_id = lane['id']

                child_lane_set_element.set("id", child_lane_set_id)

                child_lanes = []

                for child_id in lane['children']:
                    child_lanes.append(bpmn.lanes[child_id])

                export_lanes(child_lane_set_element, child_lanes, bpmn)

            else:
                lane_set_element = eTree.SubElement(element, _LANE_SET)

                lane_set_id = lane['id']

                lane_set_element.set("id", lane_set_id)

                child_lanes = []

                for child_id in lane['children']:
                    child_lanes.append(bpmn.lanes[child_id])

                export_lanes(lane_set_element, child_lanes, bpmn)

        else:
            lane_element = eTree.SubElement(element, _LANE)

            lane_id = lane['id']
            lane_name = lane['name']

            lane_element.set("id", lane_id)
            lane_element.set("name", lane_name)

            for flow_node_ref in lane['flowNodeRefs']:
                flow_node_ref_element = eTree.SubElement(lane_element, _FLOW_NODE_REF)
                flow_node_ref_element.text = flow_node_ref

            if 'children' in lane:
                child_lanes = []

                for child_id in lane['children']:
                    child_lanes.append(bpmn.lanes[child_id])

                export_lanes(lane_element, child_lanes, bpmn)


def export(bpmn, file):
    """
    Exports a collaboration model as a .bpmn file

    Parameters
    ----------
    bpmn : collaboration_model
        given collaboration model

    file : string
        path to an .bpmn file to export the collaboration model into
    """

    root = create_definitions_element()
    graph = bpmn.process_graph

    if bpmn.collaboration_id != "":
        colaboration_element = eTree.SubElement(root, _COLLABORATION)
        colaboration_element.set('id', bpmn.collaboration_id)

        for key in bpmn.pools:
            pool = bpmn.pools[key]
            participant_element = eTree.SubElement(colaboration_element, _PARTICIPANT)

            participant_element.set("id", pool['id'])
            participant_element.set("name", pool['name'])
            participant_element.set("processRef", pool['processRef'])

        for key in bpmn.message_flows:
            mf = bpmn.message_flows[key]
            mf_element = eTree.SubElement(colaboration_element, _MESSAGE_FLOW)

            for mf_key in mf:
                mf_element.set(mf_key, mf[mf_key])

    for process_id in bpmn.processes.keys():
        process_dict = bpmn.processes[process_id]

        pool_dict = bpmn.pools[process_dict['pool']]
        pool_id = pool_dict['id']

        process_element = eTree.SubElement(root, _PROCESS)

        process_element.set("id", process_dict['id'])
        process_element.set("isExecutable", "false")
        process_edges = []

        process_lanes = []

        for key in bpmn.lanes:
            lane = bpmn.lanes[key]

            if 'pool' in lane and pool_id == lane['pool']:
                process_lanes.append(lane)

        export_lanes(process_element, process_lanes, bpmn)

        for node in graph.nodes(data=True):
            if graph.nodes[node[0]]['process'] != process_id:
                continue

            node_type = node[1]['type']
            node_element = eTree.SubElement(process_element, "bpmn:"+node_type)

            node_element.set("id", node[1]['id'])

            if 'name' in node[1].keys():
                node_element.set("name", node[1]['name'])

            for incoming in list(graph.predecessors(node[0])):
                in_edge = graph.get_edge_data(incoming, node[0])
                edge_id = in_edge['id']

                if edge_id not in bpmn.message_flows.keys():
                    process_edges.append(edge_id)
                    in_edge_element = eTree.SubElement(node_element, _INCOMING)
                    in_edge_element.text = edge_id

            for outgoing in list(graph.successors(node[0])):
                out_edge = graph.get_edge_data(node[0], outgoing)
                edge_id = out_edge['id']

                if edge_id not in bpmn.message_flows.keys():
                    process_edges.append(edge_id)
                    out_edge_element = eTree.SubElement(node_element, _OUTGOING)
                    out_edge_element.text = edge_id

        for edge in graph.edges(data=True):

            edge_id = edge[2]['id']

            if edge_id in process_edges:
                edge_element = eTree.SubElement(process_element, _SEQUENCE_FLOW)
                edge_element.set("id", edge_id)
                edge_element.set("sourceRef", edge[0])
                edge_element.set("targetRef", edge[1])

    diagram = eTree.SubElement(root, _DI_DIAGRAM)
    diagram.set("id", "BPMNDiagram_1")

    plane = eTree.SubElement(diagram, _DI_PLANE)
    plane.set("id", "BPMNPlane_1")
    plane.set("bpmnElement", bpmn.collaboration_id)

    for key in bpmn.pools.keys():

        pool = bpmn.pools[key]
        pool_gui_element = eTree.SubElement(plane, _DI_SHAPE)
        pool_gui_element.set("id", pool['id'] + "_gui")
        pool_gui_element.set("bpmnElement", pool['id'])
        pool_gui_element.set("isHorizontal", "true")

        bounds = eTree.SubElement(pool_gui_element, _DI_BOUNDS)

        bounds.set("x", "0")
        bounds.set("y", "0")
        bounds.set("width", "100")
        bounds.set("height", "100")

    for key in bpmn.lanes.keys():

        lane = bpmn.lanes[key]

        if not lane['isSet']:
            lane_gui_element = eTree.SubElement(plane, _DI_SHAPE)
            lane_gui_element.set("id", lane['id'] + "_gui")
            lane_gui_element.set("bpmnElement", lane['id'])
            lane_gui_element.set("isHorizontal", "true")

            bounds = eTree.SubElement(lane_gui_element, _DI_BOUNDS)

            bounds.set("x", "0")
            bounds.set("y", "0")
            bounds.set("width", "100")
            bounds.set("height", "100")

    for node in graph.nodes(data=True):
        node_gui_element = eTree.SubElement(plane, _DI_SHAPE)
        node_gui_element.set("id", node[0] + "_gui")
        node_gui_element.set("bpmnElement", node[0])

        bounds = eTree.SubElement(node_gui_element, _DI_BOUNDS)
        bounds.set("width", node[1]['width'])
        bounds.set("height", node[1]['height'])
        bounds.set("x", node[1]['x'])
        bounds.set("y", node[1]['y'])

    for edge in graph.edges(data=True):
        edge_gui_element = eTree.SubElement(plane, _DI_EDGE)
        edge_gui_element.set("id", edge[2]['id'] + "_gui")
        edge_gui_element.set("bpmnElement", edge[2]['id'])

        for waypoint in edge[2]['waypoints']:
            waypoint_element = eTree.SubElement(edge_gui_element, _DI_WAYPOINT)
            waypoint_element.set('x', waypoint[0])
            waypoint_element.set('y', waypoint[1])

    indent(root)
    tree = eTree.ElementTree(root)
    tree.write(file, encoding='utf-8', xml_declaration=True)


def create_definitions_element():
    """
    Creates the bpmn xml root element

    Returns
    -------
    root : ET XML element
        bpmn xml root element
    """

    root = eTree.Element("bpmn:definitions")
    root.set("xmlns:bpmn", "http://www.omg.org/spec/BPMN/20100524/MODEL")
    root.set("xmlns:bpmndi", "http://www.omg.org/spec/BPMN/20100524/DI")
    root.set("xmlns:dc", "http://www.omg.org/spec/DD/20100524/DC")
    root.set("xmlns:di", "http://www.omg.org/spec/DD/20100524/DI")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("targetNamespace", "http://www.signavio.com/bpmn20")
    root.set("typeLanguage", "http://www.w3.org/2001/XMLSchema")
    root.set("expressionLanguage", "http://www.w3.org/1999/XPath")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")

    return root
