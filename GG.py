import json


class GGManager:

    def __init__(self):
        self.db_file = 'db/ggs.json'
        with open(self.db_file, mode='r', encoding='utf-8') as f:
            self.ggs_data = json.load(f)

    def save(self):
        with open(self.db_file, mode='w', encoding='utf-8') as f:
            json.dump(self.ggs_data, f)

    def add_user(self, _id, name):
        self.ggs_data[str(_id)] = {'name': name, 'ggs': 0}
        self.save()

    def get_ggs(self, _id):
        return self.ggs_data[str(_id)]['ggs']

    def add(self, _id, n):
        n = abs(n)
        self.ggs_data[str(_id)]['ggs'] += n
        self.save()

    def sub(self, _id, n):
        n = abs(n)
        self.ggs_data[str(_id)]['ggs'] -= n
        self.save()


gg_manager = GGManager()
