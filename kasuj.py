import numpy as np

sentence = "aa bbb ccc dd www"


def split(sentence):
    words = sentence.split()
    for i in range(1, len(words)):
        yield " ".join(words[0:i]), " ".join(words[i:])


for x, y in split(sentence):
    print(x, " - ", y)
