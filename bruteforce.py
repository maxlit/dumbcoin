import argparse
from cryptos.keys import PublicKey, Point
from cryptos.dumbercoin import DUMBERCOIN
from cryptos.bitcoin import BITCOIN  # Assuming the structure is similar

import time

def brute_force(public_key: PublicKey, COIN):
    start_time = time.time()  # Start timing
    for sk in range(COIN.gen.n):
        if sk > 0 and sk % 10000 == 0:  # Every 1000 iterations, report progress
            elapsed_time = time.time() - start_time
            print(f"{sk} keys were checked, it took {elapsed_time:.2f} seconds")
        
        candidate_public_key = PublicKey.from_sk(sk, COIN=COIN)
        if candidate_public_key.x == public_key.x and candidate_public_key.y == public_key.y:
            print('found private key:', hex(sk))
            return
    else:
        print('private key not found (check the public key)')
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Brute force the private key of a given public key.'
                                     , epilog="""
        Examples:
          For Bitcoin (futile):
          python bruteforce.py DC63620E1AA35D3CA8D3B6E702D954FCA0225ACD2E7B8FC80562108BB98FB99B,7280F708C4792F1ED031D7E5A505487A4FAF0CE1056C5C1A787A1CC73A63EFC7 --coin btc

          For Dumbercoin:
          python bruteforce.py 8,3
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('public_key', help='The public key in the format x,y (e.g., 8,3)')
    parser.add_argument('--coin', choices=['bitcoin', 'btc', 'dumbercoin', 'dmb'], default='dumbercoin', nargs='?',
                        help='Specify the coin network (bitcoin/btc or dumbercoin/dmb). Defaults to dumbercoin.')

    args = parser.parse_args()

    # Determine the coin based on the argument
    if args.coin in ('bitcoin', 'btc'):
        COIN = BITCOIN
        print("Warning: Brute forcing Bitcoin is computationally impractical. It is highly unlikely that a private key match will be found. Anyway, good luck!")
    else:
        COIN = DUMBERCOIN
    try:
        x_str, y_str = args.public_key.split(',')
        x = int(x_str, 16)  # Convert hex to integer
        y = int(y_str, 16)  # Convert hex to integer
        pt = Point(COIN.gen.G.curve, x, y)
        if not pt.is_valid():
            raise ZeroDivisionError
    except ValueError:
        print("Error: Public key must be provided in the format x,y where both are integers.")
        exit(1)
    except ZeroDivisionError:
        print("Error: the public key (%s, %s) is not on the elliptc curve of the coin %s. Please provide a valid public key." % (x, y, args.coin))
        exit(1)
     

    brute_force(pt, COIN)
