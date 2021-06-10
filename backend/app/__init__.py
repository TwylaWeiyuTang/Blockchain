import os
import random
import requests
from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction

app = Flask(__name__)
blockchain = Blockchain() # generate a blockchain instance
wallet = Wallet() # generate a Wallet instance
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool) # we can observe how multiple instances of the blockchain; transactions
# communicate with each other by using this pubsub functionality

@app.route('/') # create endpoint
def default():
    return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())# __repr__ helps to return in a string format

@app.route('/blockchain/mine')
def route_blockchain_mine():
    blockchain.add_block(transaction_pool.transaction_data())
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST']) # because here we are trying to post data about the
# transaction online, instead of getting data from online
def route_wallet_transact():
    transaction_data = request.get_json() # now transaction data is stored in a dictionary way
    transaction = transaction_pool.existing_transaction(wallet.address)

    if transaction:  # if transaction means true, because Python default is to treat values as true
        # default False value: False, None, 0, '', [], {}
        transaction.update(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        ) # this means the transaction exists and we update it with new data
    else:     
        transaction = Transaction(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        ) # this means the transaction does not exist in transaction pool, so we generate it

    pubsub.broadcast_transaction(transaction)

    print(f'transaction.to_json(): {transaction.to_json()}')
    return jsonify(transaction.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT # different ports are different nodes, they all are subscribed to listen to the same channels

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000) # reassign the port value for peer instances inbetween 5001-6000

    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    result_blockchain = Blockchain.from_json(result.json())

    try:
        blockchain.replace_chain(result_blockchain.chain)
        # to synchronize the nodes who newly subscribed to the blockchain channel
        print('\n -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'\n -- Error synchronizing: {e}')
app.run(port=PORT) # if we want this program to be run on other ports just put ports=5001 etc. inside the bracket
# localhost and 127.0.0.1 is reserved for the local development
# 5000 url is the port that the program is running on
# multiple applications can run on the same machine at the same time by using different ports



