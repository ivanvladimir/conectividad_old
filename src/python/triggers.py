#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Triggers for files
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2017/IIMAS/UNAM
# ----------------------------------------------------------------------

# System libraries
import xml.etree.ElementTree as ET
import re
import exceptions

re_pagenumber_ini = re.compile(r"(?P<num>\d+)\n")
re_pagenumber_fin = re.compile(r"\s+(?P<num>\d+)$")
re_footnote_mention = re.compile(r"[a-z](\d+)[,. ]")
re_footnote = re.compile(r'(?:^|\n)(?P<num>\d+)\n\s\s+\w+')


def test_format(par):
    res = []
    for t, flag, continuation in t_formats:
        val = t(par)
        if val is not None:
            res.append((flag, val))
        if not continuation and len(res) > 0:
            break
    return res


def numericalindex(par):
    res = par.find('.//NumericalIndex')
    if res is not None:
        return res.text


def pagenumber(par):
    m = re_pagenumber_ini.match(str(par.text))
    if m:
        return m.group("num")
    else:
        if (len(par) > 0):
            m = re_pagenumber_fin.match(str(par[-1].tail))
            if m:
                return m.group("num")


def namesection(par):
    res = par.find('.//RomanNumeralIndex')
    if res is not None:
        number = res.text
        if len(res.tail) > 0:
            name = res.tail.strip()
        return number+" "+name




def footnotemention(par):
    all_text = "".join([x for x in par.itertext()])
    footnotes = []
    for footnote in re_footnote_mention.findall(all_text):
        footnotes.append(int(footnote))
    if len(footnotes) == 0 and all_text.endswith('jueces 1:'):
        return [1]
    for exception, fn in exceptions.footnotementions:
        if exception in all_text:
            footnotes.append(fn)
    return footnotes


def footnote(par):
    all_text = "".join([x for x in par.itertext()])
    footnotes = []
    for footnote in re_footnote.findall(all_text):
        footnotes.append(footnote)
    return footnotes


t_formats = [
    (footnotemention, 'footnotemention', True),
    (pagenumber, 'pagenumber', True),
    (footnote, 'footnote', True),
    (namesection, 'namesection', False),
    (numericalindex, 'numericalindex', False)
]


