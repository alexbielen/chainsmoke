# Chainsmoke

Chainsmoke is a collection of abstractions for chains of functions that strives to be simple, practical and well-documented.

Look below for an overly-didactic example:

## Either

```python
from either import chainable_either, call_chain

@chainable_either
def add_2_to_either(either):
    return either + 2


@chainable_either
def add_3_to_either(either):
    return either + 3


@chainable_either
def add_4_to_either(either):
    return either + 4


def test_that_call_chain_returns_15_when_value_is_good():
    result = call_chain(add_2_to_either(6), add_3_to_either, add_4_to_either)
    assert result.value == 15


def test_that_call_chain_returns_not_a_number_when_value_is_error():
    result = call_chain(add_2_to_either("abc"), add_3_to_either, add_4_to_either)
    assert isinstance(result.value, TypeError)
    
test_that_add_chain_returns_15_when_value_is_good()
test_that_add_chain_returns_not_a_number_when_value_is_error()
```
