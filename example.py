from parsekit import *

KOREAN_DIGIT_TO_INTEGER = dict(zip("영일이삼사오육칠팔구", range(0, 10)))


def to_int(token):
    try:
        return int(token)
    except ValueError:
        return KOREAN_DIGIT_TO_INTEGER[token]


def at(position):
    def fn(digit):
        return digit * (10**position)

    return fn


DIGIT = regex(r"[1-9일이삼사오육칠팔구]").map(to_int)

multiplier_1e0 = DIGIT
multiplier_1e1 = optional(DIGIT, default=1).map(at(1)) << literal("십")
multiplier_1e2 = optional(DIGIT, default=1).map(at(2)) << literal("백")
multiplier_1e3 = optional(DIGIT, default=1).map(at(3)) << literal("천")

multiplier_numerals = regex(r"[1-9][0-9]{1,3}").map(to_int)

multiplier = either(
    multiplier_numerals,
    optional_sequence(multiplier_1e3, multiplier_1e2, multiplier_1e1, multiplier_1e0, default=0, at_least=1).map(sum),
)

number_1e0 = multiplier
number_1e4 = optional(multiplier, default=1).map(at(4)) << literal("만")
number_1e8 = multiplier.map(at(8)) << literal("억")
number_1e12 = multiplier.map(at(12)) << literal("조")
number_1e16 = multiplier.map(at(16)) << literal("경")
number_1e20 = multiplier.map(at(20)) << literal("해")

number_numerals = regex(r"[1-9][0-9]{4,}").map(to_int)

number = either(
    number_numerals,
    optional_sequence(
        number_1e20, number_1e16, number_1e12, number_1e8, number_1e4, number_1e0, default=0, at_least=1
    ).map(sum),
)

assert number("314159265358979323846264").value == 314159265358979323846264
assert number("삼천백사십일해오천9백이십6경오천삼백5십8조구천7백구십삼억이천3백8십사만육천이백6십4").value == 314159265358979323846264
