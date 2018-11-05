from parsekit import *


def test_string():
    text = 'abcdef'

    assert string('a')(text) == Success(0, 1, 'a')
    assert string('abc')(text) == Success(0, 3, 'abc')
    assert string('def')(text) == Failure(0, 'def')

    assert string('b')(text, 1) == Success(1, 2, 'b')
    assert string('bcd')(text, 1) == Success(1, 4, 'bcd')
    assert string('def')(text, 1) == Failure(1, 'def')


def test_regex():
    text = 'howdy!'

    assert regex(r'h')(text) == Success(0, 1, 'h')
    assert regex(r'how')(text) == Success(0, 3, 'how')
    assert regex(r'h[aeiou]w')(text) == Success(0, 3, 'how')
    assert regex(r'how[aeiou]')(text) == Failure(0, 'how[aeiou]')

    assert regex(r'o')(text, 1) == Success(1, 2, 'o')
    assert regex(r'owd')(text, 1) == Success(1, 4, 'owd')
    assert regex(r'[aeiou]wd')(text, 1) == Success(1, 4, 'owd')
    assert regex(r'ow[aeiou]')(text, 1) == Failure(1, 'ow[aeiou]')

    assert regex(r'how[a-z]+\!')(text) == Success(0, 6, 'howdy!')
    assert regex(r'[0-9]*')(text) == Success(0, 0, '')
