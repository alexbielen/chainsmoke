"""



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


def railroad_it(func):
    """
    Creates a railroadable type (Either, Maybe).

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
