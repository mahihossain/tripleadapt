from xml.etree.ElementTree import fromstring, ElementTree
import Backend.clevr.CLEVR as rest
import base64
import pandas as pd
import os


def dictlist(node):
    res = {}
    res[node.tag] = []
    xmltodict(node, res[node.tag])
    reply = {}
    reply[node.tag] = {'value': res[node.tag]}
    return reply


def xmltodict(node, res):
    rep = {}

    if len(node):
        # n = 0
        for n in list(node):
            rep[node.tag] = []
            xmltodict(n, rep[node.tag])
            if len(n):
                res.append({n.tag: rep[node.tag]})
            else:
                res.append(rep[node.tag][0])
    else:
        res.append({node.tag: node.text})
    return


def decode_b64(inp, decoding=""):
    if decoding != "":
        return base64.b64decode(inp).decode(decoding)
    else:
        return base64.b64decode(inp)


def save_model(path, bpmn_xml):
    file = open(path, 'w')
    file.write(bpmn_xml)
    file.close()


class process_data(object):

    data = pd.DataFrame(columns=['Date', 'UUID', 'CreationDate','HasContents', 'Size', 'Contents'])

    """
    class to receive data from the CLEVR interface. Load, structure and safe the data. This class needs
    to be used when regularly receive CLEVR data, set up the session and the user.
    UUID can be None, but time needs to be set beforehand (login of the user at CLEVR interface)
    """
    def __init__(self, uuid, time, db):
        self.uuid = uuid
        self.last_update_time = time
        self.collection = db['clevr']
        self.content = dict()
        self.bpmn_xml = ""
        self.data = pd.DataFrame()
        # if uuid is None, start a new Session and set the uuid to the newest entry (if there is one)
        if uuid is None:
            self.receive_data(self.last_update_time)
            if len(self.data):
                # if there is no data, no set up possible. that means set up again in regular time periods
                self.uuid = self.data['UUID'][len(self.data['UUID'])-1]
        self.update()


    def __init__(self, db, data):
        self.collection = db['clevr']
        self.content = dict()
        self.bpmn_xml = ""
        self.data = pd.DataFrame()
        self.data = data
        self.uuid = data['UUID']
        self.update()


    def create_dict(self, id, root):
        self.content['StartDate'] = root.find("Session/StartDate").text
        self.content['UUID'] = id
        if root.find("Session/AnonymousUser/Identifier") is not None:
            self.content["user"] = root.find("Session/AnonymousUser/Identifier").text
        else:
            self.content['user'] = "unknown"
        self.content = dictlist(root)

    def get_user(self):
        if 'user' in self.content:
            return self.content['user']
        else:
            return None

    def receive_data(self, timestamp):
        json = rest.get_data_since_date(timestamp)
        if 'error' in json:
            print(json['error'])
            return None
        for json_obj in json:
            det = self.get_data_rest(json_obj["UUID"])
            self.data = self.data.append(det, ignore_index=True)
        return self.data

    def get_data_rest(self, uuid):
        return rest.get_data_uuid(uuid)

    def update(self):
        if self.uuid is not None:
            # get contents of the specific uuid
            entry = self.get_data_rest(self.uuid)["Contents"]
            # overwrite the contents of the dictionary
            self.parse_content(entry, self.uuid)
        else:
            print("There is no data available...")

    def save_data_db(self, data, uuid):
        query = {"UUID": uuid}
        self.collection.replace_one(query, data, upsert=True)

    def save_data_csv(self):
        filename = "data/"+self.uuid+".csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.data.to_csv("data/"+self.uuid+".csv")

    def save_model(self):
        filename = "data/"+self.uuid+".bpmn"
        file = open(filename, 'w+')
        file.write(self.bpmn_xml)

    """
    This is horrible... and Historys and Activitys are not named by us!
    """
    def get_activities(self):
        return self.content['Sessions']['value'][0]['Session'][3]['Historys'][0]['History'][0]['Activitys']

    def parse_content(self, content, id):
        tree = ElementTree(fromstring(decode_b64(content)))
        # arse json format to pandas DataFrame
        root = tree.getroot()
        # remove Images because of size
        #self.bpmn_xml = root.find('Session/Revision/BPMN').text
        #for parent in root.findall('Session/Revision/BPMNObjects/BPMNObject/Images/Image/Contents'):
        #    parent.text = ""
        self.create_dict(id, root)
