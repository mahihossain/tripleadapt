import json

from pymongo import MongoClient
import Backend.config as conf

def con_db(url, db):
    client = MongoClient(url)
    return client[db]

client = con_db(conf.url_db, conf.db)

class UserListConstructor:

    def __init__(self, db):

        self.db = db

    def UserList(self):

        coll = self.db['user']
        user = coll.find({})
        user_dict = {}
        user_NR = 0

        for person in user:
            print(person['name'])
            name = str(person['name'])
            id = (person['id'])
            difficultylist = person['tasks_levels']

            def solve(s, words):
                count = 0
                for i in range(len(words)):
                    for j in range(len(words[i])):
                        if words[i][j] not in s:
                            break
                    else:
                        count += 1
                return count
            Difficult = solve("DIFFICULT", difficultylist)
            Medium = solve("MEDIUM", difficultylist)
            Low = solve("LOW", difficultylist)
            print(Difficult, Medium, Low)
            difficulty = None
            if Difficult == Medium == Low:
                difficulty = "MEDIUM"
            elif max(Difficult, Medium, Low) == Difficult:
                difficulty = "DIFFICULT"
            elif max(Difficult, Medium, Low) == Medium:
                difficulty = "MEDIUM"
            elif max(Difficult, Medium, Low) == Low:
                difficulty = "LOW"
            user_dict[user_NR] = [id, name, difficulty]
            user_NR = user_NR + 1
            out = json.dumps(user_dict)
        return out