from nltk.util import ngrams
from itertools import combinations_with_replacement
from itertools import product


def ngrams_from_file(path, num_of_chars, ngram):

    file = open(path, 'r', encoding='utf-8')
    text = file.read(num_of_chars)
    NG = list(ngrams(text, ngram))

    res = []
    for i in NG:
        res.append(''.join(i))
    return res

def ngrams_from_text(text, ngram):

    NG = list(ngrams(text, ngram))

    res = []
    for i in NG:
        res.append(''.join(i))
    return res


def make_alf(num):
    alf = ''
    for j in range(32, 219):
        alf += chr(j)
    alf += '\t\n'
    alf += chr(8211)
    for i in range(1040, 1106):
        alf += chr(i)


    # samples = combinations_with_replacement(alf, num)
    # samples = itertools.
    sam = []
    for i in product(alf, repeat=num):
        sam.append(''.join(i))
    return sam

def make_nul_vec(num):
    vec = []
    for i in range(0, num):
        vec.append(0)
    return vec

def one_hot_vec(nul_vec, pos):
    nul_vec[pos] = 1
    return nul_vec

def label_vec(num_names, pos):
    l_vec = make_nul_vec(num_names)
    l_vec[pos] = 1
    return l_vec