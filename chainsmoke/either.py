"""
Monads for error handling.
"""
from functools import reduce


class _Either(object):
    """
    Either allows you to chain computations that have either a Good status or an Error status.
    """

    def __init__(self, value):
        self.value = value


class Good(_Either):
    """
    Use for cases where everything went OK.
    """
    pass


class Error(_Either):
    """
    Use for cases where there is an error.
    """
    pass


def chainable_either(func):
    """
    """

    def check_type_of_either(either):
        if isinstance(either, Error):
            return Error(either.value)
        else:
            if not isinstance(either, Good):
                value = either
            else:
                value = either.value
            try:
                return Good(func(value))
            except Exception as e:
                return Error(e)

    return check_type_of_either


