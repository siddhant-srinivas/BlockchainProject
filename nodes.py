from datetime import datetime

class Author:
    authors = []
    def __init__(self, username, password, id, secretkey):
        self.username = username
        self._password = password
        self.id = id
        self.secretkey = secretkey
        self.authors.append(self)
        self.save_authors_data()

    @classmethod
    def save_authors_data(cls):
        with open('authors.data', 'a') as file:
            for author in cls.authors:
                file.write(f"{author.username},{author._password},{author.id},{datetime.now()},{author.secretkey}\n")

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
            if int(user[2]) == id:
                return True
        return False
    
    @classmethod
    def retrieve_secretkey(cls, id):
        existing_users = []
        try:
            with open('authors.data', 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    existing_users.append((user_data[0], user_data[1], user_data[2], user_data[3], user_data[4]))
        except FileNotFoundError:
            return False

        for user in existing_users:
            if int(user[2]) == id:
                return user[4]
        print('No such user! ')
        return False

    @classmethod
    def check_length(cls):
        existing_users = []
        try:
            with open('authors.data', 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    existing_users.append((user_data[0], user_data[1], user_data[2]))
        except FileNotFoundError:
            return 0

        return len(existing_users)

class Customer:
    customers=[]

    def __init__(self, username, password, id, secretkey):
        self.username = username
        self._password = password
        self.id = id
        self.secretkey = secretkey
        self.customers.append(self)
        self.save_customers_data()

    @classmethod
    def save_customers_data(cls):
        with open('customers.data', 'a') as file:
            for customer in cls.customers:
                file.write(f"{customer.username},{customer._password},{customer.id},{datetime.now()},{customer.secretkey}\n")

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
            if int(user[2]) == id:
                return True
        return False
    
    @classmethod
    def retrieve_secretkey(cls, id):
        existing_users = []
        try:
            with open('customers.data', 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    existing_users.append((user_data[0], user_data[1], user_data[2], user_data[3], user_data[4]))
        except FileNotFoundError:
            return False

        for user in existing_users:
            if int(user[2]) == id:
                return user[4]
        print('No such user! ')
        return False
    
    @classmethod
    def check_length(cls):
        existing_users = []
        try:
            with open('customers.data', 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    existing_users.append((user_data[0], user_data[1], user_data[2]))
        except FileNotFoundError:
            return 0

        return len(existing_users)

class Transactions:
    transactions = []
    def __init__(self, timestamp, customer_id, author_id, pid, relation):
        self.timestamp = timestamp
        self.cutomer_id = customer_id
        self.author_id = author_id
        self.pid = pid
        self.relation = relation
        self.transactions.append(self)
        self.save_transactions_data()

    @classmethod
    def save_transactions_data(cls):
        with open('transactions.data', 'a') as file:
            for transactions in cls.transactions:
                file.write(f"{transactions.timestamp},{transactions.customer_id},{transactions.author_id},{transactions.pid},{transactions.relation}\n")


