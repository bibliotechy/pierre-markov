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


def make_quixote(db, seed):
    local_seed = seed
    sentence = " ".join(local_seed)
    next_word = choice(db.get(sentence, [None]))
    while next_word:
        sentence += " " + next_word
        if dq[:len(sentence)] != sentence:
            break
        local_seed.pop(0)
        local_seed.append(next_word)
        next_word = choice(db.get(" ".join(local_seed), [None]))
    print sentence
    if dq == sentence:
        print "IT IS "


def load_db_to_number_depth(file="don-quixote.txt", number=2):
    db = defaultdict(list)

    words = dq.split(" ")

    variables = create_variable_sequence(number, words[:number])
    keys = variables.keys()
    print variables

    for word in words[number:][:10]:
        print "word: " + word
        newkey = " ".join([variables[key] for key in sorted(keys)])
        print "newkey: " + newkey
        db[newkey].append(word)
        for i in range(1, number):
            variables["donquixote" + str(i)] = variables["donquixote" + str(i+1)]
        variables["donquixote" + str(number)] = word
    return db


def create_variable_sequence(number, source_array):
    vars_dict = {}
    for i in range(number):
        var = "donquixote" + str(i + 1)
        vars_dict[var] = source_array[i]
    return vars_dict

