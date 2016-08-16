"""
Unit tests for validate.py

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

from chainsmoke.validate import validate_it, ChainSmokeValidationError


def test_that_validate_it_raises_exception_if_types_are_incorrect():
    with pytest.raises(TypeError) as exception_info:
        @validate_it
        def add_two_numbers(x: int, y: int) -> int:
            return x + y

        add_two_numbers(2, 'A')

    assert exception_info.value.args[
               0] == "add_two_numbers expects type <class 'int'> for arg y " \
                     "but received value A with type of <class 'str'>"


def test_that_validate_it_works_with_keyword_arguments():
    @validate_it
    def add_two(x: int, y: int = 'A') -> int:
        return x + y

    with pytest.raises(TypeError) as exception_info:
        add_two(4, y='B')

    assert exception_info.value.args[
               0] == "add_two expects type <class 'int'> for arg y but received value B with type of <class 'str'>"


def test_that_validate_it_does_not_work_when_using_a_default_keyword_arg():
    @validate_it
    def add_two(x: int, y: int = 'A') -> int:
        return x + y

    with pytest.raises(ChainSmokeValidationError) as exception_info:
        add_two(2)

    assert exception_info.value.args[
               0] == 'add_two cannot be properly validated by Chainsmoke. ' \
                     'This is likely because it is using a default keyword argument'


def test_that_validate_it_raises_an_exception_when_function_does_not_have_type_annotations():
    @validate_it
    def add_two(x, y):
        return x + y

    with pytest.raises(ChainSmokeValidationError) as exception_info:
        add_two(2, 6)

    assert exception_info.value.args[0] == 'add_two does not have type annotations'


def test_that_validate_it_raise_an_exception_when_there_is_a_return_type_mismatch():
    @validate_it
    def add_two(x: int, y: int) -> int:
        return str(x + y)

    with pytest.raises(TypeError) as exception_info:
        add_two(4, 5)

    assert exception_info.value.args[
               0] == "add_two has return type <class 'int'> but is returning value 9 of type <class 'str'>"
