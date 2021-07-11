"""
Small utility functions.
"""


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)

        return s[start:end]
    except ValueError:
        return ""
