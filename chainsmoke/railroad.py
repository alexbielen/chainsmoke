"""
Types and utilities for Railroad-oriented programming.

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


class Either(object):
    """
    Either allows you to chain computations that have either a Good status or an Error status.
    """

    def __init__(self, value):
        self.value = value


class Good(Either):
    """
    Use for cases where everything went OK.
    """
    pass


class Error(Either):
    """
    Use for cases where there is an error.
    """
    pass


class Maybe(object):
    """
    Maybe allows you to chain computations that have result in a Just value or a Nothing
    """

    def __init__(self, value):
        self.value = value


class Just(Maybe):
    pass


class Nothing(Maybe):
    pass


def railroad_it(railroad_type, debug=False):
    """
    Creates a railroad-able function; that is a function in which the error handling is abstracted into
    a computational context either or maybe.
    :param railroad_type:
    :param debug:
    :return:
    """
    def decorator(func):
        exceptions = []
        if railroad_type == Either:
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
                        if debug:
                            raise e
                        else:
                            return Error(e)

            result = check_type_of_either

        elif railroad_type == Maybe:
            def check_type_of_maybe(maybe):
                if isinstance(maybe, Nothing):
                    return Nothing
                else:
                    if not isinstance(maybe, Just):
                        value = maybe
                    else:
                        value = maybe.value
                    try:
                        return Just(func(value))
                    except Exception:
                        if debug:
                            func(value)
                        else:
                            return Nothing

            result = check_type_of_maybe

        else:
            raise TypeError("{railroad_type} is not a valid railroad type; try Either or Maybe.".format(railroad_type))

        return result

    return decorator
