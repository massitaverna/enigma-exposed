import string
import unittest

from lib.internals import PlugBoard, Rotor, ConfiguredRotor, Reflector
import tests.utils


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
    def test_random_permutation(self):
        """Make sure the rotor is a random permutation, by checking that the number of fixed points is low"""
        r = Rotor()
        n_fixed_points = 0
        upper_bound = tests.utils.ensure_prob(len(string.ascii_lowercase), 1-1/10000)
        
        for x in range(len(string.ascii_lowercase)):
            if r.map(x) == x:
                n_fixed_points += 1
        
        self.assertLess(
            n_fixed_points,
            upper_bound,
            f"might have failed because of bad luck, try again ({n_fixed_points=}, {upper_bound=})"
        )

    def test_inverse_map(self):
        r = Rotor()

        for x in range(len(string.ascii_lowercase)):
            self.assertEqual(x, r.inverse_map(r.map(x)))
            self.assertEqual(x, r.map(r.inverse_map(x)))


class TestConfiguredRotor(unittest.TestCase):
    def setUp(self):
        self.positions = list(range(len(string.ascii_lowercase)))
        self.r = Rotor()
        self.cr = ConfiguredRotor(self.r)

    def test_plain_rotor(self):
        """
        Treat the configured rotor as a plain rotor, i.e. don't step it and set offset to 0.
        Make sure it behaves like a plain rotor.
        """
        self.cr.set_starting_position(0)
        
        for x in self.positions:
            self.assertEqual(self.cr.map(x), self.r.map(x))
            self.assertEqual(self.cr.inverse_map(x), self.r.inverse_map(x))

    def test_starting_position(self):
        """
        Don't step the configured rotor.
        Make sure the list of its outputs is the same of a plain rotor,
        just rotated by an offset equal to its starting position.
        """
        r_output = [self.r.map(x) for x in self.positions]

        for position in self.positions:
            with self.subTest(starting_position=position):
                self.cr.set_starting_position(position)

                cr_output = [self.cr.map(x) for x in self.positions]
                self.assertEqual(cr_output, r_output[position:] + r_output[:position])

    def test_turnover_once_per_full_cycle(self):
        turnovers = sum([self.cr.step() for _ in self.positions])
        self.assertEqual(turnovers, 1)

    def test_turnover_at_notch(self):        
        for position in self.positions:
            with self.subTest(starting_position=position):
                self.cr.set_starting_position(position)
                self.cr.set_turnover_notch((position+1) % len(self.positions))
                self.assertTrue(self.cr.step())

    def test_stepping(self):
        """
        Make sure stepping works as intended:
        mapping x after stepping is equivalent to mapping x+1 before stepping.
        """
        for input in self.positions:
            with self.subTest(input=input):
                output_1 = self.cr.map((input+1) % len(self.positions))
                self.cr.step()
                output_2 = self.cr.map(input)

                self.assertEqual(output_1, output_2)

    def test_periodic(self):
        first_cycle = [self.cr.map(x) for x in self.positions]
        [self.cr.step() for _ in self.positions]
        second_cycle = [self.cr.map(x) for x in self.positions]

        self.assertEqual(first_cycle, second_cycle)


class TestReflector(unittest.TestCase):
    def test_no_fixed_points(self):
        r = Reflector()
        for x in range(len(string.ascii_lowercase)):
            self.assertNotEqual(r.map(x), x)

    def test_is_involution(self):
        r = Reflector()
        for x in range(len(string.ascii_lowercase)):
            self.assertEqual(r.map(r.map(x)), x)