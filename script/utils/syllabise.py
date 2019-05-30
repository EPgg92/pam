#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Package of usefull functions to syllabise word in french.

This file needs a constants.yaml file containing:
    - a list named vowel containing your vowel
    - a list named consonnant containing your consonnant
    - a dictionnary named exeption containing as key some letters and as value
    a V or a C
"""
import re
import utils.global_var as gv


def list_letters_and_exceptions(word):
    """Return a transformed word split into letters and exeptions.

    :param word: a word
    :type word: str
    :return: list of letters and exeptions
    :rtype: list
    """
    letters_and_exceptions = []
    jump = 0
    for j in range(len(word)):
        if jump == 0:
            k = 0
            while True:
                if k != 0:
                    word_part = word[j:-k]
                else:
                    word_part = word[j:]
                if word_part in gv.EXEPTION:
                    jump = len(word_part) - 1
                    letters_and_exceptions.append(word_part)
                    break
                elif len(word_part) == 1:
                    letters_and_exceptions.append(word_part)
                    break
                elif word_part == '':
                    break
                k += 1
        else:
            jump -= 1
    return letters_and_exceptions


def transform_cv(list_let_exc):
    """Return a list of C and V using list of letters and exeptions.

    :param list_let_exc: list of letters and exeptions
    :type list_let_exc: list
    :return: list of C and V tags
    :rtype: list
    """
    return [gv.EXEPTION[let_exc] if let_exc in gv.EXEPTION else
            'V' if let_exc in gv.VOWEL else
            'C' if let_exc in gv.CONSONNANT else ""
            for let_exc in list_let_exc]


def get_syllabe_cv(list_cv):
    """Return list of grouped C and V tags using list of C and V tags.

    :param list_cv: list of C and V tags
    :type list_cv: list
    :return: list of grouped C and V tags
    :rtype: list
    """
    temp = [''.join(x) for x in re.findall(r'C*VC*', ''.join(list_cv))]
    syllabe_cv = []
    for i, pcv in enumerate(temp):
        if i != len(temp) - 1 and pcv[-1] == "C" and temp[i + 1][0] == "V":
            syllabe_cv.append(pcv[:-1])
            temp[i + 1] = "{}{}".format("C", temp[i + 1])
        else:
            syllabe_cv.append(pcv)
    return syllabe_cv


def syllabise_word(word):
    """Return list of syllabe of a word.

    :param word: a word
    :type word: str
    :return: list of syllabe
    :rtype: list()
    """
    list_let_exc = list_letters_and_exceptions(word)
    list_cv = transform_cv(list_let_exc)
    syllabe_cv = get_syllabe_cv(list_cv)
    syllabes = []
    for pcv in syllabe_cv:
        syll = []
        for _ in range(len(pcv)):
            syll.append(list_let_exc.pop(0))
        syllabes.append("".join(syll))
    return syllabes
