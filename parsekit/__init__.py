from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, NamedTuple, Tuple, Union

if TYPE_CHECKING:
    from parsekit.typing import Result


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
    def __init__(self, parser: Parser):
        self.parser = parser

    def __call__(self, stream: str, pos: int = 0) -> Result:
        return self.parser(stream, pos)

    def search(self, stream: str, pos: int = 0) -> Optional[Success]:
        try:
            return next(self.finditer(stream, pos))
        except StopIteration:
            return None

    def finditer(self, stream: str, pos: int = 0) -> Iterable[Success]:
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

    def map(self, function: Callable[[Any], Parser]) -> Parser:
        return transform(self, function)

    def apply(self, function: Callable[[Any], Parser]) -> Parser:
        return transform(self, lambda value: function(*value))

    def __add__(self, other: Parser) -> Parser:
        return sequence(self, other)

    def __mul__(self, operand: Union[int, Tuple[int, int]]) -> Parser:
        if isinstance(operand, int):
            return times(self, operand)
        else:
            return times(self, *operand)

    def __or__(self, other: Parser) -> Parser:
        return either(self, other)

    def __lshift__(self, other: Parser) -> Parser:
        return skip(self, other)

    def __rshift__(self, other: Parser) -> Parser:
        return then(self, other)


from parsekit.combinators import *  # noqa
from parsekit.primitives import *  # noqa
