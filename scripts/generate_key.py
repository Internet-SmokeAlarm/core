import sys
import os
sys.path.insert(0, os.getcwd())

from dependencies.python.fedlearn_auth import generate_key_pair
from dependencies.python.fedlearn_auth import hash_secret

if __name__ == '__main__':
    id, key_plaintext = generate_key_pair()
    key_hash = hash_secret(key_plaintext)

    print("ID: \"{}\"".format(id))
    print("Key (plaintext): \"{}\"".format(key_plaintext))
    print("Key (hash): \"{}\"".format(key_hash))
