# Chainsmoke
[![Build Status](https://travis-ci.org/bielenah/chainsmoke.svg?branch=master)](https://travis-ci.org/bielenah/chainsmoke)


Chainsmoke is a collection of tools for chains of functions. It strives to be simple, practical and well-documented.

Here's one type of problem that Chainsmoke aims to fix:

```python
#sign_up.py

import logging
import re

def valid_email(email):
    logging.debug("[*] Function valid_email received {email} as input".format(email=email))
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        result = False
    else:
        result = True

    logging.debug("[*] Function valid_email returned {result} for input {input}".format(result=result, email=email)

    return result
```
We want to add some debug logging, but we've unfortunately created some noise that obscures the logic.
Here's a quick fix from Chainsmoke.log:

```python

from chainsmoke.log import log_it


@log_it(logging.debug)
def valid_email(email):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        result = False
    else:
        result = True


    return result

valid_email("alex@bielen.com")
```
This will give us the same functionality as the above example, but the logic remains clear and noise-free.
The `log_it` decorator will log the name of the function, any arguments or keyword arguments, and the results
of the computation.

For the above example the logger will create the following strings:

Input logging:
```python
"valid_email called with args: ("alex@bielen.com",) and kwargs {}"
```

Output logging:
```python
"valid_email returned result True"
```
So, we have a logger and an email validation function. Cool, but not that cool. What's next?

After validating the email, we would like to then send a message to the email.
The initial requirements look like this:

1) Validate the email

2) Send a message to the email

Here's a first attempt:

```python
from chainsmoke.log import log_it
from db.models import Email
from email import send_message

@log_it(logging.debug)
def valid_email(email):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        result = False
    else:
        result = True

    return result

@log_it(logging.debug)
def send_message_to_email(email):
    result = send_message(email, "Welcome to my WEBSITE!") # {'success': Bool}
    return result

@log_it(logging.debug)
def send_message_to_validated_email(email):
    # validate the email
    if not valid_email(email):
        return {'success': False}
    else:
        send_email_response = send_message_to_email(email)

    return send_email_response
```

Okay, we've created two new functions: `send_message_to_email` and an
integration function (a function that calls our two helper functions) named 
`send_message_to_validated_email`. We've also added our logger to our two new functions. 


















