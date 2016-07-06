from unittest.mock import MagicMock, call
from functools import partial

from chainsmoke.loggable import log_it
from chainsmoke import chain


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
