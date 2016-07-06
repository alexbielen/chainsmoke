from functools import reduce

from chainsmoke import either

either = either


def chain(*args, **kwargs):
    """
    Calls a chain of functions.
    :param args: functions you want called in a chain
    :return: result
    """
    if kwargs.get('wrap_with'):
        pass

    result = reduce((lambda x, y: y(x)), args)
    return result


def wrap_funcs(wrapping_func, func_list):
    wrapped_funcs = map(wrapping_func, func_list)
    return wrapped_funcs
