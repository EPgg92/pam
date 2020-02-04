#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Class which contain where tags attributes according of list of syll."""

import re
from utils.textual import Textual
from utils.syllable import Syllable
import utils.syllabise as syllabise
import utils.global_var as gv


class Word(Textual):
    """Class Word which call Class Syllable and syllabise for tokenisation."""

    def __init__(self, word):
        """Create an object type Word."""
        super().__init__(word)
        self.__replacement_grapheme()
        self.__ie('ιes', 'ies')
        self.__ie('ιent', 'ient')
        self.__ierz()
        self.__get_list_syll()
        self.__in_list_atone()
        self.get_list_type()
        self.create_metrification()

    def __in_list_atone(self):
        if self.text in gv.LIST_ATONE:
            for syll in self.list_syll:
                if syll.type == 2:
                    syll.set_type(1)
                elif syll.type == 1:
                    syll.set_type(0)
        elif len(self.list_syll) == 1:
            self.list_syll[0].set_type(2)

    def __ie(self, finish_ie='ιes', replace_ie='ies'):
        len_ie = len(finish_ie)
        if self.text[-len_ie:] == finish_ie:
            self.text = '{}{}'.format(self.text[:-len_ie], replace_ie)

    def __ierz(self):
        if bool(re.match(
                r'(^[qwrtzpsdfghjklxcvnmb]{1,2})(ι)(e[rze]$)', self.text)):
            match = re.match(
                r'(^[qwrtzpsdfghjklxcvnmb]{1,2})(ι)(e[rze]$)', self.text)
            if match.group(1) not in gv.IER:
                self.text = '{}{}{}'.format(
                    match.group(1), 'i', match.group(3))
        if bool(re.match(
                r'(.*[qwrtzpsdfghjklxcvnmb]{2,})(ι)(e[rz]$)', self.text)):
            match = re.match(
                r'(.*[qwrtzpsdfghjklxcvnmb]{2,})(ι)(e[rz]$)', self.text)
            if match.group(1)[-2:] not in gv.IER:
                self.text = '{}{}{}'.format(
                    match.group(1), 'i', match.group(3))

    def __replacement_grapheme(self):
        # "ie" -> "ιe" / _{C,e}
        self.text = re.sub(
            r'(.*(rd){0})(i|y)(e[qwrtzpsdfghjklxcvnmbe]+$)',
            r'\1ι\4', self.text)
        # self.text = re.sub(
        #     r'(.*rd)(i)(en)',
        #     r'\1ι\3', self.text)
        # "ia" -> "ιa" / _C
        self.text = re.sub(
            r'(.*(rd){0})(i|y)(a[qwrtzpsdfghjklxcvnmb]+$)',
            r'\1ι\4', self.text)
        # "io" -> "ιo" / _{C,e}
        self.text = re.sub(
            r'(.*(rd){0})(i|y)(o[qwrtzpsdfghjklxcvnmbe].*)',
            r'\1ι\4', self.text)
        # "ιon" -> "ion" / _#
        self.text = re.sub(
            r'(.*[aeouäëöüÿáéóúàèòùâêôû]{0})(i|y|ι)((on|ons)+$)',
            r'\1i\4', self.text)
        # "ien" -> "ιen" / _# ("ien" graphie alternative de "ion")
        # Elle est passé où la Regex ? WTF ?
        # "ie" -> "ιe" / _V
        self.text = re.sub(
            r'(.*)(i|y)(e.*[aeouäëöüÿáéóúàèòùâêôû])',
            r'\1ι\3', self.text)
        # "tιon" -> "tion" / _#
        self.text = re.sub(
            r'(.*(c|t))(i|y|ι)((eu|eux|eus|euse)+$)',
            r'\1i\4', self.text)
        # "prι" -> "pri" / _V
        self.text = re.sub(
            r'(.*pr)(i|y|ι)([aeouäëöüÿáéóúàèòùâêôû].*)',
            r'\1i\3', self.text)
        # "crι" -> "cri" / _V
        self.text = re.sub(
            r'(.*cr)(i|y|ι)([aeouäëöüÿáéóúàèòùâêôû].*)',
            r'\1i\3', self.text)
        # "blι" -> "bli" /_V
        self.text = re.sub(
            r'(.*bl)(i|y|ι)([aeouäëöüÿáéóúàèòùâêôû].*)',
            r'\1i\3', self.text)
        # "rcι" -> "rci" /_V
        # Ne doit pas fonctionner pour "bercier" -> est-ce vraiment une règle ?
        # Sinon : ne doit pas fonctionner devant -er. Ce que j'ai fait pour
        # gérer "trepercier"...
        self.text = re.sub(
            r'(.*rc)(i|y|ι)([aouäëöüÿáéóúàèòùâêôû](e(r){0}).*)',
            r'\1i\4', self.text)
        # "ci" -> "cι" /V_V
        self.text = re.sub(
            r'([aeouäëöüÿáéóúàèòùâêôû]c)(i|y|ι)([euäëöüÿáéóúàèòùâêôû].*)',
            r'\1ι\3', self.text)
        # "slι" -> "sli" /_V
        self.text = re.sub(
            r'(.*sl)(i|y|ι)([aeouäëöüÿáéóúàèòùâêôû].*)',
            r'\1i\3',
            self.text)
        # "plι" -> "pli" /_V
        self.text = re.sub(
            r'(.*pl)(i|y|ι)([aeouäëöüÿáéóúàèòùâêôû].*)',
            r'\1i\3',
            self.text)
        # "gu" -> "gü" /_V
        self.text = re.sub(
            r'(.*(q|g))(u|υ)([qwrtzpsdfghjklxcvnmb]{1,}.*)',
            r'\1ü\4',
            self.text)

        # "ιen" -> "ïen" /_#
        self.text = re.sub(
            r'(.*[aeiouäëïöüÿáéíóúàèìòùâêîôû]{1,}([dbt]|[qwrzpfghjkxcvnm]{1,}|'
            '[s]{1}))(i|ι)(en(s|z)?$)',
            r'\1ï\4',
            self.text)
        # J'ai dû sortir "d" de la liste avec "r"{1,} pour empêcher que "rd" ne
        # déclenche la règle ; c'est une implémentation native de l'exception.
        # Idem avec "b" pour "mb".
        # Idem avec <t> pour <contien>

        # "lιez" -> "liez"  &   "crι" -> "cri"   -> WTF, cette règle ne fait
        # pas du tout ça, j'ai été obligé de réécrire cri ailleur ! WTF (bis)
        # : la règle ne dit pas ça du tout !
        self.text = re.sub(
            r'(.*sq(u)?)(i|ι)(er)',
            r'\2ï\4', self.text)
        # "Vlies" -> "Vlïes"    &   "Vcries" -> "Vcrïes"
        self.text = re.sub(
            r'(.*[aeiouäëïöüÿáéíóúàèìòùâêîôû]{1,})(l|cr)(i|ι)((e(s|z)|é)$)',
            r'\1\2ï\5', self.text)
        # "-uer" -> "-üer"
        self.text = re.sub(
            r'([aeiuäëïüÿáéíóúàèìùâêîû][wrtzpsdfghjklxvnmb])(u|ü)(er$)',
            r'\1ü\3', self.text)
        # self.text = re.sub(
        # r'(.*t)(i|ι|y)(er$)',
        # r'\1ι\3', self.text)
        self.text = re.sub(
            r'(ue)(i)(.*)',
            r'\1ι\3', self.text)
        # pour résolution de bug, à vérifier dans l'usage.
        # "-geoient" -> goient
        self.text = re.sub(
            r'(ge)(oι)(ent$)',
            r'goi\3', self.text)
        # Supprimer le -e- n'est pas très élégant ; c'est la seule solution que
        # j'ai trouvée pour l'instant.
        self.text = re.sub(
            r'(^[qwrtzpsdfghjklxcvnmb])(oee)((s){0,1}$)',
            r'\1oυee\3', self.text)
        # Rajouter un -υ- n'est pas élégant ; c'est la seule solution que j'ai
        # trouvée pour l'instant.
        self.text = re.sub(
            r'(.*l)(oe)((e|[qwrtzpsdfghjklxcvnmb].*){0,1}$)',
            r'\1oυe\3', self.text)
        # Évaluer si on peut fusionner les deux règles précédentes.

        # "Coue" -> "Coυe"
        self.text = re.sub(
            r'([qwrtzpdfghjklxcvnm])(o(u|ü))(e)',
            r'\1oυ\3', self.text)
        # J'ai dû enlever <b> de la liste, pour ne pas la déclencher sur "boue"
        # ([buə]). C'est peut-être aussi le cas de beaucoup d'autres consonnes,
        # qu'il ne faudra pas hésiter à retirer de cette liste.
        # <s> pour <soue>.

        # Pour gérer "viel" et ses composés
        self.text = re.sub(
            r'(.*v)(ie)(l.*)',
            r'\1ιe\3', self.text)

        # Vélarisation ALS
        self.text = re.sub(
            r'(.*)(ea)(l(s|z))',
            r'\1æ\3', self.text)

        # "-ssia-" -> "-ssιa-"
        self.text = re.sub(
            r'(.*ss)(i)(a.*)',
            r'\1ι\3', self.text)

    def __get_list_syll(self):
        # TODO : factorise this function with __in_list_atone()
        if self.text in gv.DICT_SPECIAL_SYLL:
            list_syll = gv.DICT_SPECIAL_SYLL[self.text]
        else:
            list_syll = syllabise.syllabise_word(self.text)
        list_syll = [Syllable(syll) for syll in list_syll]
        if list_syll != []:
            list_syll[-1].set_is_last()
            if re.search(r'[^qg]ues$', list_syll[-1].text):
                list_syll[-1].set_type(2)
                list_syll[-1].set_text(list_syll[-1].text[:-2])
                list_syll.append(Syllable('es'))
                list_syll[-1].set_type(0)
            elif re.search(r'[^qg]ue$', list_syll[-1].text):
                list_syll[-1].set_type(2)
                list_syll[-1].set_text(list_syll[-1].text[:-1])
                list_syll.append(Syllable('e'))
                list_syll[-1].set_type(0)
            elif re.search(r'[^qg]uent$', list_syll[-1].text):
                list_syll[-1].set_type(2)
                list_syll[-1].set_text(list_syll[-1].text[:-3])
                list_syll.append(Syllable('ent'))
                list_syll[-1].set_type(0)

        if len(list_syll) > 1:
            if re.search(r'ie$', list_syll[-1].text):
                list_syll[-2].set_type(2)
                list_syll[-1].set_text(list_syll[-1].text[:-1])
                list_syll.append(Syllable('e'))
                list_syll[-1].set_type(0)
            elif re.search(r'ies$', list_syll[-1].text):
                list_syll[-2].set_type(2)
                list_syll[-1].set_text(list_syll[-1].text[:-2])
                list_syll.append(Syllable('es'))
                list_syll[-1].set_type(0)
            elif re.search(r'ient$', list_syll[-1].text):
                list_syll[-2].set_type(2)
                list_syll[-1].set_text(list_syll[-1].text[:-3])
                list_syll.append(Syllable('ent'))
                list_syll[-1].set_type(0)
            elif re.search(r'e(nt|s){0,1}$', list_syll[-1].text):
                list_syll[-1].set_type(0)
                list_syll[-2].set_type(2)
            elif re.search(r'ë(nt|s)?$', list_syll[-1].text):
                list_syll[-1].set_type(0)
                list_syll[-2].set_type(2)
            else:
                list_syll[-1].set_type(2)
        self.list_syll = list_syll

    def get_list_type(self):
        if self.text in gv.DICT_SPECIAL_TYPE:
            for i, type_syll in enumerate(gv.DICT_SPECIAL_TYPE[self.text]):
                self.list_syll[i].set_type(type_syll)
        self.list_type = [syll.type for syll in self.list_syll]

    def create_metrification(self):
        """Create metrification in function of the list of syll and type."""
        def __aligne_left(syll, type_syll):
            align = '{{:^{}}}'.format(len(syll))
            return align.format(type_syll)
        self.word_type = [syll.type for syll in self.list_syll]
        self.str_word_syll = "·".join([syll.text for syll in self.list_syll])
        self.str_word_type = " ".join([__aligne_left(syll.text, syll.type)
                                       for syll in self.list_syll])
