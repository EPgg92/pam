#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Function that generates different filename accordingly to the timestamp."""

from time import gmtime, strftime


def get_now(format_timestamp=True):
    """Return a string of the actual timestamp.

    :param format_timestamp: boolean value to determine format of output
    :type format_timestamp: bool
    :return: string of a timestamp.
    :rtype: str
    """
    if format_timestamp:
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return strftime("%Y.%m.%d.%H.%M.%S", gmtime())
