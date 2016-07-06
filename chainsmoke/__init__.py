from functools import reduce
from typing import Callable


def wrap_funcs(wrapping_func, func_list):
    """
    :param wrapping_func:  Function to wrap with
    :param func_list: List of functions to wrap
    :return: List of wrapped functions.
    """
    wrapped_funcs = []

    for func in func_list:
        if isinstance(func, Callable):
            wrapped_funcs.append(wrapping_func(func))
        else:
            wrapped_funcs.append(func)

    return wrapped_funcs


def chain(*args, **kwargs):
    """
    Returns result of a chained computation. The first argument is treated as a value.

    Optionally pass in a higher order function with the 'wrap_with' keyword argument.

    :param args: functions you want called in a chain
    :return: result of the chain of functions
    """
    wrapping_func = kwargs.get('wrap_with')

    if wrapping_func:
        args = list(wrap_funcs(wrapping_func, args))

    result = reduce((lambda x, y: y(x)), args)
    return result


def chain_as_func(*args, **kwargs):
    """
    Returns function representing a chain of functions that is ready to be called with
    a value.

    Optionally pass in a higher order function with the 'wrap_with' keyword argument.

    :param args: functions you want called in a chain
    :return: result of the chain of functions
    """
    wrapping_func = kwargs.get('wrap_with')

    if wrapping_func:
        args = list(wrap_funcs(wrapping_func, args))

    def inner(value):
        result = reduce((lambda x, y: y(x)), (value,) + args)
        return result

    return inner
