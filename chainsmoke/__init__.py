"""
__init__.py

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
