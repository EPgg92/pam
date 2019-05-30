#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""All functions needed for manage file in the pam."""

import csv
import yaml


def open_file(path, mode='r'):
    """Open the file of the path in the mode whished or print error.

    :param path: path to open
    :type path: str
    :param mode: mode to open the file
    :type mode: str
    :return: IO wrapper or 0
    :rtype: TextIOWrapper or int
    """
    try:
        return open(path, mode)
    except FileNotFoundError:
        print('PAM_Error: {} is not found.'.format(path))
    except PermissionError:
        print('PAM_Error: no permission on file: {}.'.format(path))
    else:
        print('PAM_Error: undefinned error occurs on file: {}.'.format(path))
    return 0


def open_yml(path):
    """Return a dict form a yml file.

    :param path: path to a yml file
    :type path: str
    :return: dictionnary corresponding at yml file
    :rtype: dict
    """
    returned_dic = {}
    with open_file(path, 'r') as stream:
        returned_dic = yaml.load(stream, Loader=yaml.SafeLoader)
    return returned_dic


def open_txt(path):
    """Return a string read from a file or print error.

    :param path: path of a file .txt.
    :type path: str
    :return: string in the file or 0
    :rtype: string or int
    """
    if not (len(path) > 4 and path[-4:] == '.txt'):
        print('PAM_Error: {} doesn\'t have the good extension.'.format(path))
        return 0
    txt = open_file(path)
    if txt:
        txt = txt.read()
        if txt:
            return txt
        print('PAM_Error: {} is an empty file.'.format(path))
    return 0


def write_txt(string, path):
    """Write a string in a file located to path.

    :param path: path where write file.
    :type path: str
    :param string: string to write in the file.
    :type string: str
    """
    with open_file(path, 'w+') as stream:
        stream.write(string)


def write_csv(data, path, delimiter='\t'):
    """Write a csv file to located path.

    :param path: path where write file.
    :type path: str
    :param data: list of list of datas
    :type data: list
    :param delimiter: pattern of delimitation of csv file
    :type delimiter: str
    """
    with open(path, 'w+') as stream:
        writer = csv.writer(stream, delimiter=delimiter)
        writer.writerows(data)
