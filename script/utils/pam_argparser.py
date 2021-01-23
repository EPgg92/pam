#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Manage options and arguments of the pam."""

import argparse


def get_pam_argparse():
    """Create an namespaces of all arguments options given.

    :return: namespaces containing all options and their value.
    :rtype: Namespaces()
    """
    parser = argparse.ArgumentParser(
        description='Produce prosodical-metrical analyses of text.')
    selector = parser.add_argument_group(title='Selector',
                                         description='Different options'
                                         ' to select verses.')
    debug = parser.add_argument_group(title='Configuration',
                                      description=' Options for configuration'
                                      ' of the input.')
    parser.add_argument('-f', '--files', nargs='+', metavar='filename',
                        help='Path of file to analyse',
                        type=str, required=True)
    parser.add_argument('-g', '--general',
                        help='print only the sum up analyse',
                        action='store_true')
    parser.add_argument('-m', '--metrics', help='show the metrical tags\'line',
                        type=int, default=-1, metavar='meter',)
    # debug.add_argument('-d', '--debug', nargs='+', metavar='letters',
    #                    help='print specifique information debug '
    #                    '[t, v, w, s]',
    #                    choices=set(['t', 'v', 'w', 's']),
    #                    type=str, default=[])
    debug.add_argument('-C', '--config', metavar='filename',
                       help='select an other config folder',
                       type=str, default='')
    debug.add_argument('-F', '--forms', metavar='filename',
                       help='select an other forms folder',
                       type=str, default='')
    debug.add_argument('-S', '--save_output_format', nargs='+',
                       help='save output in a file with one of the '
                       'following format'
                       ' \'csv\' or \'xlsx\' or \'txt\'',
                       choices=['csv', 'xlsx', 'txt'], metavar='format',
                       default=[])
    debug.add_argument('-L', '--line_by_line_meter',
                       action='store_true',
                       help='Create a line by line meter text file',
                       default = False)
    # debug.add_argument('-l', '--save_log_file', metavar='filename',
    #                    help='save command log in chosen file',
    #                    type=argparse.FileType('a+'),
    #                    default=open('log.txt', 'a+'))
    selector.add_argument('-c', '--cesure', nargs='+', metavar='string',
                          help='select verses fitting the wanted '
                          'cesure type; if a metrics is define',
                          type=str, default=[])
    selector.add_argument('-k', '--not_cesure', nargs='+', metavar='string',
                          help='select verses not fitting the wanted '
                          'cesure type; if a metrics is define',
                          type=str, default=[])
    selector.add_argument('-t', '--these_meters', nargs='+', metavar='number',
                          help='select verses fitting the wanted meter',
                          type=int, default=[])
    selector.add_argument('-T', '--not_these_meters', nargs='+',
                          metavar='number',
                          help='select verses not fitting'
                          ' the wanted meter',
                          type=int, default=[])
    selector.add_argument('-n', '--verse_number', nargs='+', metavar='numbers',
                          help='select lines by their numbering',
                          type=int, default=[])
    selector.add_argument('-a', '--after_verse_number', metavar='number',
                          help='select lines whose numbering is equal of '
                          'higher to the number indicated',
                          type=int, default=-1)
    selector.add_argument('-b', '--before_verse_number', metavar='number',
                          help='select lines whose numbering is lower the '
                          'number indicated',
                          type=int, default=-1)
    args = parser.parse_args()
    if args.not_cesure != [] and args.metrics == -1:
        parser.error("-k (--not_cesure) requires -m (--metrics) to work.")
    if args.cesure != [] and args.metrics == -1:
        parser.error("-c (--cesure) requires -m (--metrics) to work.")
    if args.metrics == -1 and args.general:
        parser.error("-g (--general) requires -m (--metrics) to work.")
    return args
