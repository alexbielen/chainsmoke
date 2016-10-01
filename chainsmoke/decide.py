"""
Types and utilities for working with binary decision trees.

Adapted from Chanan Zupnick's decisionTree.js

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

from collections import namedtuple
from typing import Any, Callable, Union

Result = namedtuple('Result', ['value', 'path'])


class Decision(object):
    """
    Represents a binary choice node.
    """

    def __init__(self, name: str, predicate: Callable[[Any], bool], false_next: DecisionType, true_next: DecisionType):
        """
        :param name: Name of the decision
        :param predicate: A 1-arity function that returns
        :param false_next:
        :param true_next:
        """
        self.name = name
        self.predicate = predicate
        self.false_next = false_next
        self.true_next = true_next

    def next(self, data, path=''):
        if not path:
            path = self.name + " -> "
        else:
            path = path + self.name + " -> "

        if self.predicate(data):
            result = self.true_next
        else:
            result = self.false_next

        return result.next(data, path=path)


class Action(object):
    def __init__(self, name: str, action: Callable[[Any], Any]):
        self.name = name
        self.action = action

    def next(self, data: Any, path: str) -> Result:
        result = self.action(data)
        return Result(value=result, path=path + self.name)


DecisionType = Union[Decision, Action]
