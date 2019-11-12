# sha3.py
# Dylan and Keegan Palmieri
# SHA3-256 implementation
# CS301 Fall 2019


import sys
from os import path
import bitstring
import constant


def compute_sha3(input_string):
    pad_input(input_string)
    padded_input = input_string
    padded_input_list = []

    for x in range(0, int(padded_input.len/constant.BIT_RATE)):
        padded_input_list.append(
            bitstring.BitArray(padded_input[x*constant.BIT_RATE:(x+1)*constant.BIT_RATE])
        )

    state = bitstring.BitArray('0b0')
    for _ in range(constant.BLOCK_WIDTH - 1):
        state.prepend('0b0')

    for p_i in padded_input_list:
        for _ in range(constant.CAPACITY):
            p_i.append("0b0")
        state ^= p_i
        block_permutation(state)

    input_hash = bitstring.BitArray()
    while input_hash.len < constant.OUTPUT_LENGTH:
        input_hash.append(state[0:constant.BIT_RATE])
        block_permutation(state)
    del(input_hash[constant.OUTPUT_LENGTH:])

    return input_hash


def pad_input(string_to_pad):
    string_to_pad.prepend('0b1')
    while string_to_pad.len % constant.BIT_RATE != (constant.BIT_RATE - 1):
        string_to_pad.prepend('0b0')
    string_to_pad.prepend('0b1')


def block_permutation(state):
    pass


def main():
    if not len(sys.argv) > 1:
        sys.argv.append("A")

    if path.isfile(sys.argv[1]):
        input_string = bitstring.BitArray(open(sys.argv[1], "rb").read())
    else:
        input_string = bitstring.BitArray(
            bin(int(''.join(format(ord(x), 'b') for x in sys.argv[1]), base=2))
        )

    input_hash = compute_sha3(input_string)
    print("This is the hash of the given string or filename: %s" % input_hash)

# hash of "" a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
main()
