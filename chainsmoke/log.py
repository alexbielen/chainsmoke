"""
Decorator and utilities for logging.

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

def log_it(logger, input_string=None, output_string=None):
    """
    Wraps a function in a logger.

    :param logger: Function that takes a string
    :param input_string: An optional interpolated string for logging the input; needs to have {func_name}, {args} and
                         {kwargs} in the string.
    :param output_string: An optional interpolated stirng for logging the output; needs to have {func_name} and
                          {result} in the string.
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            if input_string:
                input_log_string = input_string
            else:
                input_log_string = "{func_name} called with args: {args} and kwargs {kwargs}"

            if output_string:
                output_log_string = output_string
            else:
                output_log_string = "{func_name} returned result {result}"

            try:
                function_name = function.__name__
            except AttributeError:
                function_name = 'unknown function name; probably a lambda or partially applied function...'

            logger(input_log_string.format( func_name=function_name, args=args, kwargs=kwargs))
            result = function(*args, **kwargs)
            logger(output_log_string.format(func_name=function_name, result=result))
            return result

        return wrapper

    return decorator


