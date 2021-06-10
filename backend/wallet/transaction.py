import uuid
import time

from backend.wallet.wallet import Wallet

class Transaction:
    """
    Document of an exchange in currency from a sender to one or more recipients.
    """
    def __init__(
        self = None,
        sender_wallet = None,
        recipient = None,
        amount = None,
        id = None,
        output = None,
        input = None
    ): # by giving parameters None value here means we set their default value to None
       # so we don't have to pass in the value for each every parameter when we call the function
        self.id = id or str(uuid.uuid4())[0:8] # if transaction id is provided in the parameters above
        # then we can directly use it, otherwise we have to generate a new one
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)
    
    def create_output(self, sender_wallet, recipient, amount):
        """
        Structure the output data for the transaction.
        How much the sender want to send and to which address.
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')

        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount # this will return the 
        # balance after the sender send money to the recipient

        return output

    def create_input(self, sender_wallet, output):
        """
        Structure the input data for the transaction.
        Sign the transaction and include the sender's public key and address.
        It's the sender's information.
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output) # to make a signature on behalf of the sender wallet
            # and the signature should be generated based on the output data 
        }

    def update(self, sender_wallet, recipient, amount):
        """
        Updated the transaction with an existing or new recipient.
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')

        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount 
            # because we are sending more to this existed recipient
        else: # new receipient
            self.output[recipient] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)
        # to generate new signature, we recreate new input rather than update old input

    def to_json(self):
        """
        Serialize the transction.
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialize a transaction json representation back into a Transaction instance.
        """
        return Transaction(**transaction_json) # because we pass in the same exact arguments of transaction_json into this function
       # which is the same as:
       # return Transaction(
       #    id = transaction_json['id'],
       #    output = transaction_json['output'],
       #    input = transaction_json['input']
       #)

    @staticmethod
    def is_valid_transaction(transaction):
        """
        Validate a transaction
        Raise an exception for invalid transactions.
        """
        output_total = sum(transaction.output.values())

        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction output values')

        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ): # which means the transaction is invalid
            raise Exception('Invalid signature')

def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    # which means the sender sends 15 to the recipient
    print(f'transaction.__dict__: {transaction.__dict__}')

    transaction_json = transaction.to_json()
    restored_transaction = Transaction.from_json(transaction_json)
    print(f'restored_transaction.__dict__: {restored_transaction.__dict__}')

if __name__ == '__main__':
    main()

