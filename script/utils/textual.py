#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
from nltk.tokenize import RegexpTokenizer


class Textual():
    """Abstract class to manage all text class of the pam."""

    def __init__(self, text):
        """Create a Textual object."""
        self.text = text

    def __str__(self):
        """Return a string-form of the dict of variable of this object."""
        return pprint.pformat(vars(self))

    def splitwords(self):
        """Tokenise vers and remove ponctuation of it."""
        return RegexpTokenizer(r'\w+').tokenize(
            self.text.lower().replace('  ', ' ').replace('’', '').replace('\'',
                                                                          ' '))
