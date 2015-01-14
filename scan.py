
import langs.pl.stoppers as stoppers
import langs.pl.stemmer as stemmer
import langs.pl.occ as occ

from rieck import sim, s2

s2 = ['wyklucza', 'wspar', 'sprzę', 'oczekując', 'zamian', 'stw', 'sie', 'informacyjn', 'przyszłoś', 'pomoc', 'produkc', 'program', 'problem', 'lokaln']

is_clean = lambda x: x and not stoppers.in_stop_words(x) and stoppers.clean_stop_signs(x)
i = 0
j = 0
with open('/Users/spb/Projects/engineer/result.txt') as f:
    for line in f:
        sentences = line.split('.')
        for sentence in sentences:
            stemmed = ([stemmer.stem(word) for word in
                        [stoppers.clean_stop_signs(a) for a in sentence.split() if is_clean(a)]
                     if stemmer.stem(word)])
            if len(stemmed) > 2:
                res = sim(stemmed, s2)
                if any([a > 0.5 for a in res]):
                    print(stemmed, sim(stemmed, s2))
        i += len(sentences)
        j += 1
        if j % 1000 == 0:
            print('Przetworzono ', i, 'zdań')
    
    print('Przetworzono {0} zdań'.format(i))

