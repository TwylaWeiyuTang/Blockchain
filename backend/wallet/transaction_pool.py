class TransactionPool:
    def __init__(self):
        self.transaction_map = {}
        # our transaction pool is going to store the received transactions within this map dict

    def set_transaction(self, transaction):
        """
        Set a transaction in the transaction pool.
        """
        self.transaction_map[transaction.id] = transaction

    def existing_transaction(self, address):
        # address: the address of the sender wallet that already generated transaction that we are looking for
        """
        Find a transaction genertaed by the address in the transaction pool.
        """
        for transaction in self.transaction_map.values():
        # get a list of all the transactions
            if transaction.input['address'] == address:
                return transaction
            
    def transaction_data(self):
        """
        Return the transactions of the transaction pool represented in their json serialized form.
        """

        return list(map(lambda transaction: transaction.to_json(), self.transaction_map.values()))

    def clear_blockchain_transactions(self, blockchain):
        """
        Delete the already recorded blockchain transactions from the transaction pool.
        """
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass
