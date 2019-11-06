# sha3.py
# Dylan and Keegan Palmieri
# SHA3-256 implementation
# CS301 Fall 2019


import sys
from os import path
import bitstring
import constant


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


def compute_sha3(input_string):
    pad_input(input_string)
    padded_input = input_string
    padded_input.pos = 0
    padded_input_list = []
    for x in range(0, int(padded_input.len/constant.BIT_RATE)):
        padded_input_list.append(padded_input.read('bin:' + str(constant.BIT_RATE)))
    state = bitstring.BitStream('0b0')
    for _ in range(constant.BLOCK_WIDTH - 1):
        state.prepend('0b0')

    for p_i in padded_input_list:
        pass

    return "Hello!"  # input_hash


def pad_input(string_to_pad):
    string_to_pad.prepend('0b1')
    while string_to_pad.len % constant.BIT_RATE != (constant.BIT_RATE - 1):
        string_to_pad.prepend('0b0')
    string_to_pad.prepend('0b1')


def block_permutation():
    pass


def main():
    if not len(sys.argv) > 1:
        sys.argv.append("A")

    if path.isfile(sys.argv[1]):
        input_string = bitstring.BitStream(open(sys.argv[1], "rb").read())
    else:
        input_string = bitstring.BitStream(
            bin(int(''.join(format(ord(x), 'b') for x in sys.argv[1]), base=2))
        )

    input_hash = compute_sha3(input_string)
    print("This is the hash of the given string or filename: %s" % input_hash)


main()
