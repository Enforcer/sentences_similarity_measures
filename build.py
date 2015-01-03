import logging
import traceback
import time
import pickle


FORMAT = '%(asctime)-15s %(levelname)s:%(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger('pldictstem')
log.setLevel(logging.DEBUG)


def lwstrip(word, what):
    while word.startswith(what):
        word = word[3:]
    return word


def find_affirmative_and_negative_forms(words):
    count = words[0].count('nie') + 1 - lwstrip(words[0], 'nie').count('nie')

    affirmative_form = lambda x: not x.startswith('nie' * count)
    negative_form = lambda x: x.startswith('nie' * count)

    return list(filter(affirmative_form, words)), list(filter(negative_form, words))

def contains_negative_forms(words):
    return 'nie' + words[0] in words

def stem_safely(mega_dict, words, stem_selector):
    try:
        stem = stem_selector(words)
        for word in words:
            mega_dict[word] = stem
    except:
        print(words)
        print(traceback.format_exc())
        return False

def bmd(data, stem_selector):
    """
    Builds mega-dict
    """
    mega_dict = {}
    i = 0

    for line in data:
        words = line.split(' ')
        if len(words) > 1:
            if contains_negative_forms(words):
                affirmatives, negatives = find_affirmative_and_negative_forms(words)

                stem_safely(mega_dict, affirmatives, stem_selector)
                stem_safely(mega_dict, negatives, stem_selector)
            else:
                stem_safely(mega_dict, words, stem_selector)
        i += 1

    return mega_dict


def shortest(words):
    words.sort(key=len)
    return words[0]

def lcp(words_input):
    words = words_input[:]
    assert len(words) > 0

    if len(words) == 1:
        return words[0]

    prefix = []
    idx = 0
    words.sort(key=lambda s: len(s))
    first_word = words.pop(0)

    while idx < len(first_word) and \
            all([word[idx] == first_word[idx] for word in words]):
        prefix.append(first_word[idx])
        idx += 1

    if len(prefix) == 0:
        raise Exception('Pusty prefix! %r' % words)
    elif len(prefix) < 2:
        log.warning('Stem jest krotki: %r dla slow: %r, zwracam: %s', ''.join(prefix), words, shortest(words))
        return shortest(words)

    return ''.join(prefix)


def first_word(words_input):
    return words_input[0]


if __name__ == '__main__':
    with open('polish_words.txt') as f:
        lines = [line.strip() for line in f.readlines()]


    start = time.time()
    print('Building dict...', end='')
    mega_dict = bmd(lines, lcp)
    print('DONE (%r s).' % (time.time() - start))

    f = open('mega_dict.ppo', 'bw')
    pickle.dump(mega_dict, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    print('dumped')
