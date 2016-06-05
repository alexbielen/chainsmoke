"""
Tests for the common library functions.
"""

from either import EitherError, EitherGood, chainable_either, call_chain


good = EitherGood(6)
bad = EitherError("NOT A NUMBER")


@chainable_either
def add_2_to_either(either):
    return either + 2


@chainable_either
def add_3_to_either(either):
    return either + 3


@chainable_either
def add_4_to_either(either):
    return either + 4


def test_that_call_chain_returns_15_when_value_is_good():
    result = call_chain(add_2_to_either(good), add_3_to_either, add_4_to_either)
    assert result.value == 15


def test_that_call_chain_returns_not_a_number_when_value_is_error():
    result = call_chain(add_2_to_either(bad), add_3_to_either, add_4_to_either)
    assert result.value == "NOT A NUMBER"
