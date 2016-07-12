# Chainsmoke
[![Build Status](https://travis-ci.org/bielenah/chainsmoke.svg?branch=master)](https://travis-ci.org/bielenah/chainsmoke)


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
"valid_email returned result 7"
```
So, now we have an addition function that logs its inputs and outputs. Cool, but not that cool. What's next?




