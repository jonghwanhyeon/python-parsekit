from parsekit import *


def test_then():
    parser = then(
        string('let'),
        regex(r'\s+'),
        regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
    )
    assert parser('let foo') == Success(0, 7, 'foo')

    parser = then(
        parser,
        regex(r'\s*'),
        string('='),
        regex(r'\s*'),
        regex(r'[0-9]+'),
    )
    assert parser('let foo = 314159') == Success(0, 16, '314159')
    assert parser('let foo') == Failure(7, '=')


def test_skip():
    parser = skip(
        string('let'),
        regex(r'\s+'),
        regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
    )
    assert parser('let foo') == Success(0, 7, 'let')

    parser = skip(
        parser,
        regex(r'\s*'),
        string('='),
        regex(r'\s*'),
        regex(r'[0-9]+'),
    )
    assert parser('let foo = 314159') == Success(0, 16, 'let')


def test_sequence():
    parser = sequence(
        string('let'),
        regex(r'\s+'),
        regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
    )
    assert parser('let foo') == Success(0, 7, ['let', ' ', 'foo'])

    parser = sequence(
        parser,
        regex(r'\s*'),
        string('='),
        regex(r'\s*'),
        regex(r'[0-9]+'),
    )
    assert parser('let foo = 314159') \
        == Success(0, 16, [['let', ' ', 'foo'], ' ', '=', ' ', '314159'])


def test_either():
    parser = either(
        string('let'),
        string('var'),
        regex('int|float|double'),
    )
    assert parser('let') == Success(0, 3, 'let')
    assert parser('var') == Success(0, 3, 'var')
    assert parser('int') == Success(0, 3, 'int')
    assert parser('float') == Success(0, 5, 'float')

    parser = skip(
        parser,
        regex(r'\s+'),
        regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
    )
    assert parser('let foo') == Success(0, 7, 'let')
    assert parser('float foo') == Success(0, 9, 'float')


def test_optional():
    parser = then(
        string('let'),
        regex(r'\s+'),
        regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
        optional(
            then(
                regex(r'\s*'),
                string('='),
                regex(r'\s*'),
                regex(r'[0-9]+'),
            )
        )
    )
    assert parser('let foo') == Success(0, 7, None)
    assert parser('let foo =') == Success(0, 7, None)
    assert parser('let foo=314159') == Success(0, 14, '314159')
    assert parser('let foo = 314159') == Success(0, 16, '314159')


def test_optional_sequence():
    element = then(
        regex(r'\s*'),
        optional(string(',')),
        regex(r'\s*'),
        either(
            regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
            regex(r'[0-9]+'),
        )
    )

    parser = skip(
        then(
            string('('),
            optional_sequence(element, element, element),
        ),
        string(')'),
    )
    assert parser('()') == Success(0, 2, [None, None, None])
    assert parser('(1)') == Success(0, 3, ['1', None, None])
    assert parser('(1, 2, 3)') == Success(0, 9, ['1', '2', '3'])

    parser = skip(
        then(
            string('('),
            optional_sequence(element, element, element, at_least=2),
        ),
        string(')'),
    )
    assert parser('()') == Failure(1, None)
    assert parser('(1)') == Failure(1, None)
    assert parser('(1, 2, 3)') == Success(0, 9, ['1', '2', '3'])


def test_lookahead():
    parser = skip(
        then(
            string('let'),
            regex(r'\s+'),
            regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
        ),
        lookahead(
            sequence(
                regex(r'\s*'),
                string('='),
                regex(r'\s*'),
                regex(r'[0-9]+'),
            )
        )
    )

    assert parser('let foo = 314159') == Success(0, 7, 'foo')
    assert parser('let foo') == Failure(7, '=')
    assert parser('let foo =') == Failure(9, r'[0-9]+')


def test_transform():
    parser = then(
        string('let'),
        regex(r'\s+'),
        regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
        regex(r'\s*'),
        string('='),
        regex(r'\s*'),
        regex(r'[0-9]+'),
    ).map(int)
    assert parser('let foo = 314159') == Success(0, 16, 314159)
    assert parser('let foo') == Failure(7, '=')


def test_times():
    '''
        times(1)
        times(3)
        times(1, 3)
        times(3, 5)
        times(1, None)
        times(3, None)
    '''
    parser = then(
        string('let'),
        regex(r'\s+'),
        times(
            then(
                regex(r'\s*'),
                optional(string(',')),
                regex(r'\s*'),
                regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
            ),
            1
        )
    )
    assert parser('let foo') == Success(0, 7, ['foo'])
    assert parser('let foo, bar, baz') == Success(0, 7, ['foo'])

    parser = then(
        string('let'),
        regex(r'\s+'),
        times(
            then(
                regex(r'\s*'),
                optional(string(',')),
                regex(r'\s*'),
                regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
            ),
            3
        )
    )
    assert parser('let foo') == Failure(7, r'[A-Za-z\_][A-Za-z0-9\_]*')
    assert parser('let foo, bar, baz') == Success(0, 17, ['foo', 'bar', 'baz'])
    assert parser('let foo, bar, baz, qux, quux, corge') == Success(0, 17, ['foo', 'bar', 'baz'])

    parser = then(
        string('let'),
        regex(r'\s+'),
        times(
            then(
                regex(r'\s*'),
                optional(string(',')),
                regex(r'\s*'),
                regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
            ),
            1, 3
        )
    )
    assert parser('let foo') == Success(0, 7, ['foo'])
    assert parser('let foo, bar, baz') == Success(0, 17, ['foo', 'bar', 'baz'])
    assert parser('let foo, bar, baz, qux, quux, corge') == Success(0, 17, ['foo', 'bar', 'baz'])

    parser = then(
        string('let'),
        regex(r'\s+'),
        times(
            then(
                regex(r'\s*'),
                optional(string(',')),
                regex(r'\s*'),
                regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
            ),
            3, 5
        )
    )
    assert parser('let foo') == Failure(7, r'[A-Za-z\_][A-Za-z0-9\_]*')
    assert parser('let foo, bar, baz') == Success(0, 17, ['foo', 'bar', 'baz'])
    assert parser('let foo, bar, baz, qux, quux, corge') \
        == Success(0, 28, ['foo', 'bar', 'baz', 'qux', 'quux'])

    parser = then(
        string('let'),
        regex(r'\s+'),
        times(
            then(
                regex(r'\s*'),
                optional(string(',')),
                regex(r'\s*'),
                regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
            ),
            1, None
        )
    )
    assert parser('let foo') == Success(0, 7, ['foo'])
    assert parser('let foo, bar, baz') == Success(0, 17, ['foo', 'bar', 'baz'])

    parser = then(
        string('let'),
        regex(r'\s+'),
        times(
            then(
                regex(r'\s*'),
                optional(string(',')),
                regex(r'\s*'),
                regex(r'[A-Za-z\_][A-Za-z0-9\_]*'),
            ),
            3, None
        )
    )
    assert parser('let foo') == Failure(7, r'[A-Za-z\_][A-Za-z0-9\_]*')
    assert parser('let foo, bar, baz') == Success(0, 17, ['foo', 'bar', 'baz'])
    assert parser('let foo, bar, baz, qux, quux, corge') \
        == Success(0, 35, ['foo', 'bar', 'baz', 'qux', 'quux', 'corge'])
