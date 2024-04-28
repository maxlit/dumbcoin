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
from cryptos.dumbercoin import DUMBERCOIN

def generate_address(network):
    if network in ['bitcoin', 'btc']:
        coin = "btc"
        crypto = BITCOIN
    elif network in ['dumbercoin', 'dmb']:
        crypto = DUMBERCOIN
        coin = "dmb"
    else:
        raise ValueError("Invalid network option. Use 'bitcoin'/'btc' or 'dumbercoin'/'dmb'.")

    # generate a secret/public key pair
    secret_key = gen_secret_key(crypto.gen.n, coin)
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
    parser = argparse.ArgumentParser(description='Generate Bitcoin or Dumbercoin address')
    parser.add_argument('network', choices=['bitcoin', 'btc', 'dumbercoin', 'dmb'],
                        help='Specify the network (bitcoin/btc or dumbercoin/dmb)',
                        default='bitcoin',  # Set default value to 'dumbercoin'
                        nargs='?')  # Make the argument optional
    args = parser.parse_args()
    generate_address(args.network)

