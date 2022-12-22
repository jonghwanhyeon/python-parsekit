import sys

from parsekit import Failure, Parser, Success
from parsekit.utils import stringify


def then(*parsers):
    @Parser
    def then_parser(stream, pos):
        start = pos

        for parser in parsers:
            result = parser(stream, pos)
            if not result:
                return result  # -> Failure

            pos = result.end
        return Success(start, pos, result.value)

    return then_parser


def skip(*parsers):
    @Parser
    def skip_parser(stream, pos):
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


def sequence(*parsers):
    @Parser
    def sequence_parser(stream, pos):
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


def either(*parsers):
    @Parser
    def either_parser(stream, pos):
        for parser in parsers:
            result = parser(stream, pos)
            if result:
                return result
        return result  # -> Failure

    return either_parser


def optional(parser, default=None):
    @Parser
    def optional_parser(stream, pos):
        result = parser(stream, pos)
        if result:
            return result
        return Success(pos, pos, default)

    return optional_parser


def optional_sequence(*parsers, default=None, at_least=0):
    @Parser
    def optional_sequence_parser(stream, pos):
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


def times(parser, minimum, *args):
    maximum = args[0] if args else minimum
    if maximum is None:
        maximum = sys.maxsize

    @Parser
    def times_parser(stream, pos):
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


def lookahead(parser):
    @Parser
    def lookahead_parser(stream, pos):
        result = parser(stream, pos)
        if result:
            return Success(pos, pos, result.value)
        else:
            return result

    return lookahead_parser


def transform(parser, function):
    @Parser
    def transform_parser(stream, pos):
        result = parser(stream, pos)
        if result:
            return Success(pos, result.end, function(result.value))
        else:
            return result  # Failure

    return transform_parser


def negate(parser):
    @Parser
    def negate_parser(stream, pos):
        result = parser(stream, pos)
        if result:
            return Failure(pos, "Not {}".format(repr(result.value)))
        else:
            return Success(pos, pos, None)

    return negate_parser


def combine(parser):
    return transform(parser, lambda items: "".join(stringify(items)))
