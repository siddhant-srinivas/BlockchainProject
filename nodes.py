from datetime import datetime

class Author:
    authors = []

    def __init__(self, username, password, id):
        self.username = username
        self._password = password
        self.id = id
        self.authors.append(self)
        self.save_authors_data()

    @classmethod
    def save_authors_data(cls):
        with open('authors.data', 'w') as file:
            for author in cls.authors:
                file.write(f"{author.username},{author._password},{author.id},{datetime.now()}\n")

    @classmethod
    def check_username_exists(cls, id):
        existing_users = []
        try:
            with open('authors.data', 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    existing_users.append((user_data[0], user_data[1], user_data[2]))
        except FileNotFoundError:
            return False

        for user in existing_users:
            if int(user[1]) == id:
                return True
        return False

class Customer:
    customers = []

    def __init__(self, username, password, id):
        self.username = username
        self._password = password
        self.id = id
        self.customers.append(self)
        self.save_customers_data()

    @classmethod
    def save_customers_data(cls):
        with open('customers.data', 'w') as file:
            for customer in cls.customers:
                file.write(f"{customer.username},{customer._password},{customer.id},{datetime.now()}\n")

    @classmethod
    def check_username_exists(cls, id):
        existing_users = []
        try:
            with open('customers.data', 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    existing_users.append((user_data[0], user_data[1], user_data[2]))
        except FileNotFoundError:
            return False

        for user in existing_users:
            if int(user[1]) == id:
                return True
        return False
