"""
Bitcoin-specific functions, classes, utilities and parameters
"""

from dataclasses import dataclass
from .curves import Curve, Point, Generator

# -----------------------------------------------------------------------------
# public API
__all__ = ['DUMBCOIN']

# -----------------------------------------------------------------------------

@dataclass
class Coin:
    gen: Generator

# -----------------------------------------------------------------------------

def dumbcoin_gen():
    # Bitcoin uses secp256k1: http://www.oid-info.com/get/1.3.132.0.10
    p = 0x000000000000000000000000000000000000000000000000000000000000000B # 11
    a = 0x0000000000000000000000000000000000000000000000000000000000000001
    b = 0x0000000000000000000000000000000000000000000000000000000000000006
    Gx = 0x0000000000000000000000000000000000000000000000000000000000000002
    Gy = 0x0000000000000000000000000000000000000000000000000000000000000007
    n = 0x000000000000000000000000000000000000000000000000000000000000000D # 13
    curve = Curve(p, a, b)
    G = Point(curve, Gx, Gy)
    gen = Generator(G, n)
    return gen

# create an object that can be imported from other modules
DUMBCOIN = Coin(dumbcoin_gen())
