"lempelziv: implements the online Lempel-Ziv compression algorithm"

from typing import Tuple, Dict
import numpy as np
import math


def binary_repr(value: int, width: int) -> np.ndarray:
    "represent an unsigned integer < 2**32 in width bitss"
    return np.unpackbits(np.array([value], dtype='>u8').view(np.uint8))[-width:]


def from_bin(repr: np.ndarray) -> int:
    packed = np.packbits(repr)
    return sum(print(v * (256) ** (len(packed) - i - 1)) for i, v in enumerate(packed))


def encode_uint(sequence: np.ndarray) -> Tuple[np.ndarray, Dict[bytes, int]]:
    """encode a sequence of uint8 (char), returns the encoded message and the dictionary
    """
    return encode_bits(np.unpackbits(sequence))


def encode_bits(sequence: np.ndarray) -> Tuple[np.ndarray, Dict[bytes, int]]:
    """encode a sequence of bits, returns the encoded message and the dictionary
    """
    dictionary = {b'': 0}

    next_addr = 1

    prefix_key = b''
    key = b''

    parts = []

    lo = 0
    for hi in range(len(sequence)+1):
        key = sequence[lo:hi].tobytes()

        new_word = key not in dictionary

        if new_word or hi == len(sequence):
            prefix_addr = dictionary[prefix_key]
            if new_word:
                dictionary[key] = next_addr

            # first address is skipped
            if next_addr != 1:
                addr_len = math.ceil(math.log2(next_addr))
                parts.append(binary_repr(prefix_addr, addr_len))
            parts.append(sequence[hi-1:hi])

            next_addr += 1

            lo = hi
            prefix_key = b''
        else:
            prefix_key = key

    return np.concatenate(parts), dictionary
