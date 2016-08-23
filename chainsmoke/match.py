"""
Pattern matching decorator.

Based on a couple of implementations that I've seen out there including Guido's multimethods
and this really helpful gist by Chad Selph: https://gist.github.com/chadselph/1320421

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


class ChainsmokePatternMatchError(Exception):
    pass


class _Otherwise:
    """
    The default pattern.
    """
    pass


otherwise = _Otherwise()


def __convert_if_list(pattern):
    if isinstance(pattern, list):
        key = 'list-' + str(hash(tuple(pattern)))
    else:
        key = pattern

    return key


class Match:
    def __init__(self):
        self.funcs = {}

    def find_func(self, params):
        """
        Finds the function given the patterns
        :param params:
        :return:
        """
        match = self.funcs.get(params, self.funcs[(otherwise,)])
        return match

    def __call__(self, *patterns):
        """
        Takes the patterns that are passed into the decorator and stores the associated
        function in the function repository.
        :param patterns: The patterns to be matched against
        :return: Callable
        """


        # defines the decorator that adds the patterns to the function lookup
        def decorator(func):
            func_args = inspect.getargs(func.__code__)
            func_name = func.__name__

            if len(patterns) != len(func_args.args):
                raise ChainsmokePatternMatchError(
                    "Number of patterns needs to equal number of args in {func_name}".format(func_name=func_name))

            self.funcs[patterns] = func

            # define a function that gives a result from the matched function
            def inner(*inner_args):
                if not self.funcs.get((otherwise,)):
                    raise ChainsmokePatternMatchError(
                        "Incomplete pattern match for {func_name}; try adding an 'otherwise' case".format(
                            func_name=func_name))

                matched_function = self.find_func(inner_args)
                return matched_function(*inner_args)

            return inner

        return decorator



