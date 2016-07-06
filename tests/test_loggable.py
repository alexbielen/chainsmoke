from chainsmoke.loggable import log_it
from chainsmoke import chain
from functools import partial


def simple_addition(x, y):
    return x + y


def simple_multiplication(x, y):
    return x * y



add_two = partial(simple_addition, 2)
add_two.__name__ = 'add_two'

multiply_by_two = partial(simple_multiplication, 2)
multiply_by_two.__name__ = 'multiply_by_two'


def wrap_funcs(wrapping_func, func_list):
    wrapped_funcs = map(wrapping_func, func_list)
    return wrapped_funcs

wrapped = list(wrap_funcs(log_it(print), [add_two, multiply_by_two]))

result = chain(
    5,
    wrapped[0],
    wrapped[1]
)

print(result)









