import random
import string
from typing import TypeVar

N_AVAILABLE_ROTORS = 5
N_ROTORS = 3
N_WIRES = 10

T = TypeVar('T')


class PlugBoard:
	"""
	The plug board (Steckerbrett) swaps letters in pairs.
	It is possible that a letter does not get swapped, i.e., it gets mapped to itself.
	"""
	def __init__(self):
		self.mapping: dict[str, str] = {letter: letter for letter in string.ascii_lowercase}

	def configure(self, pairings: list[str]):
		"""
		:param pairings: a list of letters where two adjacent letters represent a swapped pair
		"""
		if len(pairings) % 2 != 0:
			raise ValueError(
				f"length of provided pairings cannot be {len(pairings)}: pairings of the plug board must be even"
			)

		for x, y in zip(pairings[::2], pairings[1::2]):
			self.mapping[x] = y
			self.mapping[y] = x
	
	def configure_at_random(self, n_wires: int):
		"""
		Configure the plug board with a random set of swapped pairs.

		:param n_wires: the number of "wires" available to swap pairs
		"""
		pairings = choose_k(string.ascii_lowercase, k=2*n_wires)
		self.configure(pairings)

	def map(self, x: str) -> str:
		"""Swap a letter according to the plug board's wiring."""
		if x not in string.ascii_lowercase:
			raise ValueError("")

		return self.mapping[x]


class Rotor:
	"""
	The rotor implements a permutation over the alphabet.
	The permutation depends on the internal wiring of the rotor.
	"""
	def __init__(self):
		"""Create a rotor with a random internal wiring."""
		n_pins = len(string.ascii_lowercase)
		self.mapping = list(range(n_pins))
		random.shuffle(self.mapping)

	def map(self, x: int) -> int:
		"""Get the output position, given the input position `x`, according to the rotor's wiring."""
		alphabet_length = len(string.ascii_lowercase)
		if x < 0 or x >= alphabet_length:
			raise ValueError(f"position {x} does not exist: positions are between 0 and {alphabet_length-1}")
		return self.mapping[x]


class ConfiguredRotor:
	"""
	A rotor inserted into the Enigma machine.
	As such, it has a position, can be stepped, and has a turnover notch position.
	"""
	def __init__(self, rotor: Rotor):
		"""Configure the rotor with random starting and turnover notch positions."""
		self.rotor = rotor
		self.offset = random.randint(0, len(string.ascii_lowercase))
		self.turnover = random.randint(0, len(string.ascii_lowercase))

	def set_starting_position(self, position: int):
		"""Set the starting position to `position`."""
		alphabet_length = len(string.ascii_lowercase)
		if position < 0 or position >= alphabet_length:
			raise ValueError(f"position {position} does not exist: positions are between 0 and {alphabet_length-1}")
		self.offset = position

	def set_turnover_notch(self, position: int):
		"""Set the turnover notch to `position`."""
		alphabet_length = len(string.ascii_lowercase)
		if position < 0 or position >= alphabet_length:
			raise ValueError(f"position {position} does not exist: positions are between 0 and {alphabet_length-1}")
		self.turnover = position

	def map(self, x: int) -> int:
		"""Get the output position, given the input position `x`, according to the rotor's wiring and current position."""
		alphabet_length = len(string.ascii_lowercase)
		self.rotor.map((x + self.offset) % alphabet_length)

	def step(self) -> bool:
		"""
		Step the rotor to the next position.
		Return a boolean indicating whether the next rotor should be stepped.
		We do not consider the double stepping anomaly.
		"""
		self.offset += 1
		self.offset = self.offset % len(string.ascii_lowercase)
		return self.offset == self.turnover


class Reflector:
	"""
	The reflector (Umkehrwalze) reflects a signal exiting the last rotor back into it,
	so that the signal can traverse the rotors again.
	The reflection happens according to the reflector's internal wiring.

	The reflector's wiring was known to the Allies.
	Also, since it mapped every letter to a _different_ letter,
	the reflector contributed to one of Enigma's weaknesses:
	namely, that a letter could not be encrypted into itself.
	"""
	mapping: dict[int, int] = {}
	
	def __init__(self):
		"""
		Create a reflector with random internal wiring.
		The wiring is class-wide, hence all instances have the same wiring.
		"""
		if not Reflector.mapping:
			pairings = list(range(len(string.ascii_lowercase)))
			random.shuffle(pairings)
			for x, y in zip(pairings[::2], pairings[1::2]):
				Reflector.mapping[x] = y
				Reflector.mapping[y] = x

	def map(self, x: int) -> int:
		alphabet_length = len(string.ascii_lowercase)
		if x < 0 or x >= alphabet_length:
			raise ValueError(f"position {x} does not exist: positions are between 0 and {alphabet_length-1}")
		return Reflector.mapping[x]


class Enigma:
	"""An implementation of the Enigma machine."""
	available_rotors: list[Rotor] = [Rotor() for _ in range(N_AVAILABLE_ROTORS)]
	
	def __init__(self):
		self.plug_board = PlugBoard()
		self.plug_board.configure_at_random(N_WIRES)
		
		self.rotors = [ConfiguredRotor(rotor) for rotor in choose_k(self.available_rotors, k=N_ROTORS)]

	@classmethod
	def get_available_rotors(cls) -> list[Rotor]:
		"""
		Get the available rotors. These were known to the Allies
		(what was unknown was the subset of rotors in use every day).
		"""
		return cls.available_rotors

	def encrypt(self, msg: str) -> str:
		if set(msg) - set(string.ascii_lowercase) != set():
			raise ValueError
		raise NotImplementedError

	def decrypt(self, ctx: str) -> str:
		if set(ctx) - set(string.ascii_lowercase) != set():
			raise ValueError
		raise NotImplementedError


def choose_k(L: list[T], k: int) -> list[T]:
	shuffled = list(L)
	random.shuffle(shuffled)
	return shuffled[:k]
