"""
util.py

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
from functools import reduce, partial
from collections import namedtuple
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


def compose(*args, **kwargs):
    """
    Returns function representing a chain of functions that is ready to be called with
    a value.

    Optionally pass in a higher order function with the 'wrap_with' keyword argument.

    :param args: functions you want called in a chain
    :return: result of the chain of functions
    """
    wrapping_func = kwargs.get('wrap_with')

    if wrapping_func:
        args = wrap_funcs(wrapping_func, args)

    def compose_inner(value):
        result = reduce((lambda x, y: y(x)), [value] + list(args))
        return result

    return compose_inner


def combine(*args: Callable) -> Callable:
    """
    Combines and integrates decorator functions into a single function.

    1) The decorators in Chainsmoke are order-dependent. This function
    helps to abstract that order by ordering the desired decorators
    instead of having the user remember the order.

    2) Some decorators will lose functionality when used in combination. This
    function adds that functionality back by passing attributes of the original
    function into the decorators.

    :param args: Any number of chainsmoke decorator functions
    :return: A single decorator function with the functionality of the combined decorators
    """
    order = {
        'validate_it': 0,
        'log_it_decorator': 1
    }
    sorted_decorators = sorted(args, key=lambda x: order[x.__name__])

    def decorator(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        inner.__name__ = func.__name__
        inner.__annotations__ = func.__annotations__
        inner.overridden_varnames = func.__code__.co_varnames

        for dec in sorted_decorators:
            inner = dec(inner)
            inner.__name__ = func.__name__

        return inner

    return decorator
