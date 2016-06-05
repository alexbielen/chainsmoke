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


class EitherGood(_Either):
    """
    Use for cases where everything went OK.
    """
    pass


class EitherError(_Either):
    """
    Use for cases where there is an error.
    """
    pass


def chainable_either(func):
    """
    Decorator to make
    :param func:
    :return:
    """

    def check_type_of_either(either):
        if isinstance(either, EitherError):
            return EitherError(either.value)
        else:
            return EitherGood(func(either))

    return check_type_of_either


def call_chain(*args):
    """
    Calls a chain of functions.
    :param args: functions you want called in a chain
    :return: result
    """
    result = reduce((lambda x, y: y(x)), args)
    return result
