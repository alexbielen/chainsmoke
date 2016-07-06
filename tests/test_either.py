"""
Tests for the common library functions.
"""

from chainsmoke.either import chainable_either
from chainsmoke import chain, chain_as_func


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
    func_chain = [
        add_3_to_either,
        add_4_to_either
    ]
    result = chain_as_func(*func_chain)(add_2_to_either(6))
    assert result.value == 15


def test_that_call_chain_returns_not_a_number_when_value_is_error():
    func_chain = [
        add_2_to_either("abc"),
        add_3_to_either,
        add_4_to_either
    ]
    result = chain(*func_chain)
    assert isinstance(result.value, TypeError)
