'''
Helpful utility methods
'''
import os
import sys
import random


def generate_secret_key_file(path):
    '''
    Generate the secret key/file
    '''
    k = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
    try:
        with open(path, 'w') as f:
            f.write(k)
    except Exception as e:
        print("Unable to create secret key file: ", str(e))
        sys.exit(-1)

    return k


def read_secret_key(path):
    '''
    Load the secret key from a file
    '''
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print("Unable to load secret key from file: ", str(e))
        sys.exit(-1)


def get_secret_key(path):
    '''
    Handles getting the secret key
    '''
    if not os.path.exists(path):
        print("Secret key file {} not found. Creating...".format(path))
        return generate_secret_key_file(path)

    print("Loading secret key from file {}.".format(path))
    return read_secret_key(path)
