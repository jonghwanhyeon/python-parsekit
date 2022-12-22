from collections import namedtuple
from typing import Any, NamedTuple


class Success(NamedTuple):
    start: int
    end: int
    value: Any

    def __bool__(self):
        return True


class Failure(NamedTuple):
    pos: int
    expected: str

    def __bool__(self):
        return False


class Parser:
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, stream, pos=0):
        return self.parser(stream, pos)

    def search(self, stream, pos=0):
        try:
            return next(self.finditer(stream, pos))
        except StopIteration:
            return None

    def finditer(self, stream, pos=0):
        while pos < len(stream):
            result = self(stream, pos)
            if result:
                if result.end > pos:
                    yield result
                    pos = result.end
                else:  # empty match
                    pos += 1
            else:  # -> Failure
                pos += 1

    def map(self, function):
        return transform(self, function)

    def apply(self, function):
        return transform(self, lambda value: function(*value))

    def __add__(self, other):
        return sequence(self, other)

    def __mul__(self, operand):
        if isinstance(operand, int):
            return times(self, operand)
        else:
            return times(self, *operand)

    def __or__(self, other):
        return either(self, other)

    def __lshift__(self, other):
        return skip(self, other)

    def __rshift__(self, other):
        return then(self, other)


from parsekit.combinators import *  # noqa
from parsekit.primitives import *  # noqa
