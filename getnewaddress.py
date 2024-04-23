"""
A cli tool that generates and prints a new Bitcoin or Dumbcoin address.
Specifically, the tool prints:
- a new secret key
- the associated public key
- the address
"""

import argparse
from cryptos.keys import gen_secret_key, PublicKey
from cryptos.bitcoin import BITCOIN
from cryptos.dumbcoin import DUMBCOIN
import random

def generate_address(network):
    if network in ['bitcoin', 'btc']:
        coin = "btc"
        crypto = BITCOIN
    elif network in ['dumbcoin', 'dmb']:
        crypto = DUMBCOIN
        coin = "dmb"
    else:
        raise ValueError("Invalid network option. Use 'bitcoin'/'btc' or 'dumbcoin'/'dmb'.")

    # generate a secret/public key pair
    if coin == 'btc':
        secret_key = gen_secret_key(crypto.gen.n)
    else:
        secret_key = random.randint(2, crypto.gen.n)
    public_key = PublicKey.from_sk(secret_key, COIN=crypto)
    print('generated secret key:')
    print(hex(secret_key))
    print('corresponding public key:')
    if coin == "btc":
        print('x:', format(public_key.x, '064x').upper())
        print('y:', format(public_key.y, '064x').upper())
    else:
        print('x:', public_key.x)
        print('y:', public_key.y)

    # get the associated address
    addr = public_key.address(net='main', compressed=True)
    print('compressed {} address (b58check format):'.format(network))
    print(addr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Bitcoin or Dumbcoin address')
    parser.add_argument('network', choices=['bitcoin', 'btc', 'dumbcoin', 'dmb'], help='Specify the network (bitcoin/btc or dumbcoin/dmb)')
    args = parser.parse_args()
    generate_address(args.network)

