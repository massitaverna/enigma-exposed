import random
import string
from typing import TypeVar

T = TypeVar('T')


def choose_k(L: list[T], k: int) -> list[T]:
	shuffled = list(L)
	random.shuffle(shuffled)
	return shuffled[:k]


def is_a_valid_position(x: int) -> bool:
	alphabet_length = len(string.ascii_lowercase)
	return (x >= 0 and x < alphabet_length)
