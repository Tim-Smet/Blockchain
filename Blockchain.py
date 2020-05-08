#Module 1: Create a Blockchain

#To be installed:

# Flask == 0.12.2: pip install Flask==0.12.2
# Postman HTTP client: https://www.getpostman.com/

#Importing the libraries:
import datetime
import hashlib
import json
from flask import Flask, jsonify

#Part 1 = building a blockchain
#How? We are going to use a class: We can build anything with a class (self driving car).
#Class contains  some advanced structure in wich u can include functions, 
#tools, methods, properties. All of them interacting with what you want to build.

class Blockchain:
    
    #The init method always takes one argument (self)
    #self will refer to the object that we create once the class is made
    def __init__(self):
        #initialize the chain. This will be a list containing the blocks
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            new_proof = block['proof']
            hash_operations = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operations[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    


#Part 2 = Mining a blockchain

#Creating web app
app = Flask(__name__)

#Creating blockchain
#Instance object from our class Blockchain
blockchain = Blockchain()

#mining new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    #we have to solve the proof of work problem based on the previous proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

#getting the full chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200

#running the app
app.run(host = '0.0.0.0', port = 5000)











