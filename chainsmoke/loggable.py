"""
Decorator for logging.
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
    def real_decorator(function):
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

    return real_decorator
