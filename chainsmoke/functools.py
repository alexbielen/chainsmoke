"""
Utilities for manipulating functions.

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
import inspect
from typing import Callable

from chainsmoke.validate import validate_it


class ChainSmokeFunctoolsError(Exception):
    pass


@validate_it
def swap(func: Callable) -> Callable:
    """
    Swaps the arguments to a function.
    :param func: A 2-arity function
    :return: A 2-arity function with swapped parameters.
    """
    num_args = len(func.__code__.co_varnames)

    if num_args != 2:
        try:
            name = func.__name__
        except AttributeError:
            name = 'anonymous function'

        raise AssertionError("swap expects a two argument function; {name} has {len} argument(s)".format(name=name,
                                                                                                         len=num_args))

    def inner(x, y):
        return func(y, x)

    return inner


@validate_it
def reorder(func: Callable, reordered_args: tuple) -> Callable:
    """
    Reorders arguments to a function according to tuple of integers
    :param func: function of n-arity
    :param reordered_args: a tuple of unique integers
    :return: function of n-arity with reordered args
    """
    name = func.__name__
    args_spec = inspect.getargs(func.__code__)
    num_positional_args = len(args_spec.args)

    if len(reordered_args) > num_positional_args:
        raise ChainSmokeFunctoolsError(
            "functools.reorder received too many args in the reordered_args tuple; "
            "make sure the length of the tuple matches the number of positional arguments in {func_name}".format(
                func_name=name))

    if len(reordered_args) < num_positional_args:
        raise ChainSmokeFunctoolsError(
            "functools.reorder received too few args in the reordered_args tuple; "
            "make sure the length of the tuple matches the number of positional arguments in {func_name}".format(
                func_name=name))

    def inner(*args, **kwargs):

        correct_order = sorted(zip(args, reordered_args), key=lambda x: x[1])
        correct_args = (arg[0] for arg in correct_order)
        return func(*correct_args, **kwargs)

    return inner
