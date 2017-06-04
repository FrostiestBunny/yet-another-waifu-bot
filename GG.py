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
        if str(_id) in self.ggs_data:
            return
        self.ggs_data[str(_id)] = {'name': name, 'ggs': 10}
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

    def set(self, _id, n):
        self.ggs_data[str(_id)]['ggs'] = n
        self.save()

    def entry_exists(self, _id):
        return self.ggs_data.get(_id, default=False)


gg_manager = GGManager()
