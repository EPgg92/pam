#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main class which contain where all tags are checked."""

import re
import utils.global_var as gv
from utils.textual import Textual
from utils.word import Word


class Verse(Textual):
    """Class Verse whish call all other classes of the pam."""

    def __init__(self, verse, num_verse):
        """Create an objet type Verse."""
        super().__init__(verse)
        self.num_verse = num_verse
        self.words = self.splitwords()
        self.__e_posttonique()
        # self.__ents_posttonique('es', 'ës')
        # self.__ents_posttonique('ent', 'ënt')
        self.words = [Word(w) for w in self.words]
        self.__e_last()
        self.update()
        self.cesure = set()
        if gv.METRICS > 1:
            self.__set_dict_syll()
            self.__find_cesure()
        self.str_cesure = '/'.join(sorted(self.cesure))

    def update(self):
        """Update all attributes of the Verse."""
        [w.get_list_type() for w in self.words]
        self.verse_syll = [w.list_syll for w in self.words]
        self.verse_type = [w.list_type for w in self.words]
        self.str_verse_syll = " ".join([w.str_word_syll for w in self.words])
        self.str_verse_type = "|".join([w.str_word_type for w in self.words])
        self.meter = len(
            [y for x in self.words for y in x.word_type if y > -1])
        if self.words != [] and self.words[-1].list_type[-1] == 0:
            self.meter -= 1

    def __set_dict_syll(self):
        self.dict_syll = {}
        counted = 0
        for i, word in enumerate(self.words):
            for j, syll in enumerate(word.list_syll):
                if syll.type != -1:
                    counted += 1
                    self.dict_syll[counted] = (syll, word, i, j)
                else:
                    self.dict_syll[-counted] = (syll, word, i, j)

    def __find_cesure(self):
        if gv.METRICS in gv.DICT_CESURE:
            position = gv.DICT_CESURE[gv.METRICS]
            for pos in position:
                if pos in self.dict_syll:
                    syll, _, pos_word, pos_syll = self.dict_syll[pos]
                    if self.meter == gv.METRICS:
                        if syll.is_last:
                            if syll.type == 2:
                                self.cesure.add('{}ma'.format(pos))
                            elif syll.type == 0 and self.words[pos_word].list_syll[pos_syll - 1].type == 2:
                                self.cesure.add('{}ly'.format(pos))
                            else:
                                self.cesure.add('{}NA'.format(pos))
                        elif syll.type == 2:
                            if self.words[pos_word].list_syll[pos_syll + 1].type == 0:
                                self.cesure.add('{}ej'.format(pos))
                            elif self.words[pos_word].list_syll[pos_syll + 1].type == -1:
                                self.cesure.add('{}épV'.format(pos))
                            else:
                                self.cesure.add('{}NA'.format(pos))
                        else:
                            self.cesure.add('{}NA'.format(pos))
                    elif self.meter == gv.METRICS + 1 and len(self.words[pos_word].list_syll) > pos_syll + 1:
                        if syll.type == 2 and self.words[pos_word].list_syll[pos_syll + 1].type == 0:
                            self.cesure.add('{}épC'.format(pos))
                        else:
                            self.cesure.add('{}NA'.format(pos))
                    else:
                        self.cesure.add('{}NA'.format(pos))
                else:
                    self.cesure.add('{}NA'.format(pos))

    def __e_last(self):
        if self.words != []:
            words = self.words
            if len(self.words[-1].list_syll) > 1 \
                    and re.search(r'e(nt|s)?$', words[-1].list_syll[-1].text) \
                    and words[-1].text not in gv.DICT_SPECIAL_TYPE:
                words[-1].list_syll[-1].set_type(0)
                words[-1].create_metrification()
            for i in range(len(words) - 1):
                if len(words[i].list_syll) > 1:
                    if re.search(r'e$', words[i].list_syll[-1].text):
                        if words[i + 1].list_syll[0].text[0] in gv.VOWEL:
                            words[i].list_syll[-1].set_type(-1)
                            words[i].create_metrification()
            self.words = words

    def __e_posttonique(self, ents='e', repl_ents='ë'):
        """Place [ë] at the end of word if necessary."""
        len_ents = len(ents)
        words = self.words
        for i, _ in enumerate(words):
            if i != len(words) - 1 and words[i][-len_ents:] == ents and \
                    words[i + 1][0] in gv.CONSONNANT:
                words[i] = '{}{}'.format(words[i][:-len_ents], repl_ents)
        self.words = words

    def __ents_posttonique(self, ents='e', repl_ents='ë'):
        """Place [ë] at the end of word if necessary."""
        len_ents = len(ents)
        words = self.words
        for i, _ in enumerate(words):
            if i != len(words) - 1:
                if words[i][-len_ents:] == ents:
                    words[i] = '{}{}'.format(words[i][:-len_ents], repl_ents)
        self.words = words
