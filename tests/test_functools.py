"""
Unit tests for functools.py

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

from chainsmoke.functools import swap, reorder


def test_that_swap_correctly_swaps_arguments():
    def divide_two_numbers(x, y):
        return x / y

    swapped_divide = swap(divide_two_numbers)
    assert swapped_divide(2, 4) == 2


def test_that_swap_raises_useful_exception_when_passed_wrong_number_of_arguments():
    def add_three(x, y, z):
        return x + y + z

    with pytest.raises(AssertionError) as exception_info:
        swap(add_three)

    assert exception_info.value.msg == "swap expects a two argument function; add_three has 3 argument(s)"


def test_that_swap_raises_useful_exception_when_passed_lambda_with_wrong_number_of_args():
    with pytest.raises(AssertionError) as exception_info:
        swap(lambda x: x * x)

    assert exception_info.value.msg == "swap expects a two argument function; <lambda> has 1 argument(s)"


def test_that_reorder_correctly_reorders_arguments():
    def add_two_and_divide(x, y, z):
        return (x + y) / z

    reordered_func = reorder(add_two_and_divide, (2, 0, 1))

    assert reordered_func(2, 4, 4) == 4




