#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""To manage syllable with class."""

from utils.textual import Textual


class Syllable(Textual):
    """Atomic class container for syllable with default values."""

    type = 1
    is_last = False

    type_syll = {
        -1: ('@'),
        0: ('é'),
        1: ('a'),
        2: ('t'),
        3: ('ae')
    }

    def set_is_last(self):
        """Change values of is_last."""
        self.is_last = True

    def set_text(self, new_text):
        """Change values of text by new_text value."""
        self.text = new_text

    def set_type(self, new_type):
        """Change values of type by new_type value."""
        self.type = new_type
