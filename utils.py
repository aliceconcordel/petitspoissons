from random import sample, randint

CONSONANTS = set("bcdfghjklmnpqrstvwxyz")
VOWELS = set("aeiou")


def random_name():
    name = ""
    n = randint(1, 4)
    for i in range(n):
        cons = sample(CONSONANTS, 1)[0]
        vow = sample(VOWELS, 1)[0]
        name +=  cons + vow
        if randint(0, 1):
            other_vow = sample(VOWELS, 1)[0]
            if vow != other_vow:
                name += other_vow
    if randint(0, 1):
        name += sample(CONSONANTS, 1)[0]
    return name.capitalize()