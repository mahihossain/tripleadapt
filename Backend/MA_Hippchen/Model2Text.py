import os
import json
import nltk
from HanTa import HanoverTagger as ht
from pattern.text.de import conjugate
from german_nouns.lookup import Nouns

import codecs
from random import seed
from random import randint


class Model2Text:
    """
    Model2Text Klasse erstellen
    """

    def __init__(self):
        self.nouns = Nouns()
        self.m = 0
        self.model_name = ''
        self.connector_list = []
        self.current_path = 0
        self.last_path = 0
        self.last_person = ''
        self.last_satzanfang = ''
        self.pre_last_satzanfang = ''
        self.previous_position = ''
        self.current_position = ''
        self.noun_group = []
        self.verb_group = []

    # nltk.download('omw-1.4')
    try:
        print(conjugate("bin", "1sg"))
    except:
        pass

    def InfoExt(self, data):
        """Informationen aus Modell ziehen"""
        print("Extraction")
        print(data)
        tagger = ht.HanoverTagger('morphmodel_ger.pgz')
        Nodes = {}
        for i in data['nodes']:
            node = {'id': i['id'], 'action': i['label'], 'group': i['group'], 'edgesTo': [], 'edgesFrom': [], 'tagging': [],
                    'unit': i.get('organizational_unit')}
            for e in data['edges']:
                if e['from'] == i['id']:
                    node['edgesTo'].append(e['to'])
                if e['to'] == i['id']:
                    node['edgesFrom'].append(e['from'])
            Nodes[i['id']] = node
        print(Nodes)

        for k in Nodes:
            tokenized_sent = nltk.tokenize.word_tokenize(
                Nodes[k]['action'], language='german')
            tags = tagger.tag_sent(tokenized_sent)
            Nodes[k]['tagging'] = tags

        return Nodes

    def data2tree(self, Nodes):
        tree = {'structure': []}
        for i in Nodes:
            if Nodes[i]['edgesFrom'] == []:
                tree['start'] = i
            if Nodes[i]['edgesTo'] == []:
                tree['end'] = i
        hlptree = [self.buildtree(tree['start'], Nodes)]
        tree['structure'].append(hlptree)
        while len(tree['structure']) == 1:
            tree['structure'] = tree['structure'][0]
        return tree

    def buildtree(self, root, Nodes):
        global connector_list
        hlp = []
        hlp.append(root)
        if len(Nodes[root]['edgesTo']) == 0:
            return hlp
        next = Nodes[root]['edgesTo'][0]
        while Nodes[next]['group'] != 'connector' and len(Nodes[next]['edgesTo']) > 0:
            hlp.append(next)
            next = Nodes[next]['edgesTo'][0]
        if len(Nodes[next]['edgesTo']) == 0:
            hlp.append(next)
        if Nodes[next]['group'] == 'connector' and len(Nodes[next]['edgesTo']) > 1:
            self.connector_list.append(Nodes[next]['action'])

        if len(Nodes[next]['edgesTo']) > 1:
            innerlist = []
            for x in Nodes[next]['edgesTo']:
                innerlist.append(self.buildtree(x, Nodes))
            hlp.append(innerlist)
            lastconnector = Nodes[innerlist[len(
                innerlist) - 1][-1]]['edgesTo'][0]
            hlp.extend(self.buildtree(
                Nodes[lastconnector]['edgesTo'][0], Nodes))
        return hlp

    def tree2sen(self, Tree, Nodes):
        global current_path
        global last_path
        global previous_position
        global current_position
        msg = []
        for i in Tree['structure']:
            if isinstance(i, str):
                msg.append(i)
            else:
                msg = self.buildSenStruc(i, msg)
        print(msg)
        tab = 0
        # f = codecs.open('Test.txt', 'w', "utf-8")
        f = codecs.open(
            '../../../Frontend/demo/src/Model2Text/model2text.txt', 'w', "utf-8")

        self.current_position = self.previous_position = f.tell()
        for x in msg:
            if x in Nodes:
                self.previous_position = self.current_position
                self.current_position = f.tell()
                for i in range(tab):
                    f.write('\t')
                if tab > 0:
                    f.write('- ')
                if x == msg[0]:
                    self.writeStart(Nodes[x], f)
                else:
                    if msg[len(msg) - 1] == x:
                        self.writeEnd(Nodes[x], f)
                    else:
                        self.writeSen(Nodes[x], f, self.current_path, tab)
                f.write('\n')
            else:
                if x[:2] == 'OR' or x[:3] == 'AND' or x[:3] == 'XOR':
                    if x[len(x) - 1] == '1':
                        self.previous_position = self.current_position
                        self.current_position = f.tell()
                        if tab >= 1:
                            f.write('\t')
                        self.writeConnector(x, f)
                        self.last_path = self.current_path
                        self.current_path = 1
                        tab = tab + 1
                    else:
                        self.current_path = int(x[len(x) - 1])
                else:
                    tab = tab - 1
                    self.current_path = self.last_path
        f.close()

    def buildSenStruc(self, i, msg):
        global m, connector_list
        n = 1
        m = self.m + 1
        for e in i:
            if isinstance(e, list):
                msg.append(
                    self.connector_list[self.m - 1] + '.' + str(self.m) + '.' + str(n))
                n = n + 1
            if len(e) == 1 or isinstance(e, str):
                while isinstance(e, list):
                    e = e[0]
                msg.append(e)
            else:
                if isinstance(e[0], list):
                    m = m - 1
                    msg.pop()
                msg = self.buildSenStruc(e, msg)
        msg.append('end')
        return msg

    def writeConnector(self, con, file):
        if con[:2] == 'OR':
            file.write(
                'Von den folgenden Pfaden werden einzelne oder mehrere durchgeführt: \n')
        if con[:3] == 'XOR':
            file.write('Von den folgenden Pfaden wird nur einer ausgeführt: \n')
        if con[:3] == 'AND':
            file.write(
                'Von den folgenden Pfaden werden alle gleichzeitig durchgeführt: \n')

    def writeSen(self, Node, file, path, tab):
        global last_person
        global current_position
        global previous_position
        global noun_group
        global verb_group
        global last_satzanfang
        global pre_last_satzanfang
        artikel = ' '
        nomen = ''
        verb = ''
        person = Node['unit'][0]
        satzanfang = self.getSatzanfang()

        for t in Node['tagging']:
            if t[2][0:1] == 'N' or t[2] == 'KON':
                if nomen == '':
                    nomen = t[0]
                    artikel = self.getArtikel(nomen)
                else:
                    nomen = nomen + ' ' + t[0]
            if t[2][0:2] == 'VV' or t[2] == 'ADJD':
                verb = t[1]

        if person == self.last_person and self.last_person != '':
            self.noun_group.append(nomen)
            self.verb_group.append(verb)
            file.truncate(file.truncate(self.previous_position))
            self.last_satzanfang = self.pre_last_satzanfang
            self.current_position = self.previous_position
            file.seek(self.previous_position)
            for i in range(tab):
                file.write('\t')
            if tab > 0:
                file.write('- ')

            sen_group = f'{satzanfang} wird von {person}'

            if len(self.noun_group) == 2 and self.verb_group[0] == self.verb_group[1]:
                file.write(
                    f'{satzanfang} wird von {person} {self.getArtikel(self.noun_group[0])}{self.noun_group[0]} und {self.getArtikel(self.noun_group[1])}{self.noun_group[1]} {conjugate(self.verb_group[0], "ppart")}.')
            else:
                for n, v in enumerate(self.noun_group):
                    if n == 0:
                        sen_group = sen_group + \
                            f' {self.getArtikel(self.noun_group[n])}{self.noun_group[n]} {conjugate(self.verb_group[n], "ppart")}'
                    elif n == len(self.noun_group)-1:
                        sen_group = sen_group + \
                            f' und {self.getArtikel(self.noun_group[n])}{self.noun_group[n]} {conjugate(self.verb_group[n], "ppart")}.'
                    else:
                        sen_group = sen_group + \
                            f', {self.getArtikel(self.noun_group[n])}{self.noun_group[n]} {conjugate(self.verb_group[n], "ppart")}'
                file.write(sen_group)

            return True
        else:
            self.noun_group = [nomen]
            self.verb_group = [verb]

        self.last_person = person

        sen_person = [f'Zunächst wird {artikel}{nomen} von {person} {conjugate(verb, "ppart")}.',
                      f'{satzanfang} wird {artikel}{nomen} von {person} {conjugate(verb, "ppart")}.', ]
        sen_no_person = [f'Zunächst wird {artikel}{nomen} {conjugate(verb, "ppart")}.',
                         f'{satzanfang} wird {artikel}{nomen} {conjugate(verb, "ppart")}.']
        if path == 1:
            if person is None or person == '':
                print('0')
                file.write(sen_no_person[0])
            else:
                print('0')
                file.write(sen_person[0])
        else:
            self.last_satzanfang = 'Zunächst'
            if person is None or person == '':
                print('1')
                file.write(sen_no_person[1])
            else:
                print('1')
                file.write(sen_person[1])

    def getSatzanfang(self):
        global last_satzanfang
        global pre_last_satzanfang
        Satzanfang = ['Nun', 'Anschließend', 'Danach',
                      'An dieser Stelle', 'Als nächstes']
        value = randint(0, len(Satzanfang) - 1)
        while Satzanfang[value] == self.last_satzanfang:
            value = randint(0, len(Satzanfang) - 1)
        self.pre_last_satzanfang = self.last_satzanfang
        self.last_satzanfang = Satzanfang[value]
        return Satzanfang[value]

    def getArtikel(self, Nomen):
        genus = self.nouns[Nomen]

        if genus != []:
            genus = genus[0]['genus']

        if genus == 'n':
            return 'das '
        elif genus == 'm':
            return 'der '
        elif genus == 'f':
            return 'die '
        else:
            return ''

    def writeStart(self, Node, file):
        global model_name
        artikel = ' '
        nomen = ''
        verb = ''
        person = Node['unit']
        for t in Node['tagging']:
            if t[2][0:1] == 'N' or t[2] == 'KON':
                if nomen == '':
                    nomen = t[0]
                    artikel = self.getArtikel(nomen)
                else:
                    nomen = nomen + ' ' + t[0]
            if t[2][0:2] == 'VV' or t[2] == 'ADJD':
                verb = t[0]
        if person is None or person == ['']:
            startSen = f'Zu Beginn des Modells {self.model_name} wird {artikel}{nomen} {conjugate(verb, "ppart")}.'
        else:
            startSen = f'Zu Beginn des Modells {self.model_name} wird {artikel}{nomen} von {person[0]} {conjugate(verb, "ppart")}.'
        file.write(startSen)

    def writeEnd(self, Node, file):
        artikel = ' '
        nomen = ''
        verb = ''
        person = Node['unit']
        for t in Node['tagging']:
            if t[2][0:1] == 'N' or t[2] == 'KON':
                if nomen == '':
                    nomen = t[0]
                    artikel = self.getArtikel(nomen)
                else:
                    nomen = nomen + ' ' + t[0]
            if t[2][0:2] == 'VV' or t[2] == 'ADJD':
                verb = t[0]
        if person is None or person == ['']:
            endSen = f'Am Ende des Modells wird {artikel}{nomen} {conjugate(verb, "ppart")}.'
        else:
            endSen = f'Am Ende des Modells wird {artikel}{nomen} von {person[0]} {conjugate(verb, "ppart")}.'
        file.write(endSen)

    def improvesen():
        print("Satzstruktur verbessern und gemeinsame Sätze zusammenfassen")

    def data2text(self, model):
        print("Main")
        "Modelle importieren"

        # print(os.listdir())
        if os.listdir()[0] == '.flaskenv':
            os.chdir(os.path.join('..', 'MA_Hippchen', 'Data'))

        print('Modell: ', model)
        # path = os.path.join('Evaluation_Gebaeudeeinsturz.json')
        # path = os.path.join('Modell1.json')
        # path = os.path.join('Modell2.json')
        # path = os.path.join('Modell3.json')

        path = os.path.join(model)

        print('Vor open')
        f = open(path)
        print('Hallo')

        data = json.load(f)[0]

        f.close()
        global model_name
        self.model_name = data['model']
        Nodes = self.InfoExt(data)
        print("Nodes: ", Nodes)
        Tree = self.data2tree(Nodes)
        print("Tree: ", Tree)
        self.tree2sen(Tree, Nodes)
        print(self.connector_list)

        os.chdir(os.path.join('..', '..', 'server'))
        # print('danach: ', os.listdir())

        return('data2text')

        # import gmrde

        # w = gmrde.Woerterbuch()
        # frage = input("Stellen Sie eine Frage: ")
        # antwort = gmrde.umformen.frageZuAntwort(w, frage, case=False)
        # print(antwort)
