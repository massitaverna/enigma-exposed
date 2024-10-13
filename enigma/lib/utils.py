import random
import string
from typing import TypeVar

T = TypeVar('T')


class InvalidPosition(ValueError):
	def __init__(self, x: int, alphabet_length: int = len(string.ascii_lowercase)):
		super().__init__(f"position {x} does not exist: positions are between 0 and {alphabet_length-1}")


def choose_k(L: list[T], k: int) -> list[T]:
	shuffled = list(L)
	random.shuffle(shuffled)
	return shuffled[:k]


def is_a_valid_position(x: int, alphabet_length: int = len(string.ascii_lowercase)) -> bool:
	return (x >= 0 and x < alphabet_length)
