from nose.tools import assert_true, assert_equals
from build import contains_negative_forms, find_affirmative_and_negative_forms, bmd, lcp, lwstrip


def lwstrip_test():
    word = 'taktaktraktor'

    expected = 'traktor'
    actual = lwstrip(word, 'tak')

    assert_equals(expected, actual)


def contains_negative_forms_test():
    words = ['równoczesny', 'nierównoczesny', 'równoczesnymi', 'równoczesnych', 'równoczesnym', 'równoczesnemu',
             'równoczesnego', 'równoczesną', 'równoczesnej', 'równoczesne', 'równoczesna', 'równocześni',
              'równocześnie', 'nierównoczesnymi', 'nierównoczesnych', 'nierównoczesnym', 'nierównoczesnemu',
              'nierównoczesnego', 'nierównoczesną', 'nierównoczesnej', 'nierównoczesne', 'nierównoczesna',
              'nierównocześni', 'nierównocześnie'
            ]

    assert_true(contains_negative_forms(words))

"""
Testy generowania form twierdzacych i przeczacych z listy odmian slowa

Zestaw slow, oczekiwane formy twierdzace i oczekiwane formy przeczace
"""
data_test_suite = [
    # Pojedyncze 'nie'
    (['palony', 'niepalony'], ['palony'], ['niepalony']),
    (['obżarty', 'nieobżarty', 'nieobżartej'], ['obżarty'], ['nieobżarty', 'nieobżartej']),
    # Podwojne 'nie'
    (['niewolniczy', 'nieniewolniczy'], ['niewolniczy'], ['nieniewolniczy']),
    (['niewieści', 'nieniewieścimi', 'nieniewieści', 'niewieścimi'], ['niewieści', 'niewieścimi'], ['nieniewieści', 'nieniewieścimi']), 
    # Potrojne 'nie'
    (['nieniecki', 'nienieniecki'], ['nieniecki'], ['nienieniecki']),
    # 'nie' w srodku
    (['dudnieniową', 'dudnieniowe', 'niedudnieniową', 'niedudnieniowe'], ['dudnieniową', 'dudnieniowe'], ['niedudnieniową', 'niedudnieniowe']),
    # 'nie' na koncu
    (['detoksykacyjnie', 'niedetoksykacyjnie'], ['detoksykacyjnie'], ['niedetoksykacyjnie']),
    # 'nie' i jego litery na poczatku
    (['iniektorowy', 'nieiniektorowy'], ['iniektorowy'], ['nieiniektorowy']),
]

def check_corectness_of_generated_forms(words, expected_affirmative, expected_negative):
    actual_affirmative, actual_negative = find_affirmative_and_negative_forms(words)

    assert_equals(sorted(expected_affirmative), sorted(actual_affirmative))
    assert_equals(sorted(expected_negative), sorted(actual_negative))

def find_affirmative_and_negative_forms_tests_generator():
    for words, expected_affirmative, expected_negative in data_test_suite:
        yield check_corectness_of_generated_forms, words, expected_affirmative, expected_negative


def lcp_test():
    actual = lcp(['nieżółciopędnie'])
    expected = 'nieżółciopędnie'

    assert_equals(actual, expected)

def test_bmd_with_lcp():
    lines = [' '.join(piece[0]) for piece in data_test_suite]

    all_words = []
    for piece in data_test_suite:
        all_words += piece[0]
    
    actual = bmd(lines, lcp)

    assert_equals(sorted(actual.keys()), sorted(all_words))
