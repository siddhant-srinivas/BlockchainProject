import hashlib
import json
from datetime import time, datetime
from hashlib import sha256
from proof_of_work import generatePow

find_pow = generatePow()

def calculate_transaction_hash(transaction):
    #if isinstance(transaction,str):
    #    print(transaction)
    transactionString = str(transaction)
    #transactionString = json.dumps(transaction, sort_keys=True)
    return hashlib.sha256(transactionString.encode()).hexdigest()

class Block:
    def __init__(self, index, previous_hash, current_transactions, timestamp, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.current_transactions = current_transactions
        self.timestamp = timestamp or datetime.now().timestamp
        self.nonce = nonce
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.compute_hash()

    def compute_hash(self):  
        #block_string = json.dumps(self.__dict__, sort_keys=True)
        block_string = (
            str(self.index) +
            str(self.previous_hash) +
            ''.join(map(str, self.current_transactions)) +  # Convert list to string
            str(self.timestamp) +
            str(self.nonce)
        )
        first_hash = sha256(block_string.encode()).hexdigest()
        second_hash = sha256(first_hash.encode()).hexdigest() #Hashing twice for added security
        return second_hash

    def calculate_merkle_root(self):
        transaction_hashes = [calculate_transaction_hash(tx) for tx in self.current_transactions]
        return self.build_merkle_tree(transaction_hashes)

    @staticmethod
    def build_merkle_tree(transaction_hashes):
        if len(transaction_hashes) == 0:
            return None

        elif len(transaction_hashes) == 1:
            return transaction_hashes[0]

        elif len(transaction_hashes) % 2 == 1:
            transaction_hashes.append(transaction_hashes[-1]) #Duplicating last transaction

        parents = []
        i = 0
        while i < len(transaction_hashes):
            children = (
                    transaction_hashes[i] + transaction_hashes[i + 1]
            )
            parent = hashlib.sha256(children.encode()).hexdigest()
            parents.append(parent)
            i += 2

        return Block.build_merkle_tree(parents)

    def __str__(self):
        return str(self.__dict__)


class Blockchain:
    def __init__(self):
        self.hashChain = [] 
        self.transactions = []
        self.genesisBlock()
        self.blockCount = 0

    def __str__(self):
        return str(self.__dict__)

    def genesisBlock(self):  
        genesis_data = {
            'timestamp': datetime.now().timestamp(),
            'author_id': '',  # Placeholder for author ID
            'customer_id': '',  # Placeholder for customer ID
            'pid': '',  # Placeholder for product ID
            'relation': ''  # Placeholder for relation
        }
        genesisBlock = Block('Block0', 0x0, genesis_data , datetime.now().timestamp(), 0)
        genesisBlock.hash = genesisBlock.compute_hash()
        self.hashChain.append(genesisBlock.hash)
        self.transactions.append(genesisBlock)
        return genesisBlock

    def createBlock(self, data):
        transaction_hashes = [calculate_transaction_hash(tx) for tx in data]
        block = Block(len(self.hashChain), self.hashChain[-1], transaction_hashes, datetime.now().timestamp(), 0)
        block.hash = find_pow.mineBlock(block)
        self.hashChain.append(block.hash)
        self.transactions.append(block)

        self.blockCount += 1
        if self.blockCount % 100 == 0:
            self.adjust_difficulty(100)
        
        block_dict = {
            "index": block.index,
            "previous_hash": block.previous_hash,
            "current_transactions": block.current_transactions,
            "timestamp": block.timestamp,
            "nonce": block.nonce,
            "merkle_root": block.merkle_root,
            "hash": block.hash
        }
        return block_dict
        #return json.loads(str(block).replace('\'', '\"')) #Converts string back to dict

    def get_data(self):
        block_data_list = []
        for block in self.transactions:
            block_data = {
                "Index": block.index,
                "Timestamp": block.timestamp,
                "Previous Hash": block.previous_hash,  
                "Merkle Root": block.merkle_root,
                "Nonce": block.nonce
            }
            block_data_list.append(block_data)
        return block_data_list


    def getLastBlock(self):
        return self.hashChain[-1]

    def adjust_difficulty(self, n):
    
        block_times = []    # Collect block times for the last n blocks

        for block in self.transactions[-n:]:
            block_times.append(block.timestamp)

        actual_block_time = block_times[-1] - block_times[0]
        target_block_time = 300 #Adjustable, set to 5 mins 
        find_pow.adjustDifficulty(actual_block_time, target_block_time)