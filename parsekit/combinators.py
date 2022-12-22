import sys
from typing import Any, Callable, Optional

from parsekit import Failure, Parser, Success
from parsekit.typing import Result
from parsekit.utils import stringify


def then(*parsers: Parser) -> Parser:
    @Parser
    def then_parser(stream: str, pos: int) -> Result:
        start = pos

        for parser in parsers:
            result = parser(stream, pos)
            if not result:
                return result  # -> Failure

            pos = result.end
        return Success(start, pos, result.value)

    return then_parser


def skip(*parsers: Parser) -> Parser:
    @Parser
    def skip_parser(stream: str, pos: int) -> Result:
        start = pos

        first_result = None
        for parser in parsers:
            result = parser(stream, pos)
            if not result:
                return result  # -> Failure

            if first_result is None:
                first_result = result

            pos = result.end
        return Success(start, pos, first_result.value)

    return skip_parser


def sequence(*parsers: Parser) -> Parser:
    @Parser
    def sequence_parser(stream: str, pos: int) -> Result:
        start = pos

        values = []
        for parser in parsers:
            result = parser(stream, pos)
            if not result:
                return result  # -> Failure

            pos = result.end
            values.append(result.value)
        return Success(start, pos, values)

    return sequence_parser


def either(*parsers: Parser) -> Parser:
    @Parser
    def either_parser(stream: str, pos: int) -> Result:
        for parser in parsers:
            result = parser(stream, pos)
            if result:
                return result
        return result  # -> Failure

    return either_parser


def optional(parser: Parser, default=None) -> Parser:
    @Parser
    def optional_parser(stream: str, pos: int) -> Result:
        result = parser(stream, pos)
        if result:
            return result
        return Success(pos, pos, default)

    return optional_parser


def optional_sequence(*parsers: Parser, default: Optional[Any] = None, at_least: int = 0) -> Parser:
    @Parser
    def optional_sequence_parser(stream: str, pos: int) -> Result:
        start = pos

        count = 0
        values = []
        for parser in parsers:
            result = parser(stream, pos)
            if not result:
                values.append(default)
                continue

            pos = result.end
            count += 1
            values.append(result.value)

        if count >= at_least:
            return Success(start, pos, values)
        else:
            return Failure(start, None)

    return optional_sequence_parser


def times(parser: Parser, minimum: int, *args) -> Parser:
    maximum = args[0] if args else minimum
    if maximum is None:
        maximum = sys.maxsize

    @Parser
    def times_parser(stream: str, pos: int) -> Result:
        start = pos

        count = 0
        values = []
        while count < maximum:  # maximum
            result = parser(stream, pos)
            if not result:
                break

            pos = result.end
            count += 1
            values.append(result.value)

        if count < minimum:  # minimum
            return result  # -> Failure

        return Success(start, pos, values)

    return times_parser


def lookahead(parser: Parser) -> Parser:
    @Parser
    def lookahead_parser(stream: str, pos: int) -> Result:
        result = parser(stream, pos)
        if result:
            return Success(pos, pos, result.value)
        else:
            return result

    return lookahead_parser


def transform(parser: Parser, function: Callable[[Any], Any]) -> Parser:
    @Parser
    def transform_parser(stream: str, pos: int) -> Result:
        result = parser(stream, pos)
        if result:
            return Success(pos, result.end, function(result.value))
        else:
            return result  # Failure

    return transform_parser


def negate(parser: Parser) -> Parser:
    @Parser
    def negate_parser(stream: str, pos: int) -> Result:
        result = parser(stream, pos)
        if result:
            return Failure(pos, "Not {}".format(repr(result.value)))
        else:
            return Success(pos, pos, None)

    return negate_parser


def combine(parser: Parser) -> Parser:
    return transform(parser, lambda items: "".join(stringify(items)))
