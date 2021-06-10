import hashlib
import json

def crypto_hash(*args): # *args now become a list of arguments that you want to pass in this function
    """
    Return a sha-256 hash of the given arguments. 
    Within the same data input, sha-256 only generate one unique string output.
    It is a one-way function, data to the hash.
    Because of these attributes, it is really useful in generating blockchains, since every block
    presents a unique hash based on its block fields.
    We can verify if the block is clean by regenerating its hash based on the same block field. 
    If the hash we generated is different from the original hash, we immediately know that the data is tampered.
    """
    stringsified_args = sorted(map(lambda arg: json.dumps(arg), args))
    # we sort this variable to prevent the situation that when there are two lists of arguments input
    # the elements in these two lists are the same but in different orders. If we don't sort the input
    # the output hash string for these two technically same input will be different.
    # this helps to transfer each argument that of any input format to string format
    joined_data = ''.join(stringsified_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest() # because sha-256 method can only intake byte-string
    # we can encode the input into UTF-8 format
    # hexdigest method helps to generate a unique 64 characters hexadecimal string value 

def main():
    print(f"crypto_hash('one',2,[3]): {crypto_hash('one',2,[3])}")
    print(f"crypto_hash(2,'one',[3]): {crypto_hash(2,'one',[3])}")
if __name__ == '__main__':
    main()