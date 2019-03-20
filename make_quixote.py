import bson
import plyvel
from random import choice
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d','--db', help='DB file to write to', required=True)
args = parser.parse_args()


db = plyvel.DB(args.db, create_if_missing=True)
dq = open("./don-quixote-tosed.txt").read().encode("utf8").split(b" ")


def make_quixote():

    keys = [key for key, value in db.iterator()]
    newdq = [b'El', b'ingenioso']
    print(b'El ingenioso'.decode('utf8'), end=' ', flush=True)
    next_word = random_value_from(b' '.join(newdq))
    while next_word is not None and dq != newdq :
        if dq[len(newdq)] == next_word:
            print(next_word.decode('utf8'), end=' ', flush=True)
            last_newdq = newdq[-1]
            newdq.append(next_word)
            next_word = random_value_from(b' '.join([last_newdq, next_word]))
        else:
            next_word = random_value_from_random(keys)


def random_value_from(key):
    return choice(bson.loads(db.get(key))["values"])

def random_value_from_random(keys):
    return random_value_from(choice(keys))

if __name__ == "__main__":
    make_quixote()
