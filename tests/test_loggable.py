"""
Unit tests for loggable.py

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

from unittest.mock import MagicMock, call
from functools import partial

from chainsmoke.log import log_it
from chainsmoke.util import chain


# some very simple functions
def simple_addition(x, y):
    return x + y

def simple_multiplication(x, y):
    return x * y


# set up a partial function with a name
add_two = partial(simple_addition, 2)
add_two.__name__ = 'add_two'

# and a partial function without
multiply_by_two = partial(simple_multiplication, 2)


def test_that_log_it_logs_inputi_and_output_correctly():
    mock_logger = MagicMock()
    result = chain(
        5,
        add_two,
        multiply_by_two,
        wrap_with=log_it(mock_logger)
    )

    mock_logger.assert_has_calls(
        [
            call('add_two called with args: (5,) and kwargs {}'),
            call('add_two returned result 7'),
            call('unknown function name; probably a lambda or partially applied function... '
                 'called with args: (7,) and kwargs {}'),
            call('unknown function name; probably a lambda or partially applied function... returned result 14')
        ])


def test_that_input_and_output_string_can_be_changed():
    mock_logger = MagicMock()
    result = chain(
        5,
        add_two,
        multiply_by_two,
        wrap_with=log_it(mock_logger,
                         input_string="{func_name}; {args}; {kwargs}",
                         output_string='{func_name}; {result}')
    )

    mock_logger.assert_has_calls(
        [
            call('add_two; (5,); {}'),
            call('add_two; 7'),
            call('unknown function name; probably a lambda or partially applied function...; (7,); {}'),
            call('unknown function name; probably a lambda or partially applied function...; 14')
        ])


def test_that_when_log_it_is_applied_it_returns_the_correct_value():
    mock_logger = MagicMock()
    result = chain(
        5,
        add_two,
        multiply_by_two,
        wrap_with=log_it(mock_logger)
    )

    assert result == 14
