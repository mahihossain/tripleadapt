"""
Imports .json files or json string representation
"""
import uuid
import json
from ....rmm4py.models.graph_representation.collaboration_model import CollaborationModel


def load_diagram_from_json(filepath_or_jsonstring, randomize_ids=False):
    """
        Loads a json file and returns a collaboration model
        Parameters
        ----------
        filepath_or_jsonstring : str
            filepath to .json file or json string representation
        randomize_ids : bool, optional
            if set true, randomizes all id's used in the epmls

        Returns
        -------
        list of collaboration models
            imported Json

        """

    def create_model_for_element(element):
        """
                Parses an element of the json data
                ----------
                element
                    an element of the json data

                Returns
                -------
                collaboration model
                    the parsed model

        """

        def check_not_none(model, name, position, size, angle, z, body, root=None):
            """
                Checks if arguments are none
                ----------
                model
                   Collaboration model
                name
                    name attribute
                position
                    position attribute
                size
                    size attribute
                angle
                    angle attribute
                z
                    z attribute
                body
                    body attribute
                root
                    root attribute

            """
            if name is not None:
                model.process_graph.add_node(id_, name=name)
            if position is not None:
                model.process_graph.add_node(id_, position=position)
            if size is not None:
                model.process_graph.add_node(id_, size=size)
            if angle is not None:
                model.process_graph.add_node(id_, angle=angle)
            if z is not None:
                model.process_graph.add_node(id_, z=z)
            if body is not None:
                model.process_graph.add_node(id_, body=body)
            if root is not None:
                model.process_graph.add_node(id_, root=root)

        model = CollaborationModel()

        for info in element['cells']:
            if randomize_ids:
                id_ = str(uuid.uuid1())
            else:
                id_ = info['id']
            type_ = ''

            if info['type'] == "standard.Path":
                name = None
                z = None
                body = None
                root = None
                position = None
                angle = None
                size = None

                if info['attrs'] is not None:
                    attrs = info['attrs']
                    if attrs['body'] is not None:
                        body = attrs['body']
                    if attrs['root'] is not None:
                        root = attrs['root']
                    if attrs['label'] is not None:
                        label = attrs['label']
                        name = label['text']

                if 'start' in name.lower():
                    type_ = 'startEvent'
                elif 'end' in name.lower():
                    type_ = 'endEvent'
                elif 'intermediateCatch' in name.lower():
                    type_ = "intermediateCatchEvent"
                elif 'intermediateThrow' in name.lower():
                    type_ = "intermediateThrowEvent"
                elif 'boundary' in name.lower():
                    type_ = "boundaryEvent"
                else:
                    type_ = 'event'

                if info['z'] is not None:
                    z = info['z']
                if info['position'] is not None:
                    position = info['position']
                if info['size'] is not None:
                    size = info['size']
                if info['angle'] is not None:
                    angle = info['angle']

                check_not_none(model, name, position, size, angle, z, body, root)
                model.process_graph.add_node(id_, type=type_)
            if info['type'] == "standard.Rectangle":
                type_ = 'task'
                z = None
                name = None
                body = None
                position = None
                angle = None
                size = None
                if info['position']:
                    position = info['position']
                if info['size']:
                    size = info['size']
                if info['z'] != None:
                    z = info['z']
                if info['angle']:
                    angle = info['angle']
                if info['attrs']:
                    attrs = info['attrs']
                    if attrs['body']:
                        body = attrs['body']
                    if attrs['label']:
                        label = attrs['label']
                        name = label['text']

                check_not_none(model, name, position, size, angle, z, body)
                model.process_graph.add_node(id_, type=type_)

            if info['type'] == "standard.Circle":
                name = None
                z = None
                body = None
                root = None
                position = None
                angle = None
                size = None

                if info['attrs'] is not None:
                    attrs = info['attrs']
                    if attrs['body'] is not None:
                        body = attrs['body']
                    if attrs['root'] is not None:
                        root = attrs['root']
                    if attrs['label'] is not None:
                        label = attrs['label']
                        name = label['text']
                if info['position'] is not None:
                    position = info['position']
                if info['size'] is not None:
                    size = info['size']
                if info['angle'] is not None:
                    angle = info['angle']
                if info['z'] is not None:
                    z = info['z']

                if 'or' in name.lower():
                    type_ = "inclusiveGateway"
                if 'xor' in name.lower():
                    type_ = "exclusiveGateway"
                if 'and' in name.lower():
                    type_ = "parallelGateway"
                if 'eventbased' in name.lower():
                    type_ = "eventBasedGateway"
                if 'complex' in name.lower():
                    type_ = "complexGateway"
                model.process_graph.add_node(id_, id=id_)
                model.process_graph.add_node(id_, type=type_)
                check_not_none(model, name, position, size, angle, z, body, root)
                model.process_graph.add_node(id_, type=type_)

            if info['type'] == "standard.Link":
                z = None
                if info['z'] is not None:
                    z = info['z']
                attrs = info['attrs']
                src = info['source']
                src_id = src['id']
                target = info['target']
                target_id = target['id']
                if attrs:
                    if z is not None:
                        model.process_graph.add_edge(src_id, target_id, id=id_, z=z, attrs=attrs)
                    else:
                        model.process_graph.add_edge(src_id, target_id, id=id_, attrs=attrs)
                else:
                    if z is not None:
                        model.process_graph.add_edge(src_id, target_id, id=id_, z=z)
                    else:
                        model.process_graph.add_edge(src_id, target_id, id=id_)
        return model

    models = []
    if filepath_or_jsonstring.endswith(".json"):
        f = open(filepath_or_jsonstring, "r")

        data = json.loads(f.read())
    else:
        data = json.loads(filepath_or_jsonstring)

    if isinstance(data, list):
        for element in data:
            model = create_model_for_element(element)
            models.append(model)
    else:
        model = create_model_for_element(data)
        models.append(model)

    return models
