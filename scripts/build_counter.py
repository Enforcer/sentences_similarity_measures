import os
import sys
from collections import Counter
import imp
import pickle

assert len(sys.argv) == 3, 'Podaj skrot jezyka i nazwe pliku'

#clean_stop_signs
#in_stop_words
stoppers = imp.load_source('stoppers', './langs/{0}/stoppers.py'.format(sys.argv[1]))

#stem
stemmer = imp.load_source('stemmer', './langs/{0}/stemmer.py'.format(sys.argv[1]))

c = Counter()

is_clean = lambda x: x and not stoppers.in_stop_words(x) and stoppers.clean_stop_signs(x)

with open(sys.argv[2]) as f:
    for line in f:
        c.update([stemmer.stem(word) for word in
                    [stoppers.clean_stop_signs(a) for a in line.split() if is_clean(a)]
                 if stemmer.stem(word)])

f = open('counter.ppo', 'wb')
pickle.dump(c, f, pickle.HIGHEST_PROTOCOL)
f.close()
print('Counter built')
print(c)
