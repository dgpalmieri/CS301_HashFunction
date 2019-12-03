# sha3.py
# Dylan and Keegan Palmieri
# SHA3-256 implementation
# CS301 Fall 2019


import argparse  # Use with CLI method of input
import sys  # Use with debugging/writing input
from os import path
import bitstring
from copy import deepcopy
import constant


def compute_sha3(input_string):
    pad_input(input_string)
    padded_input = input_string
    padded_input_list = []

    for x in range(int(padded_input.len/constant.BIT_RATE)):
        padded_input_list.append(bitstring.BitArray(
            padded_input[x*constant.BIT_RATE:(x+1)*constant.BIT_RATE]
        ))

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
    count = 0
    state_array = [[[int(0) for _ in range(constant.WORD_SIZE)] for _ in range(5)] for _ in range(5)]

    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array[x][y][z] = state[count]
                count += 1
                assert(count <= state.len)

    for _ in range(12 + 2*constant.WORD_SIZE):
        state_array = theta(state_array)
        state_array = rho(state_array)
        state_array = pi(state_array)
        state_array = chi(state_array)
        state_array = iota(state_array)

    for i in range(5):
        for j in range(5):
            for k in range(constant.WORD_SIZE):
                state[(5*i + j)*constant.WORD_SIZE + k] = state_array[i][j][k]


def theta(state_array):
    C = [[0 for _ in range(constant.WORD_SIZE)] for _ in range(5)]
    for x in range(5):
        for z in range(constant.WORD_SIZE):
            C[x][z] = (state_array[x][0][z] ^ state_array[x][1][z] ^
                       state_array[x][2][z] ^ state_array[x][3][z] ^
                       state_array[x][4][z])
    D = [[0 for _ in range(constant.WORD_SIZE)] for _ in range(5)]
    for x in range(5):
        for z in range(constant.WORD_SIZE):
            D[x][z] = C[(x - 1) % 5][z] ^ C[(x + 1) % 5][(z - 1) % constant.WORD_SIZE]
    state_array_prime = deepcopy(state_array)
    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array_prime[x][y][z] = state_array[x][y][z] ^ D[x][z]
    return state_array_prime


def rho(state_array):
    state_array_prime = [[[0 for _ in range(constant.WORD_SIZE)] for _ in range(5)] for _ in range(5)]
    for z in range(constant.WORD_SIZE):
        state_array_prime[0][0][z] = state_array[0][0][z]
    x, y = 1, 0
    for t in range(24):
        for z in range(constant.WORD_SIZE):
            state_array_prime[x][y][z] = state_array[x][y][z - int((t+1)*(t+2)/2) % constant.WORD_SIZE]
            x, y = y, (2*x + 3*y) % 5
    return state_array_prime


def pi(state_array):
    state_array_prime = [[[0 for _ in range(constant.WORD_SIZE)] for _ in range(5)] for _ in range(5)]
    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array_prime[x][y][z] = state_array[(x + 3*y) % 5][x][z]
    return state_array_prime


def chi(state_array):
    state_array_prime = [[[0 for _ in range(constant.WORD_SIZE)] for _ in range(5)] for _ in range(5)]
    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array_prime[x][y][z] = (state_array[x][y][z] ^
                                              ((state_array[(x+1) % 5][y][z] ^ 1) *
                                               state_array[(x+2) % 5][y][z]))
    return state_array_prime


def iota(state_array):
    state_array_prime = [[[0 for _ in range(constant.WORD_SIZE)] for _ in range(5)] for _ in range(5)]

    return state_array


def round_constant_generation(t):
    return t


def main(function_arg=None):

    # USE THIS WHEN READY TO DEPLOY
    #    parser = argparse.ArgumentParser(
    #        description='Compute the SHA3-256 hash of an input.')
    #    parser.add_argument('input', metavar='input', type=str,
    #                        help='A relative or absolute filepath, a filename'
    #                             'in the current directory, or a string value')
    #    cline_args = parser.parse_args()
    #
    #    if not cline_args and not function_arg:
    #        arg = "A"
    #
    #    input_hash = compute_sha3(input_string)
    #    print("This is the hash of the given string or filename: %s" % input_hash)

    # USE THIS WHILE WRITING IN IDE
    if not len(sys.argv) > 1:
        sys.argv.append("A")

    # Consider using mmap here
    if path.isfile(sys.argv[1]) or function_arg and path.isfile(function_arg):
        if function_arg:
            input_string = bitstring.BitArray(open(function_arg, "rb").read())
        else:
            input_string = bitstring.BitArray(open(sys.argv[1], "rb").read())
    elif function_arg:
        input_string = bitstring.BitArray(bin(int(
            ''.join(format(ord(x), 'b') for x in function_arg), base=2
        )))
    else:
        input_string = bitstring.BitArray(bin(int(
            ''.join(format(ord(x), 'b') for x in sys.argv[1]), base=2
        )))

    input_hash = compute_sha3(input_string)
    print("This is the hash of the given string or filename: %s" % input_hash)


# hash of "A" 1c9ebd6caf02840a5b2b7f0fc870ec1db154886ae9fe621b822b14fd0bf513d6
main()
