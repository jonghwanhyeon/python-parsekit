import re

from . import Failure, Parser, Success


def literal(text):
    @Parser
    def literal_parser(stream, pos):
        if stream.startswith(text, pos):
            return Success(pos, pos + len(text), text)
        else:
            return Failure(pos, text)

    return literal_parser


def regex(pattern, flags=0):
    compiled = re.compile(pattern, flags)

    @Parser
    def regex_parser(stream, pos):
        match = compiled.match(stream, pos)
        if match:
            return Success(pos, match.end(0), match.group(0))
        else:
            return Failure(pos, pattern)

    return regex_parser
