"""
Test that decorators integrate well together.

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
from unittest.mock import MagicMock, call

from chainsmoke.chain import combine
from chainsmoke.log import log_it
from chainsmoke.validate import validate_it


def test_that_validate_and_log_work_together():
    mock_logger = MagicMock()
    validate_and_log = combine(log_it(mock_logger), validate_it)

    @validate_and_log
    def add_three(x: int, y: int, z: int) -> int:
        return x + y + z

    add_three(1, 2, 3)
    mock_logger.assert_has_calls(
        [
            call('add_three called with args: (1, 2, 3) and kwargs {}'),
        ])


def test_that_validate_and_log_work_together_passed_in_any_order():
    mock_logger = MagicMock()
    validate_and_log = combine(validate_it, log_it(mock_logger))

    @validate_and_log
    def add_four(w: int, x: int, y: int, z: int) -> int:
        return sum([w, x, y, z])

    add_four(1, 2, 3, 4)
    mock_logger.assert_has_calls(
        [
            call('add_four called with args: (1, 2, 3, 4) and kwargs {}'),
        ])


def test_that_validate_works_when_used_with_log_through_combine():
    mock_logger = MagicMock()
    validate_and_log = combine(log_it(mock_logger), validate_it)

    @validate_and_log
    def add_three(x: int, y: int, z: int) -> int:
        return x + y + z

    with pytest.raises(TypeError) as exception_info:
        add_three(1, 2, '3')

    assert exception_info.value.args[
               0] == "add_three expects type <class 'int'> for arg z but received value 3 with type of <class 'str'>"
