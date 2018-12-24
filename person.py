import time
import psycopg2


class People:

    def __init__(self):
        self.pimps = {}
        self.workers = {}
        self.conn = None
        self.cur = None

    def connect(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM pimps;")
        query = self.cur.fetchall()
        for row in query:
            _id, username = row
            self.pimps[str(_id)] = Person(str(_id), str(username), True)

        self.cur.execute("SELECT * FROM pros;")
        query = self.cur.fetchall()
        for row in query:
            _id, username, pimp_id, pimp_name = row
            self.workers[str(_id)] = Person(str(_id), str(username))
            if pimp_id != "0":
                pimp = self.pimps[str(pimp_id)]
                self.workers[str(_id)].add_pimp(pimp)

    def save(self):
        self.conn.commit()

    def add_worker(self, ide, username):
        if self.conn is None:
            print("No connection.")
            return
        person = Person(ide, username)
        self.workers[person.ide] = person
        self.cur.execute("INSERT INTO pros (id, name, pimp_id, pimp_name) VALUES (%s, %s, %s, %s)",
                         (ide, username, "0", "0"))
        self.save()

    def add_pimp(self, ide, username):
        if self.conn is None:
            print("No connection.")
            return
        person = Person(ide, username, True)
        self.pimps[person.ide] = person
        self.cur.execute("INSERT INTO pimps (id, name) VALUES (%s, %s)",
                         (ide, username))
        self.save()

    def add_pimp_to_worker(self, ide, pimp):
        self.workers[str(ide)].add_pimp(pimp)
        self.cur.execute("UPDATE pros SET pimp_id=%s, pimp_name=%s WHERE id=%s",
                         (pimp.ide, pimp.username, ide))
        self.save()

    def get_worker(self, ide):
        if self.conn is None:
            print("No connection.")
            return
        ide = str(ide)
        return self.workers.get(ide, None)

    def remove_worker(self, ide):
        if self.conn is None:
            print("No connection.")
            return
        ide = str(ide)
        del self.workers[ide]

    def get_pimp(self, ide):
        if self.conn is None:
            print("No connection.")
            return
        ide = str(ide)
        return self.pimps.get(ide, None)


class Person:

    def __init__(self, ide, username, is_pimp=False):
        self.ide = str(ide)
        self.username = username
        self.time_last_action = None
        self.is_pimp = is_pimp
        self.pimp = None

    def has_pimp(self):
        return self.pimp is not None

    def add_pimp(self, pimp):
        self.pimp = pimp

    def get_pimp(self):
        return self.pimp

    def set_time(self):
        self.time_last_action = time.time()

    def check_time(self, delta):
        if self.time_last_action is None:
            return True
        return time.time() - self.time_last_action > delta

    def time_left(self, delta):
        return self.time_last_action + delta - time.time()


people = People()
