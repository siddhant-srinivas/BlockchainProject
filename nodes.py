from datetime import datetime

class Author:
    authors = []

    def __init__(self, username, password, id):
        self.username = username
        self._password = password
        self.id = id
        self.authors.append(self)

class Customer:
    customers = []

    def __init__(self, username, password, id):
        self.id = id
        self.username = username
        self._password = password
        self.customers.append(self)


