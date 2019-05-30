#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import utils.global_var as gv
import utils.file as fl


def define_path_config(config_path):
    """Redifine path of config and update global vars.

    :param config_path: path of a folder containing config files
    :type path: str
    """
    if config_path != '':
        gv.PATH_CONF = config_path
    gv.DICT_SPECIAL_SYLL = fl.open_yml(
        os.path.join(gv.PATH_CONF, 'special_syll.yaml'))
    gv.DICT_SPECIAL_TYPE = fl.open_yml(
        os.path.join(gv.PATH_CONF, 'special_type.yaml'))
    gv.DICT_CONST = fl.open_yml(
        os.path.join(gv.PATH_CONF, 'constants.yaml'))
    gv.VOWEL = gv.DICT_CONST['vowel']
    gv.EXEPTION = gv.DICT_CONST['exeption']
    gv.CONSONNANT = gv.DICT_CONST['consonnant']
    gv.IER = gv.DICT_CONST['ier']


def define_path_forms(forms_path):
    """Redifine path of forms and update global vars.

    :param forms_path: path of a folder containing forms yaml
    :type path: str
    """
    if forms_path != '':
        gv.PATH_FORMS = forms_path
    list_atone_files = glob.glob(
        os.path.join('{}', '*.yaml').format(gv.PATH_FORMS))
    for filename in list_atone_files:
        gv.LIST_ATONE.extend(fl.open_yml(filename)['list'])
    i = 0
    len_list = len(gv.LIST_ATONE)
    while i < len_list:
        if isinstance(gv.LIST_ATONE[i], str) and gv.LIST_ATONE[i][-1] == 'e':
            gv.LIST_ATONE.append(gv.LIST_ATONE[i][:-1] + 'ë')
        i += 1
