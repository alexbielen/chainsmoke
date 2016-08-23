"""
Unit tests for match.py

Copyright (C) 2016  Alex Hendrie Bielen

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
import pytest

from chainsmoke.match import Match, otherwise, ChainsmokePatternMatchError

easy_match = Match()
bad_match = Match()
factorial_match = Match()
sum_tuple_match = Match()


@easy_match(1)
def easy(n):
    return 'a'


@easy_match(2)
def easy(n):
    return 'b'


@easy_match(otherwise)
def easy(n):
    return 'c'


@bad_match(1)
def no_otherwise(n):
    return 0


@factorial_match(0)
def factorial(n):
    return 1


@factorial_match(otherwise)
def factorial(n):
    return n * factorial(n - 1)


def test_that_match_works_with_simple_functions():
    assert easy(1) == 'a'
    assert easy(2) == 'b'
    assert easy(3) == 'c'
    assert easy(4) == 'c'


def test_that_match_raises_an_exception_when_there_is_not_an_otherwise_case():
    with pytest.raises(ChainsmokePatternMatchError) as exception_info:
        no_otherwise(1)

    assert exception_info.value.args[0] == "Incomplete pattern match for no_otherwise; try adding an 'otherwise' case"


def test_that_match_works_with_recursive_factorial():
    assert factorial(5) == 120

