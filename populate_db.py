import bson
import plyvel
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='Text file to load into db', required=True)
parser.add_argument('-d','--db', help='DB file to write to', required=True)

args = parser.parse_args()

text = open(args.file).read().encode("utf8")
words = text.split(b" ")

db = plyvel.DB(args.db, create_if_missing=True)
#
# dq = open("./don-quixote.txt").read().encode("utf8")
# source = open("./source.txt").read().encode("utf8")
# dqwords = dq.split(b" ")
# source_words = source.split(b" ")
# db = plyvel.DB('./dqdb', create_if_missing=True)

#db.Put(b' '.join([one,two]), bson.dumps({"values" : [words[2].decode('utf8'),]}))

w1, w2 = words.pop(0), words.pop(0)
for word in words:
    key = b' '.join([w1,w2])
    if db.get(key):
        value = db.get(key)
        array_of_vals = bson.loads(value)["values"]
        if word not in array_of_vals:
          array_of_vals.append(word)
    else:
        array_of_vals = [word]
    db.put(key, bson.dumps({"values": array_of_vals}))
    w1, w2 = w2, word
