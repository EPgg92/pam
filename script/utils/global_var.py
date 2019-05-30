#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Initialisation of all globals varaibles."""

import os

PATH_GLOBAL_MODULE = os.path.realpath(__file__)
PATH_UTILS = os.path.dirname(PATH_GLOBAL_MODULE)
PATH_SCRIPT = os.path.dirname(PATH_UTILS)
PATH_PAM = os.path.dirname(PATH_SCRIPT)
PATH_CONF = os.path.join(PATH_PAM, 'config')
PATH_FORMS = os.path.join(PATH_CONF, 'forms')

DICT_SPECIAL_SYLL = {}
DICT_SPECIAL_TYPE = {}
DICT_CONST = {}

VOWEL = {}
EXEPTION = {}
CONSONNANT = {}
IER = {}

LIST_ATONE = []

DICT_CESURE = {
    8: [3, 4, 5],
    9: [3, 4, 5, 6],
    10: [3, 4, 5, 6, 7],
    11: [3, 4, 5, 6, 7, 8],
    12: [3, 4, 5, 6, 7, 8, 9],
    13: [3, 4, 5, 6, 7, 8, 9, 10],
    14: [3, 4, 5, 6, 7, 8, 9, 10, 11]
}

METRICS = 0
