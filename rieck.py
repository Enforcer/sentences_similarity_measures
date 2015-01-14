
import langs.pl.stoppers as stoppers
import langs.pl.occ as occ

import math

def corpus_dependant_weighting(w):
    """
    w - stem
    """
    N = 190379
    freq = occ.frequency(w) # stem
    return math.log(N, 2) - math.log(freq, 2) + 1

def length_dependant_weighting(w):
    """
    w - stem
    """
    DECAY = 0.7
    return DECAY**(-len(w))

def position_dependant_weighting(w, x):
    """
    w - stem
    x - sentence
    """
    W = lambda position, sentence: (position + 1) / len(sentence)
    indices = [i for i, v in enumerate(x) if v == "w"]
    return sum([W(position, x) for position in indices])

def phi(w, x):
    CDP_FACTOR = 0.5
    LDP_FACTOR = 0.2
    PDW_FACTOR = 0.3

    W = lambda word, sentence: CDP_FACTOR * corpus_dependant_weighting(word) + \
        LDP_FACTOR * length_dependant_weighting(word) + \
        PDW_FACTOR * position_dependant_weighting(word, sentence)

    return x.count(w) * W(w, x)

def get_feature_vector(x):
    """
    x - sentence
    """
    unique_tokens = set(x)
    return [
        phi(w, x) 
        for w in unique_tokens
    ]

_COEFFICIENT_MEASURES = {}

def coefficient_measure(fun):
    _COEFFICIENT_MEASURES[fun.__name__] = fun
    return fun
"""
COEFFICIENCY MEASURES
"""
@coefficient_measure
def jaccard(a, b, c):
    return a / (a + b + c)

@coefficient_measure
def simpson(a, b ,c):
    return a / min(a + b, a + c)

@coefficient_measure
def braun_blanquet(a, b, c):
    return a / max(a + b, a + c)

@coefficient_measure
def czekanowski_sorensen_dice(a, b, c):
    return 2*a / (2*a + b + c)

@coefficient_measure
def kulczynski_one(a, b, c):
    return a / (b + c)

@coefficient_measure
def kulczynski_two(a, b, c):
    return (a / (a + b) + a / (a + c)) / 2

@coefficient_measure
def otsuka_ochiai(a, b, c):
    return a / math.sqrt((a + b)*(a + c))

@coefficient_measure
def sokal_sneath(a, b, c):
    return a / (a + 2 * (b + c))

"""
END OF COEFFICIENCY MEASURES
"""
def jensen_shannon(x, y):
    #H = lambda x, y: 
    def H(x, y):
        print('H: ', x, y)
        return x * math.log(2 * x / (x + y), 10) + y * math.log(2 * y / (x + y), 10)
    common_words = set(x) & set(y)
    result = sum([
        H(phi(w, x), phi(w, y))
        for w in common_words
    ])
    print('Jensen-Shannon', result)

def sim(x, y, verbose=True):
    sum_of_words = set(x + y)
    a = sum([min(phi(w, x), phi(w, y)) for w in sum_of_words])
    b = sum([phi(w, x) - min(phi(w, x), phi(w, y)) for w in sum_of_words])
    c = sum([phi(w, y) - min(phi(w, x), phi(w, y)) for w in sum_of_words])

    #results = []
    #for name, measure in _COEFFICIENT_MEASURES.items():
    #    if verbose:
    #        print(name, measure(a, b, c))
    return jaccard(a, b, c), czekanowski_sorensen_dice(a, b, c), braun_blanquet(a, b, c)


s1 = ['radoś', 'wyb', 'górs', 'wyciecz']
s2 = ['radoś', 'byśmy', 'wyb', 'górs', 'wyciecz']

#print(sim(s1, s2))
#jensen_shannon(s1, s2)


