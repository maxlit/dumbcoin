"""
A cli tool to brute force the private key of a given public key (straightforward for dumbcoin).
"""

import argparse
from cryptos.keys import PublicKey
from cryptos.dumbcoin import DUMBCOIN

def brute_force_dumbcoin(public_key: PublicKey, COIN=DUMBCOIN):
    for sk in range(COIN.gen.n):
        candidate_public_key = PublicKey.from_sk(sk, COIN=COIN)
        if candidate_public_key.x == public_key[0] and candidate_public_key.y == public_key[1]:
            print('found private key:', hex(sk))
            return
    else:
        print('private key not found (check the public key)')
        return

# Assuming PublicKey constructor looks something like:
# def __init__(self, x, y, *args, **kwargs):
# Correctly passing x and y as named arguments

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Brute force the private key of a given public key for dumbcoin.')
    parser.add_argument('public_key', help='The public key in the format x,y (e.g., 8,3)')
    args = parser.parse_args()
    
    try:
        x, y = map(int, args.public_key.split(','))
        # Adjusting instantiation to pass x and y correctly
        public_key = (x,y)
    except ValueError:
        print("Error: Public key must be provided in the format x,y where both are integers.")
        exit(1)
    except TypeError:
        print("Error: Incorrect arguments provided to PublicKey constructor.")
        exit(1)

    brute_force_dumbcoin(public_key)