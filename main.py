from datetime import datetime
from hashlib import sha256
from block import Blockchain
from nodes import Author, Customer
import string
import random
import hmac
import hashlib

blockchain = Blockchain()

def verify_user(secretkey):
    challenge = input("Enter the challenge: ")
    bit = random.randint(0, 1) 
    print('the random bit is ', bit)
    challenge = challenge + str(bit)
    print('the contents of hmac.new are',secretkey.encode(),'zzzz',challenge.encode(),'zzzz',hashlib.sha256)
    expected_response = hmac.new(secretkey.encode(), challenge.encode(), hashlib.sha256).hexdigest()

    response = input("Give your response to the challenge and bit: ")
    print('expected: ',expected_response)
    print('received: ',response)
    is_authenticated = hmac.compare_digest(expected_response, response)
    return is_authenticated


def main():
    transactions = []
    products = {}
    busyCustomers = []
    busyAuthors = []

    exitCond = 0
    while exitCond == 0:
        print(""" 
        ------------------------------------------------------
        🛒 Choose an action:
        1. Login / Signup 
        2. Buy a research paper / Comic book
        3. View all the products and their owners
        4. Update product status/Add transaction
        5. Mine a block
        6. View a block
        7. Terminate program
        ------------------------------------------------------
        """)
        user_input = input("Enter your Choice: \n")
        if user_input == '1':  #########################################################################################################################################
            role = input("Enter A to login/signup as an Author and C to login/signup as a Customer\n").lower()
            if role == 'a':
                user_answer = input("Have you already registered? Enter y for yes and n for no\n").lower()
                if(user_answer == 'y'):
                    id = int(input("Enter your ID: \n"))
                    user_found = False
                    user_found = Author.check_username_exists(id)
                    if not user_found:
                        print("You have not registered yet! Enter a username and password:")
                        username = str(input("Username: "))
                        password = str(input("Password: "))
                        secretkey = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))    #generates a random string of length 5 that we are taking as secret key for this user
                        print("Your secret key is: ", secretkey)
                        if username != '' and password != '':
                            Author(username, password, id, secretkey)
                            print(f"Author {username} registered successfully")
                        else:
                            print("\n Username and/or password can't be empty, please try again \n")
                        
                        numPapers = int(input("Enter the number of papers you own: "))
                        for i in range(1, numPapers+1):
                            productNo = input(f"Enter the ID of paper number {i}: ")
                            products[productNo] = id

                elif(user_answer == 'n'):
                    id = int(input("Enter an appropriate author ID: \n"))
                    print('Enter a username and password:')
                    username = str(input("Username: "))
                    password = str(input("Password: "))
                    secretkey = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))    #generates a random string of length 5 that we are taking as secret key for this user
                    print("Your secret key is: ", secretkey)
                    if username != '' and password != '':
                        Author(username, password, id, secretkey)
                        print(f"Author {username} registered successfully")
                    else:
                        print("\n Username and/or password can't be empty, please try again \n")

                    numPapers = int(input("Enter the number of papers you own: "))
                    for i in range(1, numPapers+1):
                        productNo = input(f"Enter the ID of paper number {i}: ")
                        products[productNo] = id

            elif role == 'c':
                user_answer = input("Have you already registered? Enter y for yes and n for no\n").lower()
                if(user_answer == 'y'):
                    id = int(input("Enter your ID: \n"))
                    user_found = False
                    # for users in Customer.customers:
                    #     if users.id == id:
                    #         user_found = True
                    user_found = Customer.check_username_exists(id)
                    if not user_found:
                        print("You have not registered yet! Enter a username and password:")
                        username = str(input("Username: "))
                        password = str(input("Password: "))
                        secretkey = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))    #generates a random string of length 5 that we are taking as secret key for this user
                        print("Your secret key is: ", secretkey)
                        if username != '' and password != '':
                            Customer(username, password, id, secretkey)
                            print(f"Customer {username} registered successfully")
                        else:
                            print("\n Username and/or password can't be empty, please try again \n")
                elif(user_answer == 'n'):
                    id = int(input("Enter an appropriate customer ID: \n"))
                    print('Enter a username and password:')
                    username = str(input("Username: "))
                    password = str(input("Password: "))
                    secretkey = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))    #generates a random string of length 5 that we are taking as secret key for this user
                    print("Your secret key is: ", secretkey)
                    Customer(username, password, id, secretkey)
                    print(f'Customer {username} registered successfully!')
            else:
                print("Invalid role entered. Please enter either A or C\n")

        elif user_input == '2':   #############################################################################################################################################
            role = input("Enter A to login as an Author and C to login as a Customer\n").lower()
            if role == 'a':
                print("An author cannot buy a research paper. Please choose another action or login as a customer. ")
                continue
            
            elif role != 'c':
                print("Invalid role entered. Please enter either A or C\n")
                continue

            customerId = int(input("Enter ID of the Customer: \n"))

            secretkey = Customer.retrieve_secretkey(customerId)
            auth = verify_user(secretkey)

            if auth == False:
                print('Challenge-Response Authentication unsuccessful! ')
                continue
            else:
                print('Challenge-Response Authentication successful! ')

            user_found = False
            for users in Customer.customers:
                if users.id == customerId:
                    user_found = True
            if not user_found:
                print("Customer not found. Please register and try again.\n")

            elif len(Author.authors) == 0:
                print("There are no authors available. Please register an author\n")

            elif customerId in busyCustomers:
                print("Customer is already in a transaction. Please try again. \n")

            else:
                pid = input("Enter the product you want to buy \n")
                if pid in products:
                    authorId = products[pid]
                    if authorId in busyAuthors:
                        print("The author is busy with an existing transaction. Please try again later.")

                    else:
                        busyAuthors.append(authorId)
                        busyCustomers.append(customerId)
                        transactions.append(
                            {'timestamp': datetime.now().timestamp(), 
                             'customer_id': customerId,
                             'author_id': authorId, 'pid': pid,
                             'relation': "cta"})
                        print("Order placed successfully!\n")
                        #products.remove(pid)
                else:
                    print("Product unavailable\n")

        elif user_input == '3': ########################################################################################################################################
            for key, value in products.items():
                print(f"Paper number: {key}, Author ID: {value}")

        elif user_input == '4':  ###########################################################################################################################################
            role = input("Enter A for Author and C for Customer\n").lower()
            pid = input("Enter product id: \n")
            if role == 'a':
                found = False
                customer_id = None
                authorId = int(input("Enter your ID:"))
                secretkey = Author.retrieve_secretkey(authorId)
                auth = verify_user(secretkey)   #hmac

                if auth == False:
                    print('Challenge-Response Authentication unsuccessful! ')
                    continue
                else:
                    print('Challenge-Response Authentication successful! ')

                for i in transactions:
                    if i.get('relation') == "cta" and i.get('pid') == pid:
                        customer_id = i['customer_id']
                        found = True

                    if (i.get('relation') == "atc" or i.get('relation') == "cr") and i.get('pid') == pid and products[pid] == i.get('author_id'):
                        found = False
                        break

                if found is False:
                    print("No pending orders")

                else:
                    if products[pid] != authorId:
                        print(f"first {type(products[pid])}, second {type(authorId)}")
                        print("You cannot add a transaction for a paper you do not own.")
                        continue

                    transactions.append(
                        {'timestamp': datetime.now().timestamp(), 'author_id': authorId,
                         'customer_id': customer_id, 'pid': pid,
                         'relation': "atc"})

                    print("Transaction from author to customer added successfully.")

            elif role == 'c':
                found = False
                customer_id = None
                for i in transactions:
                    if i.get('relation') == "atc" and i.get('pid') == pid:
                        customer_id = i['customer_id']
                        pid = i['pid']
                        authorId = products[pid]
                        found = True
                    if i.get('relation') == "cr" and i.get('pid') == pid and products[pid] == i.get('author_id'):
                        found = False
                        break
                if found is False:
                    print("No pending order")
                else:
                    transactions.append(
                        {'timestamp': datetime.now().timestamp(), 'author_id': authorId,
                         'customer_id': customer_id, 'pid': pid,
                         'relation': "cr"})

                    print("Transaction of customer receiving the product added successfully ")

            else:
                print("Invalid role entered. Please enter either A or C\n")

        elif user_input == '5':  ################################################################################################################################################
            pid = input("Enter product id: \n")
            customer_id = None
            user_found = False
            for i in transactions:
                if i.get('relation') == "cr" and i.get('pid') == pid:
                    user_found = True
                    customer_id = i.get('customer_id')
                    break
            if user_found is False:
                print("Transaction not complete, mining not possible")
            else:
                blockchain.createBlock(transactions)
                busyCustomers.remove(customer_id)
                print("Block added successfully")


        elif user_input == '6':  #################################################################################################################################################
            blocks_data = blockchain.get_data()
            for block_data in blocks_data:
                for key, value in block_data.items():
                    print(f"{key} : {value}")
                print("\n")

        elif user_input == '7':
            print("Exiting...")
            break

        exitCond = int(input("Enter 0 to continue and 1 to exit: \n"))
    return products


siddhant = main()