# sha3.py
# Dylan and Keegan Palmieri
# SHA3-256 implementation
# CS301 Fall 2019


import sys
from os import path
import bitstring
from copy import deepcopy
import constant


"""
SHA3-256 implementation in Python

objective:
Compute the SHA3-256 hash of a given input.

arguments:
arg -- string or filename to be hashed (default "A")

For a nicely formatted document, see
https://keccak.team/files/Keccak-submission-3.pdf, which is the write-up
by the people who created the SHA3 Keccak algorithm with psuedocode and
excellent explainations of what everything does and how it works.
(And it has pictures!)

Overview of the algorithm:
For this implementation, we used the keccak-f[1600] algorithm. The basic
steps of the algorithm are as follows:
1. Pad the input P with the pattern 10* such that the length of the input
    is divisible by r (in this case, 1088)
2. Break P into an array of r-sized pieces, P_i
3. Initialize the state array S into a string of b (1600) zero bits
4. For each block P_i:
    a. Extend P_i by c zero bits, creating a string of length b
    b. XOR P_i with S
    c. Apply the block permutation function to S, creating a new state S
5. Initialize Z to the empty string
6. While the length of Z is less than d:
    a. Append the first r bits of S to Z
    b. If Z is still less than d bits long, apply the block permutation
        function to S, yielding a new state S
7. Truncate Z to d bits

The state permutation functions Theta, Rho, Pi, Chi, and Iota are
described in the document listed above, and are explained much better
than I could hope to here.

NOTE: There is currently a bug involving the state functions that is
    causing the code to not return the correct hash. This is a known bug
    and I'm working on it! :)
"""


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
        state = block_permutation(state)

    input_hash = bitstring.BitArray()
    while input_hash.len < constant.OUTPUT_LENGTH:
        input_hash.append(state[0:constant.BIT_RATE])
        state = block_permutation(state)
    del(input_hash[constant.OUTPUT_LENGTH:])

    return input_hash


def pad_input(string_to_pad):
    string_to_pad.prepend('0b1')
    while string_to_pad.len % constant.BIT_RATE != (constant.BIT_RATE - 1):
        string_to_pad.prepend('0b0')
    string_to_pad.prepend('0b1')


def block_permutation(state):
    state_prime = deepcopy(state)
    state_array = [[[int(0) for _ in range(constant.WORD_SIZE)] for _ in range(5)] for _ in range(5)]

    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array[x][y][z] = state[constant.WORD_SIZE*(5*y + x) + z]

    for i in range(12 + 2*constant.WORD_POWER):
        state_array = theta(state_array)
        state_array = rho(state_array)
        state_array = pi(state_array)
        state_array = chi(state_array)
        state_array = iota(state_array, i)

    for i in range(5):
        for j in range(5):
            for k in range(constant.WORD_SIZE):
                state_prime[constant.WORD_SIZE*(5*j + i) + k] = state_array[i][j][k]

    return state_prime


def theta(state_array):
    C = [[bitstring.Bits() for _ in range(constant.WORD_SIZE)] for _ in range(5)]
    for x in range(5):
        for z in range(constant.WORD_SIZE):
            C[x][z] = (state_array[x][0][z] ^ state_array[x][1][z] ^
                       state_array[x][2][z] ^ state_array[x][3][z] ^
                       state_array[x][4][z])
    D = [[bitstring.Bits() for _ in range(constant.WORD_SIZE)] for _ in range(5)]
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
    state_array_prime = deepcopy(state_array)
    for z in range(constant.WORD_SIZE):
        state_array_prime[0][0][z] = state_array[0][0][z]
    x, y = 1, 0
    for t in range(24):
        for z in range(constant.WORD_SIZE):
            state_array_prime[x][y][z] = state_array[x][y][z - int((t+1)*(t+2)/2) % constant.WORD_SIZE]
            x, y = y, (2*x + 3*y) % 5
    return state_array_prime


def pi(state_array):
    state_array_prime = deepcopy(state_array)
    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array_prime[x][y][z] = state_array[(x + 3*y) % 5][x][z]
    return state_array_prime


def chi(state_array):
    state_array_prime = deepcopy(state_array)
    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array_prime[x][y][z] = (state_array[x][y][z] ^
                                              ((state_array[(x+1) % 5][y][z] ^ 1) *
                                               state_array[(x+2) % 5][y][z]))
    return state_array_prime


def iota(state_array, round_index):
    state_array_prime = deepcopy(state_array)
    RC = [0 for _ in range(constant.WORD_SIZE)]
    for j in range(constant.WORD_POWER):
        RC[pow(2, j) - 1] = round_constant_generation(j + 7*round_index)
    for z in range(constant.WORD_SIZE):
        state_array_prime[0][0][z] = state_array[0][0][z] ^ RC[z]
    return state_array_prime


def round_constant_generation(t):
    if t % 255 == 0:
        return 1
    R = [1, 0, 0, 0, 0, 0, 0, 0]
    for i in range(1, t % 255):
        R.insert(0, 0)
        R[0] = R[0] ^ R[8]
        R[4] = R[4] ^ R[8]
        R[5] = R[5] ^ R[8]
        R[6] = R[6] ^ R[8]
        del(R[8:])
    return R[0]


def main():

   if not len(sys.argv) > 1:
        sys.argv.append('A')

    if path.isfile(sys.argv[1]):
        input_string = bitstring.BitArray(open(sys.argv[1], "rb").read())
    else:
        input_string = bitstring.BitArray(bin(int(
            ''.join(format(ord(x), 'b') for x in sys.argv[1]), base=2
        )))

    input_hash = compute_sha3(input_string)
    print("This is the hash of the given string or filename: %s" % input_hash)


main()
