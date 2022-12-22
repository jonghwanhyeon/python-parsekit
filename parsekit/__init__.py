from collections import namedtuple


class Success(namedtuple("Success", ["start", "end", "value"])):
    def __bool__(self):
        return True


class Failure(namedtuple("Failure", ["pos", "expected"])):
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
        return seq(self, other)

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


from .combinators import *  # noqa
from .primitives import *  # noqa
