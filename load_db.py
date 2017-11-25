from collections import defaultdict
from random import choice

text_file="don-quixote.txt"
dq = open(text_file).read().decode("utf8")


def load_db_in_memory():

    db = defaultdict(list)

    words = dq.split(" ")

    w1, w2 = words.pop(0), words.pop(0)

    for word in words:
        db[w1 + " " + w2].append(word)
        w1, w2 = w2, word
    return db


def build_sentences(db, seed, sentence=""):
    return sentence + db[" ".join(seed)]


def make_quixote(db=None, seed=None, number=10):
    if not db:
        db = load_db_to_number_depth(number=number)
    if not seed:
        seed = dq[:(number * 50)].split(" ")[:number]
    local_seed = seed[:]
    count = 0
    pr = True
    sentence = " ".join(local_seed)
    next_word = choice(db.get(sentence, [None]))
    while next_word is not None:
        count += 1
        sentence += " " + next_word
        if dq[:len(sentence)] != sentence:
            print "LEN: " + str(len(sentence))
            print "SEED: "
            print local_seed
            print "SEED AS STRING: " + " ".join(local_seed)
            print count
            pr = False
            break
        local_seed.pop(0)
        local_seed.append(next_word)
        next_word = choice(db.get(" ".join(local_seed), None))
    if pr:
        print sentence
    if dq == sentence:
        print "IT IS "
    else:
        print ""
        print "LEN: " + str(len(sentence))
        print "SEED: "
        print local_seed
        print "SEED AS STRING: " + " ".join(local_seed)
        print count


def load_db_to_number_depth(number=2):
    db = defaultdict(list)

    words = dq.split(" ")
    current_seq = words[:number]

    for word in words[number:]:
        newkey = " ".join(current_seq)
        db[newkey].append(word)
        current_seq.pop(0)
        current_seq.append(word)
    return db
