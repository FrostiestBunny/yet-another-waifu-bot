import time


class People:

    def __init__(self):
        self.pimps = {}
        self.workers = {}

    def add_worker(self, ide, username):
        person = Person(ide, username)
        self.workers[person.ide] = person

    def add_pimp(self, ide, username):
        person = Person(ide, username, True)
        self.pimps[person.ide] = person

    def get_worker(self, ide):
        ide = str(ide)
        return self.workers.get(ide, None)

    def remove_worker(self, ide):
        ide = str(ide)
        del self.workers[ide]

    def get_pimp(self, ide):
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
