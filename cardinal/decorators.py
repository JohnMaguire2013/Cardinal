from __future__ import absolute_import, print_function, division

import re
import functools

import six


_RETYPE = type(re.compile('foobar'))


def command(triggers):
    if isinstance(triggers, six.string_types):
        triggers = [triggers]

    if not isinstance(triggers, list):
        raise TypeError("Command must be a trigger string or list of triggers")

    def wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            return f(*args, **kwargs)

        inner.commands = triggers
        return inner

    return wrap


def regex(expression):
    if (not isinstance(expression, six.string_types) and
            not isinstance(expression, _RETYPE)):
        raise TypeError("Regular expression must be a string or regex type")

    def wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            return f(*args, **kwargs)

        inner.regex = expression
        return inner

    return wrap


def help(lines):
    # For backwards compatibility
    if isinstance(lines, six.string_types):
             lines = [lines]

    if not isinstance(lines, list):
        raise TypeError("Help must be a help string or list of help strings")

    def wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            return f(*args, **kwargs)

        # Create help list or prepend to it
        if not hasattr(inner, 'help'):
            inner.help = lines
        else:
            inner.help = lines + inner.help

        return inner

    return wrap


def event(triggers):
    if isinstance(triggers, six.string_types):
        triggers = [triggers]

    if not isinstance(triggers, list):
        raise TypeError("Event must be a trigger string or list of triggers")

    def wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            return f(*args, **kwargs)

        inner.events = triggers
        return inner

    return wrap
