"""
Tests for the common library functions.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
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
