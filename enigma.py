import random
import string
from typing import Optional

from utils import choose_k, is_a_valid_position

N_AVAILABLE_ROTORS = 5
N_ROTORS = 3
N_WIRES = 10


class InvalidPosition(ValueError):
	def __init__(self, x):
		alphabet_length = len(string.ascii_lowercase)
		super().__init__(f"position {x} does not exist: positions are between 0 and {alphabet_length-1}")


class PlugBoard:
	"""
	The plug board (Steckerbrett) swaps letters in pairs.
	It is possible that a letter does not get swapped, i.e., it gets mapped to itself.
	"""
	def __init__(self, n_wires: Optional[int] = 0):
		"""
		Create a plugboard with random wirings.
		
		:param Optional[int] n_wires: The number of wires to randomly connect on the plug board.
		If zero, `self.map()` is the identity function. Default is 0.
		"""
		self.mapping: dict[str, str] = {letter: letter for letter in string.ascii_lowercase}
		if n_wires > 0:
			pairings = choose_k(string.ascii_lowercase, k=2*n_wires)
			self.configure(pairings)

	def configure(self, pairings: list[str]):
		"""
		:param list[str] pairings: a list of letters where two adjacent letters represent a swapped pair
		"""
		if len(pairings) % 2 != 0:
			raise ValueError(
				f"length of provided pairings cannot be {len(pairings)}: pairings of the plug board must be even"
			)

		for x, y in zip(pairings[::2], pairings[1::2]):
			self.mapping[x] = y
			self.mapping[y] = x

	def map(self, c: str) -> str:
		"""Swap a letter according to the plug board's wiring."""
		alphabet = string.ascii_lowercase
		if c not in alphabet:
			raise ValueError(
				f"character {c} does not belong to the alphabet: "
				f"valid characters are between {alphabet[0]} and {alphabet[-1]}"
			)
		return self.mapping[c]


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
		if not is_a_valid_position(x):
			raise InvalidPosition(x)
		return self.mapping[x]
	
	def inverse_map(self, y: int) -> int:
		"""Get the input position that results in the output `y`, according to the rotor's wiring."""
		if not is_a_valid_position(y):
			raise InvalidPosition(y)
		return self.mapping.index(y)


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
		if not is_a_valid_position(position):
			raise InvalidPosition(position)
		self.offset = position

	def set_turnover_notch(self, position: int):
		"""Set the turnover notch to `position`."""
		if not is_a_valid_position(position):
			raise InvalidPosition(position)
		self.turnover = position

	def map(self, x: int) -> int:
		"""Get the output position, given the input position `x`, according to the rotor's wiring and current position."""
		alphabet_length = len(string.ascii_lowercase)
		return self.rotor.map((x + self.offset) % alphabet_length)

	def inverse_map(self, y: int) -> int:
		"""Get the input position that results in the output `y`, according to the rotor's  and current position."""
		alphabet_length = len(string.ascii_lowercase)
		return self.rotor.inverse_map((y + self.offset) % alphabet_length)

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
		"""Get the reflected position, given the input position `x`, according to the reflector's internal wiring."""
		if not is_a_valid_position(x):
			raise InvalidPosition(x)
		return Reflector.mapping[x]


class Enigma:
	"""An implementation of the Enigma machine."""
	available_rotors: list[Rotor] = [Rotor() for _ in range(N_AVAILABLE_ROTORS)]
	
	def __init__(self):
		self.plug_board = PlugBoard(N_WIRES)
		self.rotors = [ConfiguredRotor(rotor) for rotor in choose_k(self.available_rotors, k=N_ROTORS)]
		self.reflector = Reflector()

	@classmethod
	def get_available_rotors(cls) -> list[Rotor]:
		"""
		Get the available rotors. These were known to the Allies
		(what was unknown was the subset of rotors in use every day).
		"""
		return cls.available_rotors

	def encrypt(self, msg: str) -> str:
		"""
		Encrypt a message and update the internal state of the machine.

		When encrypting a message, each of its letters go through the plugboard, the rotors,
		gets reflected back into the rotors, and finally goes through the plugboard again.

		Each letter makes the first rotor step, and possibly other rotors too, depending on the ring settings.

		After a message is encrypted, another one can be encrypted: the output is the same as if the
		concatenation of the two messages was encrypted in one function call.
		"""
		if set(msg) - set(string.ascii_lowercase) != set():
			raise ValueError("plaintext should be lowercase ASCII characters only")
		
		ctx = ""
		for letter in msg:
			ptx_letter = self.plug_board.map(letter)
			x = string.ascii_lowercase.index(ptx_letter)
			x = self._rotor_forward_path(x)
			x = self.reflector.map(x)
			x = self._rotor_return_path(x)
			ctx_letter = self.plug_board.map(string.ascii_lowercase[x])
			ctx += ctx_letter

		return ctx

	def decrypt(self, ctx: str) -> str:
		"""
		Decrypt a message and update the internal state of the machine.

		Decryption is identical to encryption. See `self.encrypt` for more details.
		"""
		return self.encrypt(ctx)
	
	def _rotor_forward_path(self, x: int) -> int:
		step = True
		for rotor in self.rotors:
			if step:
				step = rotor.step()
			x = rotor.map(x)
		return x
	
	def _rotor_return_path(self, x: int) -> int:
		for rotor in self.rotors[::-1]:
			x = rotor.inverse_map(x)
		return x
