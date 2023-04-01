import unittest
from .quix import QuixSql  

class QuixTest(unittest.TestCase):

    def setUp(self):
        self.dq = QuixSql(db_path="dq.db")
    
    def tearDown(self):
        self.dq.db.close()

    # def test_values_from_key(self):
    #     assert(self.dq.values_from(' "Que') == ['mi'])

    def test_fragment_initial(self):
        assert(self.dq.fragment() is not None)

    def test_set_fragment_already_set(self):
        self.dq._fragment = "foo bar bag farm"
        self.dq.fragment()
        assert(self.dq.fragment() is "foo bar bag farm")
    
    def test_current_key(self):
        assert(self.dq.current_key() is not None)
    
    def test_current_key_with_without_initial_fragment(self):
        self.dq._current_key = None
        self.dq._fragment = "foo bar\nbang bob son"
        assert(self.dq.current_key() == "bob son")

    def test_values_initial(self):
        assert(self.dq.values() is not None)
        assert(type(self.dq.values()) is list)
        

    def test_values_with_initial_value(self):
        self.dq._values = [b"foo", b"bar", b"bang"]
        assert(self.dq.values() == [b"foo", b"bar", b"bang"])
