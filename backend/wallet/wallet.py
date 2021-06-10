import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of miner's balance.
    Allows a miner to authorize transactions.
    """

    def __init__(self):
        self.address = str(uuid.uuid4())[0:8] # this method can generate a unique address/ID based on timestamp
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key() # We can get the associate public key
        # according to the private key
        self.serialize_public_key()

    def sign(self, data):
        """
        Generate a signature based on data using the local private key.
        """
        # By using this signature function, other entities will be able to verify if that transaction
        # was indeed created by the sender.
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'), # because the input format of data can only be byte
            ec.ECDSA(hashes.SHA256())
        )) # convert these bytes into a string

    def serialize_public_key(self):
        """
        Reset the public key to the serialized version.
        """
        self.public_key = self.public_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def verify(public_key, data, signature):
        """
        This will verify a signature based on the original public_key and data.
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        ) # because above function turn the public key into utf8 format, now we need to change it
        # back to the object format to run this function, otherwise it will break our code

        (r, s) = signature # because decoded signature returns a tuple value

        try: # use try is to prevent if the following code does not work and break all the program
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature: # instead of using Exception, we can use a method called InvalidSignature
            # which is more specific
            return False


def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')
    # we can check the wallet's attributes(public key and private key) by calling a dictionary
    # function
    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    should_be_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'should_be_valid: {should_be_valid}')

    should_be_invalid = Wallet.verify(Wallet().public_key, data, signature) # we generate a new
    # random public key to imitate when hackers want to tamper our data and see if this method 
    # return correct value
    print(f'should_be_invalid: {should_be_invalid}')

if __name__ == '__main__':
    main()
