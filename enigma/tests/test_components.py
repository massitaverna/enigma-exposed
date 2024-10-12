import unittest

from lib.internals import PlugBoard


class TestPlugboard(unittest.TestCase):
    def test_identity_mapping(self):
        p = PlugBoard()