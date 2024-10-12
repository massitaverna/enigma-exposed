import string
import unittest

from lib.internals import PlugBoard


class TestPlugBoard(unittest.TestCase):
    def test_identity_mapping(self):
        p = PlugBoard(n_wires=0)
        for c in string.ascii_lowercase:
            self.assertEqual(p.map(c), c)

    def test_swap_two_letters_only(self):
        p = PlugBoard()
        pairings = ["a", "b"]
        p.configure(pairings)

        self.assertEqual(p.map("a"), "b")
        self.assertEqual(p.map("b"), "a")
        for c in string.ascii_lowercase:
            if c in pairings:
                continue
            self.assertEqual(p.map(c), c)

    def test_swap_multiple_letters(self):
        p = PlugBoard()
        pairings = ["a", "b", "m", "n", "x", "y"]
        p.configure(pairings)

        for i in range(0, len(pairings), 2):
            self.assertEqual(p.map(pairings[i]), pairings[i+1])
            self.assertEqual(p.map(pairings[i+1]), pairings[i])

        for c in string.ascii_lowercase:
            if c in pairings:
                continue
            self.assertEqual(p.map(c), c)

    def test_random_wiring_at_initialization(self):
        n_wires = 10
        p = PlugBoard(n_wires)

        swapped = 0
        for c in string.ascii_lowercase:
            if p.map(c) != c:
                swapped += 1

        self.assertEqual(swapped, 2*n_wires)
    
    def test_is_involution(self):
        p = PlugBoard(n_wires=10)

        for c in string.ascii_lowercase:
            self.assertEqual(p.map(p.map(c)), c)

    def test_pairings_must_be_even(self):
        with self.assertRaises(ValueError):
            p = PlugBoard(n_wires=0)
            p.configure(["a", "b", "c"])

    def test_self_pairing_is_invalid(self):
        with self.assertRaises(ValueError):
            p = PlugBoard(n_wires=0)
            invalid_pairing = ["a", "a"]
            p.configure(invalid_pairing)


class TestRotor(unittest.TestCase):
    pass
