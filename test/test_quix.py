import pytest
import unittest
from quix import quix


class QuixTest(unittest.TestCase):

    def setUp(self):
        self.dq = quix.Quix()
    
    def tearDown(self):
        self.dq.db.close()

    def test_values_from_key(self):
        assert(self.dq.values_from(b' "Que') == [b'mi'])

    def test_fragment_initial(self):
        assert(self.dq.fragment() is not None)

    def test_set_fragment_already_set(self):
        self.dq._fragment = b"foo bar bag farm"
        self.dq.fragment()
        assert(self.dq.fragment() is b"foo bar bag farm")
    
    def test_current_key(self):
        assert(self.dq.current_key() is not None)
    
    def test_current_key_with_without_initial_fragment(self):
        self.dq._current_key = None
        self.dq._fragment = b"foo bar\nbang bob son"
        assert(self.dq.current_key() == b"bob son")

    def test_values_initial(self):
        assert(self.dq.values() is not None)
        assert(type(self.dq.values()) is list)
        

    def test_values_with_initial_value(self):
        self.dq._values = [b"foo", b"bar", b"bang"]
        assert(self.dq.values() == [b"foo", b"bar", b"bang"])
