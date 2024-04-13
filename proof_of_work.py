import hashlib

class generatePow():
    def __init__(self):
        self.difficulty = 1  # Initial difficulty level

    def mineBlock(self, block):
        found = False
        block.nonce = 1
        difficulty = self.difficulty  #to change difficulty of computation
        while not found:
            computed_hash = block.compute_hash()
            sha = hashlib.sha256(computed_hash.encode())
            solution = sha.hexdigest()
            if solution.startswith('011' * difficulty):
                print('Proof of work found. Block Nonce is ', block.nonce)
                return solution

            block.nonce += 1
        
    def adjustDifficulty(self, actual_block_time, target_block_time):
        if actual_block_time < target_block_time:
            self.difficulty += 1  
        elif actual_block_time > target_block_time:
            self.difficulty -= 1  

        self.difficulty = max(1, self.difficulty)
    