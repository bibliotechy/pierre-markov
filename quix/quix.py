import sqlite3
from random import randrange, choices


class QuixSql():
    def __init__(self, db_path="./dq.db"):
        self.db = sqlite3.connect(db_path).cursor()
        self._fragment = self.random_key()
        self._current_key = self._fragment
        self._values = None
        self._chapter = None
        self._final_fragment = False

    
    def generate_fragment(self):
        while (not self._final_fragment) and (len(self.values()) > 0):
            next_word = self.values().pop(randrange(len(self.values())))[0]
            possible_next_fragment = " ".join([self.fragment(), next_word])
            if self.fragment_chapter(possible_next_fragment):
                self._fragment = possible_next_fragment
                self._current_key = None
                self._values = None
                self.generate_fragment()
            else:
                pass
        self._final_fragment = True

        return {"fragment": self.fragment(), "chapter": self.fragment_chapter(self.fragment())[0]}

    def fragment_chapter(self, fragment):
        if self._chapter:
            return self.known_fragment_chapter(fragment)
        return self.not_yet_known_fragment_chapter(fragment)
    
    def not_yet_known_fragment_chapter(self, fragment):
        chapters =  self.db.execute("SELECT chapter from chapters where text like ?", (f"%{fragment}%",)).fetchall()
        if len(chapters) == 1:
            self._chapter = chapters[0][0] 
        return chapters[0] if chapters else None

    def known_fragment_chapter(self, fragment):
        chapter =  self.db.execute("SELECT chapter from chapters where text like ? and chapter=?", (f"%{fragment}%", self._chapter)).fetchone()
        return chapter

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
        key =  _db.execute("SELECT key from ENGLISH ORDER BY RANDOM() LIMIT 1").fetchone()[0]
        return key

    def fragment(self):
        return self._fragment

    def values_from(self, key):
        values = self.db.execute("SELECT value, count from ENGLISH where key=?", (key,)).fetchall()
        return values

    def random_value_from(self, key):
        words_and_counts = self.values_from(key)
        return choices([b[0] for b in words_and_counts], weights=[b[1] for b in words_and_counts], k=1)[0]

    def random_value_from_random(self, keys):
        return self.random_value_from(self.random_key())
