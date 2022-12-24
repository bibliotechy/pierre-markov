import sqlite3
from random import randrange, choices


class QuixSql():
    def __init__(self, db_path="./dq.db"):
        self.db = sqlite3.connect(db_path).cursor()
        self._fragment = self.random_key()
        self._current_key = self._fragment
        self._values = None

    
    def generate_fragment(self):
        while len(self.values()) > 0:
            next_word = self.values().pop(randrange(len(self.values())))[0]
            possible_next_fragment = " ".join([self.fragment(), next_word])
            if self.fragment_chapter(possible_next_fragment):
                self._fragment = possible_next_fragment
                self._current_key = None
                self._values = None
                self.generate_fragment()
            else:
                pass
        
        return({"fragment": self.fragment(), "chapter": self.fragment_chapter(self.fragment())[0]})

    def fragment_chapter(self, fragment):
        return self.db.execute("SELECT chapter from chapters where text like ?", (f"%{fragment}%",)).fetchone()

    def values(self):
        if self._values is None:
            self._values = self.values_from(self.current_key())
        return self._values

    def current_key(self):
        if self._current_key is None:
            new_key_elements = self.fragment().split(' ')[-2:]
            self._current_key = " ".join(new_key_elements)
        return self._current_key

    def random_key(self, db=None):
        _db = db if db else self.db
        return _db.execute("SELECT key from ENGLISH ORDER BY RANDOM() LIMIT 1").fetchone()[0]

    def fragment(self):
        return self._fragment

    def values_from(self, key):
        return self.db.execute("SELECT value, count from ENGLISH where key=?", (key,)).fetchall() 

    def random_value_from(self, key):
        words_and_counts = self.values_from(key)
        return choices([b[0] for b in words_and_counts], weights=[b[1] for b in words_and_counts], k=1)[0]

    def random_value_from_random(self, keys):
        return self.random_value_from(self.random_key())
