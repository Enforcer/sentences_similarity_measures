import os
import sys
import pickle
import logging

log = logging.getLogger('pldictstem')

dict_path = ''

current_dir = os.path.dirname(os.path.abspath(__file__))
dict_path = os.path.join(current_dir, 'res', 'mega_dict.ppo')

f = open(dict_path, 'rb')
mega_dict = pickle.load(f)
f.close()

def stem(word, leave_proper_names=False):
    if not word or word.isdigit():
        return False

    try:
        return mega_dict[word.lower()]
    except KeyError:
        #log.warning('%s not in dict' % (word))
        return alternative_stemmer(word, leave_proper_names=leave_proper_names)


def own_name_detector(x, leave_proper_names=False):
    if not leave_proper_names and x[0] == x[0].upper():
        #log.warning('%s is suspected to be a proper name, ommiting..', x)
        return False
    else:
        return x

#alternative_stemmer = lambda x: x
alternative_stemmer = own_name_detector
