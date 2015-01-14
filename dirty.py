import sys
import logging
log = logging.getLogger('pldictstem')
log.setLevel(logging.INFO)
ch = logging.StreamHandler( sys.__stdout__ )
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

import langs.pl.stoppers as stoppers
import langs.pl.stemmer as stemmer
import langs.pl.occ as occ

def tokenize(sentence, leave_proper_names=False):
    assert len(sentence) > 0
    sentence = stoppers.clean_stop_signs(sentence)
    words = sentence.split(' ')
    assert len(words) > 0
    words[0] = words[0].lower()
    return [w for w in
            [stemmer.stem(word, leave_proper_names=leave_proper_names) for word in words if not stoppers.in_stop_words(word)]
            if w]

print(sys.argv)

for sentence in sys.argv[1:]:
    print([(t, occ.occurencies[t], occ.frequency(t)) for t in tokenize(sentence)])
    print(tokenize(sentence))

from rieck import sim
print(sim(sys.argv[1], sys.argv[2]))
