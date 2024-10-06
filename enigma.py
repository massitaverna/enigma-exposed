import random
import string

N_AVAILABLE_ROTORS = 5
N_ROTORS = 3
N_WIRES = 10

T = TypeVar('T')


class PlugBoard:
	def __init__(self):
		self.mapping: dict[str, str] = {letter: letter for letter in string.ascii_lowercase}

	def configure(self, pairings: list[str]):
		if len(pairings) % 2 != 0:
			raise ValueError("Pairings of the plug board must be even")

		for x, y in zip(pairings[::2], pairings[1::2]):
			self.mapping[x] = y
			self.mapping[y] = x
	
	def configure_at_random(self, n_wires: int):
		pairings = choose_k(string.ascii_lowercase, k=2*n_wires)
		self.configure(pairings)

	def map(self, x: str) -> str:
		return self.mapping[x]


class Rotor:
	def __init__(self):
		n_pins = len(string.ascii_lowercase)
		self.mapping = list(range(n_pins))
		self.mapping.shuffle(output)

	def map(self, x: int) -> int:
		return self.mapping[x]


class ConfiguredRotor:
	def __init__(self, rotor: Rotor):
		self.rotor = rotor
		self.offset = 0

	def set_starting_position(self, offset: int):
		self.offset = offset

	def set_random_starting_position(self):
		self.offset = random.randint(0, len(string.ascii_lowercase))

	def map(self, x: int) -> int:
		self.rotor.map(x + self.offest)

	def step(self) -> bool:
		"""
		Step the rotor to the next position.
		Return a boolean indicating whether the next rotor should be stepped.
		We do not consider the double stepping anomaly.
		"""
		self.offset += 1
		self.offset = self.offest % len(string.ascii_lowercase)
		return False  # TODO: check notch


class Reflector:
	"""
	The reflector's wiring was known to the Allies.
	Also, since it mapped every letter to a _different_ letter,
	the reflector contributed to one of Enigma's weaknesses:
	namely, that a letter could not be encrypted into itself.
	"""
	mapping: dict[int, int] = {}
	
	def __init__(self):
		if not Reflector.mapping:
			pairings = random.shuffle(list(range(len(string.ascii_lowercase))))
			for x, y in zip(pairings[::2], pairings[1::2]):
				Reflector.mapping[x] = y
				Reflector.mapping[y] = x

	def map(self, x: int) -> int:
		return Reflector.mapping[x]


class Enigma:
	"""An implementation of the Enigma machine."""
	available_rotors: list[Rotor] = [Rotor() for _ in range(N_AVAILABLE_ROTORS)]
	
	def __init__(self):
		self.plug_board = PlugBoard()
		self.plug_board.configure_at_random(N_WIRES)
		
		rotors_in_use = choose_k(self.available_rotors, k=N_ROTORS)
		self.rotors: list[ConfiguredRotor] = []
		for rotor in rotors_in_use:
			configured_rotor = ConfiguredRotor()
			configured_rotor.set_random_starting_position()
			self.rotors.append(configured_rotor)

		# TODO: Ring settings

	@classmethod
	def get_available_rotors(cls) -> list[Rotor]:
		"""
		The available rotors were known to the Allies
		(what was unknown was the subset of rotors in use every day)
		"""
		return cls.available_rotors

	def encrypt(self, msg: str) -> str:
		pass

	def decrpyt(self, ctx: str) -> str:
		pass


def choose_k(L: list[T], k: int) -> list[T]:
	indices = list(range(len(L)))
	result = []

	for _ in range(k):
		index = random.choice(indices)
		indices.remove(index)
		result.append(L[index])

	return result