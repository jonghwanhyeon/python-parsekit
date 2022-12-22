import re

from parsekit import Failure, Parser, Success
from parsekit.typing import Result

whitespace_pattern = re.compile(r"[ \t]+")


def consume_whitespace(stream: str, pos: int) -> int:
    match = whitespace_pattern.match(stream, pos)
    if match is None:
        return pos

    return match.end(0)


def literal(text: str) -> Parser:
    @Parser
    def literal_parser(stream: str, pos: int) -> Result:
        pos = consume_whitespace(stream, pos)

        if stream.startswith(text, pos):
            return Success(pos, pos + len(text), text)
        else:
            return Failure(pos, text)

    return literal_parser


def regex(pattern: str, flags: int = 0) -> Parser:
    compiled = re.compile(pattern, flags)

    @Parser
    def regex_parser(stream: str, pos: int) -> Result:
        pos = consume_whitespace(stream, pos)

        match = compiled.match(stream, pos)
        if match:
            return Success(pos, match.end(0), match.group(0))
        else:
            return Failure(pos, pattern)

    return regex_parser
