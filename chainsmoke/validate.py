"""
Utilities for validating inputs to functions in a non-disruptive way.


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
import typing


class ChainSmokeValidationError(Exception):
    pass


def is_instance_of(obj, type_annotation):
    """
    Replacement for Python's isinstance. This checks the object's type annotation
    against types derived from typing.
    :param obj: any object with type annotations
    :param type_annotation: any type annotation from Python's typing module
    :return:
    """
    pass


def validate_it(func):
    """
    Validate that the parameters have the correct types according to the type annotations.

    :param func: function to be decorated
    :param __meta: the original meta data about the original function; only used by the integration module
    :return: decorated function
    """
    types = func.__annotations__
    func_name = func.__name__

    # since varnames is read-only we sometimes have to use a different attribute
    try:
        param_names = func.overridden_varnames
    except AttributeError:
        args_spec = inspect.getargs(func.__code__)
        param_names = args_spec.args

    def validate_inner(*args, **kwargs):
        if not types:
            raise ChainSmokeValidationError("{func_name} does not have type annotations".format(func_name=func_name))

        if not kwargs and len(args) != len(param_names):
            raise ChainSmokeValidationError(
                "{func_name} cannot be properly validated by Chainsmoke. "
                "This is likely because it is using a default keyword argument".format(func_name=func_name))

        if not kwargs:
            names_and_values = zip(param_names, args)
        else:
            keyword_args = []
            for name in param_names:
                val = kwargs.get(name)
                if val:
                    keyword_args.append(val)

            names_and_values = zip(param_names, args + tuple(keyword_args))

        for name, value in names_and_values:
            t = types[name]

            if not isinstance(value, t):
                bad_type = type(value)
                error_string = "{func_name} expects type {expected_type} for arg {arg_name} " \
                               "but received value {value} with type of {value_type}"
                error_string = error_string.format(func_name=func_name,
                                                   expected_type=t,
                                                   arg_name=name,
                                                   value=value,
                                                   value_type=bad_type)
                raise TypeError(error_string)

        # check the type of the return as well
        return_type = types['return']
        result = func(*args, **kwargs)

        if not isinstance(result, return_type):
            bad_return_type = type(result)
            error_string = "{func_name} has return type {expected_type} but is returning value {value} of type {value_type}"
            error_string = error_string.format(func_name=func_name,
                                               expected_type=return_type,
                                               value=result,
                                               value_type=bad_return_type)
            raise TypeError(error_string)

        return result

    return validate_inner
