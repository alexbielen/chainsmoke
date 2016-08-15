# Chainsmoke
[![Build Status](https://travis-ci.org/alexbielen/chainsmoke.svg?branch=master)](https://travis-ci.org/alexbielen/chainsmoke)

Chainsmoke is a collection of tools for chains of functions. It strives to be simple, practical and well-documented.


##Logging


Here's one type of problem that Chainsmoke aims to fix:

```python
#addition.py

import logging

def add_two_numbers(x, y):
    logging.debug("[*] add_two_numbers passed arguments x: {x} and y: {y}".format(x=x, y=y))
    result = x + y
    logging.debug("[*] add_two_numbers return result: {result}".format(result=result))
    return result

add_two_numbers(3, 4)
```
We want to add some debug logging, but we've unfortunately created some noise that obscures the logic.
Here's a quick fix from Chainsmoke.log:

```python
import logging
from chainsmoke.log import log_it

@log_it(logging.debug)
def add_two_numbers(x, y):
    return x + y

add_two_numbers(3, 4)
```
This will give us the same functionality as the above example, but the logic remains clear and noise-free.
In fact, we've been able to simplify the function slightly because we do not need the intermediary `result` variable.

The `log_it` decorator will log the name of the function, any arguments or keyword arguments, and the results
of the computation.

For the above example the logger will create the following strings:

Input logging:
```python
"add_two_numbers called with args: (3, 4,) and kwargs {}"
```

Output logging:
```python
"add_two_numbers returned result 7"
```
So, now we have an function `add_two_numbers` that logs its inputs and outputs. Cool, but not that cool. What's next?

##Chain

Let's set up our first chain of functions.

```python
from chainsmoke.chain import chain


def add_two(x):
    return x + 2


def multiply_by_two(x):
    return x * 2


def divide_by_two(x):
    return x / 2


result = chain(
    5,
    add_two,
    multiply_by_two,
    divide_by_two
)
# result: 7.0
```

The `chain` function allows you to easily pass the result of one function to the next function. The first argument to chain
will be treated like a value, much like how `5` is in this example.

All of the functions in the chain must have an arity of one; put another way the functions in the chain must have exactly
one argument. In the real world you'll often have functions with more than one argument so when using Chainsmoke you'll find
`functools.partial` comes in handy. Here's the same example using more general functions and `functools.partial`:

```python
from chainsmoke.chain import chain
from functools import partial


def addition(x, y):
    return x + y

def multiplication(x, y):
    return x * y

def division(x, y): # not used...
    return x // y

add_two = partial(addition, 2)
multiply_by_two = partial(multiplication, 2)
divide_by_two = partial(multiplication, .5)

result = chain(
    5,
    add_two,
    multiply_by_two,
    divide_by_two
)
```
As you can see, `functools.partial` allows you to 'bake-in' a parameter to a function; this is referred to as
'partial application' or 'currying'. Notice how we had to implement `divide_by_two` as multiplication by .5?
That's due to the behavior of `functools.partial` -- specifically that it replaces the arguments in order.
This means that because division is not associative you can't curry the function and get the same behavior.

There are two utilities in Chainsmoke that offer a solution to this problem; `swap` and `reorder`.

`swap` is a simple function that swaps the order of the arguments. 

```python
from chainsmoke.functools import swap

def division(x, y):
    return x // y
    
swapped_division = swap(division)

swapped_division(2, 4) # 2
```

Let's use swap on the division function in the same chain of simple arithmetic functions from before:

```python
from functools import partial

from chainsmoke.chain import chain
from chainsmoke.functools import swap

def addition(x, y):
    return x + y

def multiplication(x, y):
    return x * y

def division(x, y):
    return x // y

add_two = partial(addition, 2)
multiply_by_two = partial(multiplication, 2)
divide_by_two = partial(swap(division), 2)

result = chain(
    5,
    add_two,
    multiply_by_two,
    divide_by_two
)
```
## wrap_with

`chain` has a keyword argument `wrap_with` that takes a decorator function and applies it to all of the functions in the
 chain.

 So instead of writing this...

```python
from functools import partial

from chainsmoke.chain import chain
from chainsmoke.functools import swap
from chainsmoke.log import log_it


@log_it(print)
def addition(x, y):
    return x + y

@log_it(print)
def multiplication(x, y):
    return x * y

@log_it(print)
def division(x, y):
    return x // y

add_two = partial(addition, 2)
multiply_by_two = partial(multiplication, 2)
divide_by_two = partial(swap(division), 2)

result = chain(
    5,
    add_two,
    multiply_by_two,
    divide_by_two
)
```
... you can write this ...

```python
from functools import partial

from chainsmoke.chain import chain
from chainsmoke.functools import swap
from chainsmoke.log import log_it


def addition(x, y):
    return x + y

def multiplication(x, y):
    return x * y

def division(x, y):
    return x // y

add_two = partial(addition, 2)
multiply_by_two = partial(multiplication, 2)
divide_by_two = partial(swap(division), 2)

result = chain(
    5,
    add_two,
    multiply_by_two,
    divide_by_two,
    wrap_with=log_it(print)

)
```















