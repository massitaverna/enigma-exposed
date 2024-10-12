import string
import unittest

from lib.internals import PlugBoard


class TestPlugboard(unittest.TestCase):
    def test_identity_mapping(self):
        p = PlugBoard(n_wires=0)
        for c in string.ascii_lowercase:
            self.assertEqual(p.map(c), c)