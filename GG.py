import os
import psycopg2
import urllib.parse as urlparse


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse("postgres://xxaytwrfomnnml:9c4c70dd8f25b43cb187d34d01f6fa6f0885a0cb705d9d64ad88dcc21df1d630@ec2-54-247-189-141.eu-west-1.compute.amazonaws.com:5432/d3cnnian2qaq96")


class GGManager:

    def __init__(self):
        global url
        self.ggs_data = {}
        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM users;")
        query = self.cur.fetchall()
        for row in query:
            _id, ggs, username = row
            self.ggs_data[str(_id)] = {'name': str(username), 'ggs': int(ggs)}

    def save(self):
        self.conn.commit()

    def add_user(self, _id, name):
        _id = str(_id)
        if _id in self.ggs_data:
            return
        self.ggs_data[_id] = {'name': name, 'ggs': 10}
        self.cur.execute("INSERT INTO users (id, ggs, username) VALUES (%s, %s, %s)", (_id, 10, name))
        self.save()

    def get_user(self, _id):
        _id = str(_id)
        return self.ggs_data[_id]

    def get_ggs(self, _id):
        _id = str(_id)
        return self.ggs_data[_id]['ggs']

    def add(self, _id, n):
        _id = str(_id)
        n = abs(n)
        self.ggs_data[_id]['ggs'] += n
        ggs = self.get_ggs(_id)
        self.cur.execute("UPDATE users SET ggs=%s WHERE id=%s", (ggs, _id))
        self.save()

    def sub(self, _id, n):
        _id = str(_id)
        n = abs(n)
        self.ggs_data[_id]['ggs'] -= n
        ggs = self.get_ggs(_id)
        self.cur.execute("UPDATE users SET ggs=%s WHERE id=%s", (ggs, _id))
        self.save()

    def set(self, _id, n):
        _id = str(_id)
        self.ggs_data[_id]['ggs'] = n
        self.cur.execute("UPDATE users SET ggs=%s WHERE id=%s", (n, _id))
        self.save()

    def entry_exists(self, _id):
        _id = str(_id)
        return self.ggs_data.get(_id, False)

    def close(self):
        self.cur.close()
        self.conn.close()


gg_manager = GGManager()
