"""
Tests for the decision tree library.

MIT License

Copyright (c) 2016 Alex Bielen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from chainsmoke.decide import Decision, Action


class DriversLicense(object):
    def __init__(self, age, name, state, valid):
        self.age = age
        self.name = name
        self.state = state
        self.valid = valid


# test data
alex_drivers_license = DriversLicense(29, 'Alex', 'Ohio', False)
denis_drivers_license = DriversLicense(22, 'Denis', 'New York', True)
dave_drivers_license = DriversLicense(20, 'Dave', 'Maryland', True)


# helper functions
def check_out_of_state(driver_license):
    if driver_license.state != 'New York':
        return driver_license.valid
    else:
        return True


# decision tree
do_not_allow_in_bar = Action('do not allow in bar', lambda x: 'Get out of the bar, {name}'.format(name=x.name))
allow_into_bar = Action('allow in bar', lambda x: 'Welcome to the bar, {name}'.format(name=x.name))
check_that_out_of_state_id_is_valid = Decision(
    'check that out of state id is valid',
    check_out_of_state,
    false_next=do_not_allow_in_bar,
    true_next=allow_into_bar
)
check_over_21 = Decision(
    'check that person is over 21',
    lambda x: x.age >= 21,
    false_next=do_not_allow_in_bar,
    true_next=check_that_out_of_state_id_is_valid
)


def test_that_decision_tree_behaves_properly():
    alex_result = check_over_21.next(alex_drivers_license)
    dave_result = check_over_21.next(dave_drivers_license)
    denis_result = check_over_21.next(denis_drivers_license)

    assert alex_result.value == 'Get out of the bar, Alex'
    assert dave_result.value == 'Get out of the bar, Dave'
    assert denis_result.value == 'Welcome to the bar, Denis'

    assert alex_result.path == 'check that person is over 21 -> check that out of state id is valid -> do not allow in bar'
    assert dave_result.path == 'check that person is over 21 -> do not allow in bar'
    assert denis_result.path == 'check that person is over 21 -> check that out of state id is valid -> allow in bar'
