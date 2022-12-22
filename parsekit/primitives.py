import re

from parsekit import Failure, Parser, Success

whitespace_pattern = re.compile(r"[ \t]+")


def consume_whitespace(stream, pos):
    match = whitespace_pattern.match(stream, pos)
    if match is None:
        return pos

    return match.end(0)


def literal(text):
    @Parser
    def literal_parser(stream, pos):
        pos = consume_whitespace(stream, pos)

        if stream.startswith(text, pos):
            return Success(pos, pos + len(text), text)
        else:
            return Failure(pos, text)

    return literal_parser


def regex(pattern, flags=0):
    compiled = re.compile(pattern, flags)

    @Parser
    def regex_parser(stream, pos):
        pos = consume_whitespace(stream, pos)

        match = compiled.match(stream, pos)
        if match:
            return Success(pos, match.end(0), match.group(0))
        else:
            return Failure(pos, pattern)

    return regex_parser
