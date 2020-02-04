#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Object to manage all pam activities."""
import os
import pprint
from collections import defaultdict as dd
import pandas as pd
import utils.global_var as gv
import utils.file as fl
import utils.datetime_pam as dp
from utils.verse import Verse


class Pam_manager():
    """Class which manage pam activities in fonction of the pam_argparse."""

    def __init__(self, pamargv):
        """Create an object type Pam_manager."""
        gv.METRICS = pamargv.metrics
        self.pamargv = pamargv
        self.files = {}
        self.to_print = ''
        self.verse_numbers = set()
        self.stat_meter = dd(lambda: dd(int))
        self.stat_cesure = dd(lambda: dd(float))
        self.dataframe = dd(list)

        self.__get_verces()
        if self.__select_number():
            self.__select_verse_number()
        self.__process_verse()
        self.__select_verse_meter()
        self.__select_verse_cesure()
        self.__organize_in_tab()
        if not self.pamargv.general:
            self.__get_verse_str()
        self.__get_stat()
        self.__get_general_stat_str()
        self.__get_stat_str()
        self.__save_in_file()

    def __get_verces(self):
        def get_dict_verces(txt):
            dict_verces = {}
            txt = txt.split('\n')
            num_verce = 1
            for line in txt:
                line = line.strip()
                if line != '':
                    dict_verces[num_verce] = line
                    num_verce += 1
            return dict_verces

        for i, path in enumerate(self.pamargv.files):
            txt = fl.open_txt(path)
            if txt:
                self.files[i] = (path, get_dict_verces(txt))

    def __select_number(self):
        def get_max(files):
            max_verse_number = max([len(files[key][1])
                                    for key in files])
            return max_verse_number
        ret = True
        after = self.pamargv.after_verse_number
        before = self.pamargv.before_verse_number
        numbers = self.pamargv.verse_number
        if after + before == -2:
            if numbers == []:
                ret = False
            else:
                self.verse_numbers = numbers
        else:
            if after == -1:
                after = 1
            if before < 0:
                before = get_max(self.files)
            while after < before:
                self.verse_numbers.add(after)
                after += 1
            self.verse_numbers = self.verse_numbers.union(numbers)
        return ret

    def __select_verse_number(self):
        for key in sorted(self.files):
            path, dict_verses = self.files[key]
            dict_verses = {num_verce: dict_verses[num_verce]
                           for num_verce in dict_verses
                           if num_verce in self.verse_numbers}
            self.files[key] = path, dict_verses

    def __select_verse_meter(self):
        these = self.pamargv.these_meters
        not_these = self.pamargv.not_these_meters
        if these + not_these != []:
            for key in sorted(self.files):
                path, dict_verses = self.files[key]
                if these != []:
                    dict_verses = {num: dict_verses[num] for num in
                                   dict_verses if dict_verses[num].meter
                                   in these}
                else:
                    dict_verses = {num: dict_verses[num] for num in
                                   dict_verses if dict_verses[num].meter
                                   not in not_these}
                self.files[key] = path, dict_verses

    def __select_verse_cesure(self):
        if self.pamargv.cesure != []:
            for key in sorted(self.files):
                path, dict_verses = self.files[key]
                dict_verses = {num: dict_verses[num] for num
                               in dict_verses if len(set.intersection(
                                   set(self.pamargv.cesure),
                                   dict_verses[num].cesure)) > 0}
                self.files[key] = path, dict_verses
        if self.pamargv.not_cesure != []:
            for key in sorted(self.files):
                path, dict_verses = self.files[key]
                dict_verses = {num: dict_verses[num] for num
                               in dict_verses if len(set.intersection(
                                   set(self.pamargv.not_cesure),
                                   dict_verses[num].cesure)) == 0}
                self.files[key] = path, dict_verses

    def __process_verse(self):
        for key in sorted(self.files):
            _, dict_verses = self.files[key]
            for number in dict_verses:
                dict_verses[number] = Verse(dict_verses[number], number)

    def __organize_in_tab(self):
        def separe_list(listtosep, sep=' '):
            len_list = len(listtosep)
            i = 0
            ret = []
            while i < len_list:
                for elt in listtosep[i]:
                    ret.append(elt)
                if i < len_list - 1:
                    ret.append(sep)
                i += 1
            return ret

        for key in sorted(self.files):
            _, dict_verses = self.files[key]
            for number in dict_verses:
                verse = dict_verses[number]
                list_syll_word = [[s.text for s in w]
                                  for w in verse.verse_syll]
                self.dataframe[key].append(separe_list(verse.verse_type, '|'))
                self.dataframe[key].append(separe_list(list_syll_word, ' '))

    def __get_verse_str(self):
        def get_max_length(dict_verses):
            len_max = 10
            for number in dict_verses:
                verse = dict_verses[number]
                len_str = max(len(verse.str_verse_syll),
                              len(verse.str_verse_type))
                if len_max < len_str:
                    len_max = len_str
            return len_max

        def format_meter(verse, gmeter):
            if self.pamargv.metrics <= 0:
                return ''
            return 'm:{meter}[{gmeter}]'.format(meter=verse.meter,
                                                gmeter=gmeter)

        def format_cesure(verse):
            return '/'.join(sorted(verse.cesure))

        def format_line_number(verse):
            return 'num_l:{}'.format(verse.num_verse)

        gmeter = self.pamargv.metrics
        for key in sorted(self.files):
            path, dict_verses = self.files[key]
            self.to_print += 'Analyse de {}\n'.format(path)
            len_max = get_max_length(dict_verses)
            pattern = '\n{{:<{len}}}\t{{}}\t{{}}\n{{:<{len}}}\t{{}}'
            pattern = pattern.format(len=len_max)
            for number in dict_verses:
                verse = dict_verses[number]
                self.to_print += pattern.format(verse.str_verse_type,
                                                format_meter(verse, gmeter),
                                                format_cesure(verse),
                                                verse.str_verse_syll,
                                                format_line_number(verse))
            self.to_print += '\n\n'

    def __get_stat(self):
        len_dict_cesure = 1
        if self.pamargv.metrics in gv.DICT_CESURE:
            len_dict_cesure = len(gv.DICT_CESURE)
        for key in sorted(self.files):
            path, dict_verses = self.files[key]
            for num in dict_verses:
                verse = dict_verses[num]
                self.stat_meter[(key, path)][verse.meter] += 1
                for ces in verse.cesure:
                    self.stat_cesure[(key, path)][ces] += 1 / len_dict_cesure

    def __get_stat_str(self):
        def _pourcent(number, total, keep=True):
            def _divide(number, total):
                try:
                    return number / total
                except ZeroDivisionError:
                    return 0

            str0 = '{:05.2f}% soit {:^4}/{}'.format(
                _divide(number, total / 1) * 100, number, total)
            if not keep:
                return str0[:-len(str(total)) - 1]
            return str0

        def __str_form_meter(badgood, number, total):
            return _pourcent(number, total) + ' vers {} formés\n'.format(
                badgood)

        def __str_bad_meter(meter, gmeter, number, total):
            return '\t- m:{}[{}]\t'.format(meter, gmeter) + _pourcent(number,
                                                                      total,
                                                                      False)

        def __str_bad_cesure(cesure, number, total):
            return '\t- {}\t'.format(cesure) + _pourcent(number, total, False)

        def __all_bad_meter(gmeter, dict_meter, total):
            return '\n'.join([__str_bad_meter(m, gmeter, dict_meter[m], total)
                              for m in sorted(dict_meter) if m != gmeter])

        def __all_cesure(dict_cesure, total, fact):
            return '\n'.join([__str_bad_cesure(c, round(dict_cesure[c] * fact),
                                               total)
                              for c in sorted(dict_cesure)])

        gmeter = self.pamargv.metrics
        if gmeter > 0:
            for key, path in sorted(self.stat_meter):
                dict_meter = self.stat_meter[(key, path)]
                self.to_print += '{key} {path}\tm:{m}\n'.format(key=key + 1,
                                                                path=path,
                                                                m=gmeter)
                total = sum([dict_meter[m] for m in dict_meter])
                bad = total - dict_meter[gmeter]
                self.to_print += __str_form_meter('bien', dict_meter[gmeter],
                                                  total)
                self.to_print += __str_form_meter('mal', bad, total)
                self.to_print += __all_bad_meter(gmeter, dict_meter, total)
                self.to_print += '\n\n'
                if (key, path) in self.stat_cesure:
                    dict_cesure = self.stat_cesure[(key, path)]
                    self.to_print += 'Distribution des césures'
                    self.to_print += ' pour {} vers:\n'.format(total)
                    self.to_print += __all_cesure(dict_cesure, total,
                                                  len(gv.DICT_CESURE))
                    self.to_print += '\n'
                self.to_print += '\n'

    def __get_general_stat_str(self):
        key_g = len(self.stat_meter)
        if key_g > 1:
            key_g = (key_g, 'general')
            for key, path in sorted(self.stat_meter):
                dict_meter = self.stat_meter[(key, path)]
                for meter in dict_meter:
                    self.stat_meter[key_g][meter] += dict_meter[meter]
                if (key, path) in self.stat_cesure:
                    dict_cesure = self.stat_cesure[(key, path)]
                    for cesure in dict_cesure:
                        self.stat_cesure[key_g][cesure] += dict_cesure[cesure]

    def __rewrite_dataframe(self):
        def get_max_list(dataframe):
            return max([len(l) for l in dataframe])

        def create_lines_syll_meter(verse, len_max):
            def flat_list(xlist):
                ret = []
                for x in xlist:
                    ret.extend(x)
                return ret

            len_max *= 2
            list_syll = flat_list([[s.text for s in w]
                                   for w in verse.verse_syll])
            list_type = flat_list(verse.verse_type)
            len_syll_type = len(list_type)
            i = 0
            j = 0
            ret_line_meter = []
            ret_line_syll = []
            minus = False
            while j < len_max:
                if i < len_syll_type and ((minus and list_type[i] < 0) or
                                          (not minus and list_type[i] >= 0)):
                    ret_line_meter.append(list_type[i])
                    ret_line_syll.append(list_syll[i])
                    i += 1
                else:
                    ret_line_meter.append('')
                    ret_line_syll.append('')
                j += 1
                minus = not minus
            return ret_line_meter, ret_line_syll

        for key in self.dataframe:
            dataframe = self.dataframe[key]
            len_max = get_max_list(dataframe)
            len_dataframe = len(dataframe)
            i = 0
            while i < len_dataframe:
                len_i = len(dataframe[i])
                dataframe[i] = dataframe[i] + [''] * (len_max - len_i)
                i += 1
            i = 0
            verses = self.files[key][1]
            for num_verse in sorted(verses):
                verse = verses[num_verse]
                len_dataverse = len(dataframe[i])
                dataframe[i], dataframe[i + 1] = create_lines_syll_meter(
                    verse, len_max)
                dataframe[i] += [''] + [verse.meter] + sorted(verse.cesure)
                dataframe[i + 1] += [num_verse]
                i += 2
            col_name = []
            for x in range(len_max):
                col_name.append('syll_tag{}'.format(x + 1))
                col_name.append('syll_tag{} -1'.format(x + 1))
            col_name += ['num_l', 'meter']
            if gv.METRICS in gv.DICT_CESURE:
                col_name += ['ces_{}'.format(x) for x in
                             gv.DICT_CESURE[gv.METRICS]]
            self.dataframe[key] = pd.DataFrame(dataframe, columns=col_name)

    def __save_txt(self):
        list_filename = [self.files[key][0] for key in self.files]
        list_filename = [''.join(os.path.basename(f).split('.')[:-1])
                         for f in list_filename]
        filename = '_'.join(list_filename)
        filename = '.'.join([filename, dp.get_now(), 'txt'])
        fl.write_txt(str(self), os.path.join('pam_output', filename))

    def __save_xlsx(self):
        def __dataframe_stat_meter(dict_meter):
            total = sum([dict_meter[key] for key in dict_meter])
            return pd.DataFrame([[key, dict_meter[key],
                                  dict_meter[key] / total * 100]
                                 for key in sorted(dict_meter)],
                                columns=['meter', 'occurence', 'frequence'])

        def __dataframe_stat_cesure(dict_cesure):
            return pd.DataFrame([[key, dict_cesure[key] * len(gv.DICT_CESURE)]
                                 for key in sorted(dict_cesure)],
                                columns=['cesure', 'occurence'])

        self.__rewrite_dataframe()
        for key in self.files:
            filename = ''.join(os.path.basename(
                self.files[key][0]).split('.')[:-1])
            filename = '.'.join([filename, dp.get_now(), 'xlsx'])
            path = os.path.join('pam_output', filename)
            tags_syll = self.dataframe[key]
            stat_key = (key, self.files[key][0])
            stat_meter = __dataframe_stat_meter(self.stat_meter[stat_key])
            dict_cesure = __dataframe_stat_cesure(self.stat_cesure[stat_key])
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            tags_syll.to_excel(writer, sheet_name='tags_syll', index=False)
            stat_meter.to_excel(writer, sheet_name='stat_meter', index=False)
            dict_cesure.to_excel(writer, sheet_name='stat_cesure', index=False)
            writer.save()

    def __save_csv(self):
        for key in self.files:
            filename = ''.join(os.path.basename(
                self.files[key][0]).split('.')[:-1])
            filename = '.'.join([filename, dp.get_now(), 'csv'])
            data = self.dataframe[key]
            path = os.path.join('pam_output', filename)
            fl.write_csv(data, path, ',')

    def __save_in_file(self):
        if self.pamargv.save_output_format != []:
            os.makedirs('pam_output', exist_ok=True)
        if 'txt' in self.pamargv.save_output_format:
            self.__save_txt()
        if 'csv' in self.pamargv.save_output_format:
            self.__save_csv()
        if 'xlsx' in self.pamargv.save_output_format:
            self.__save_xlsx()

    def __str__(self):
        """Return the string to_print containing all information."""
        return self.to_print

    def debug(self):
        """Debug methode, usefull for developpement."""
        return pprint.pformat(vars(self))
