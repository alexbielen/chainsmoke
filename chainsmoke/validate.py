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


def validate_it(func):
    """
    Validate that the parameters have the correct types according to the type annotations.

    :param func:
    :return:
    """
    types = func.__annotations__
    param_names = func.__code__.co_varnames

    # :todo make this work for kwargs as well
    def inner(*args, **kwargs):
        names_and_values = zip(param_names, args)

        for name, value in names_and_values:
            t = types[name]
            if not isinstance(value, t):
                bad_type = type(value)
                func_name = func.__name__
                error_string = "{func_name} expects type {expected_type} for arg {arg_name} " \
                               "but received value {value} with type of {value_type}"
                error_string.format(func_name=func_name,
                                    expected_type=t,
                                    arg_name=name,
                                    value=value,
                                    value_type=bad_type)
                raise TypeError(error_string)

        return func(args, kwargs)

    return inner

