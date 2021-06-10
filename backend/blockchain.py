from backend.blockchain.block import Block
# since we import the whole block file, this file will also executes the codes that are not in
# the Block function, as long as it's in block.py file

class Blockchain:
    """
    Blockchain: a public ledge of transactions.
    Implemented as a list of blocks - dataset of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data)) # self.chain[-1] here represents the last_block

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following rules apply:
        1. The incoming chain must be longer than the local one
        2. The incoming chain is formatted properly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer.')
        try:    
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')
        # if the incoming chain can pass the above two points, then it has met the requirements and followed the rules
        self.chain = chain

    def to_json(self):
        """
        The goal of this method is to serialize the blockchain into a list of blocks.
        """
        return list(map(lambda block: block.to_json(), self.chain)) # this returns in a list, so it can be jsonified
        # self.chain is the list of chain need to be passed into the lambda function

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a Blockchain instance.
        The result will contain a chain list of Block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
        # transforming the list of chains from json format to the block instances using lambda function
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
        1. the chain must start with the genesis block;
        2. blocks must be formatted correctly.
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        for i in range (1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

def main():

    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)

    print(f'blockchain.py__name__: {__name__}')
    # if we run this code, the result we get here is the __name__ for block.py and the __main__ for
    # blockchain.py, because we are running blockchain.py file, instead of block.py file.

if __name__ == '__main__': # check if name is equal to '__main__' module
    main() # this code will help us generate output of the '__main__' file.