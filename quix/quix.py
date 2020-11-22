import bson
import plyvel
from random import choice, randrange

class Quix(object):
    def __init__(self, db_path="./dqdb", text_path="./don-quixote.txt"):
        self.db = plyvel.DB(db_path, create_if_missing=True)
        self.keys = [key for key, value in self.db.iterator()]
        self.the_text = open(text_path).read().encode("utf8")
        self.split_text = self.the_text.split(b" ")
        self._fragment = choice(self.keys)
        self._current_key = self._fragment
        self._values = None

    
    def generate_fragment(self):
        while len(self.values()) > 0:
          next_word = self.values().pop(randrange(len(self.values())))
        
          if b" ".join([self.fragment(), next_word]) in self.the_text:
              self._fragment = b" ".join([self.fragment(), next_word])
              self._current_key = None
              self._values = None
              self.generate_fragment()
          else:
              pass
        return(self.fragment().decode("utf8"))


    def values(self):
        if self._values is None:
            self._values = self.values_from(self.current_key())
        return self._values

    def current_key(self):
        if self._current_key is None:
            new_key_elments = self.fragment().split(b' ')[-2:]
            self._current_key = b" ".join(new_key_elments)
        return self._current_key

    def fragment(self):
        return self._fragment

    def values_from(self, key):
        return bson.loads(self.db.get(key))["values"] 

    def random_value_from(self, key):
        return choice(self.values_from(key))

    def random_value_from_random(self, keys):
        return self.random_value_from(choice(keys))