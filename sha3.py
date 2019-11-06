# sha3.py
# Dylan and Keegan Palmieri
# SHA3-256 implementation
# CS301 Fall 2019


import sys
from os import path
import bitstring

"""
Functions
    Main SHA-3 compute
    Padding function
    Block permutation

Vars
    Input bit string N
    permutation block width b = 1600
    rate r - size of read and write chunks = 1088
    output length d = 256
    array State = 5x5 array of shorts (64 bits)
    capacity c = 512
"""


def compute_sha3():
    pass


def pad_input():
    pass


def block_permutation():
    pass


def main():
    if not len(sys.argv) > 1:
        sys.argv.append("A")

    if path.isfile(sys.argv[1]):
        N = bitstring.ConstBitStream(open(sys.argv[1], "rb").read())
    else:
        N = bitstring.ConstBitStream(
            bin(int(''.join(format(ord(x), 'b') for x in sys.argv[1]), base=2))
        )

    print(N)


main()
