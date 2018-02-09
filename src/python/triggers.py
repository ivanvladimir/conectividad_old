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

re_recovery=re.compile(r'(?:art.culos?|art.culos?) '
                       r'(?P<articles>[\d.,y ixviabc]+-?) '
                       r'(?:fracción [^,]*, )?(inciso [^,]*, )?'
                       r'(?:de esa|de esta|de la |del |de su |en la )?'
                       r'(?P<source>(dich[oa] '
                       r'|últim[oa] '
                       r'|presente ley '
                       r'|ley (\d+(\.\d+)?)?)?'
                       r'[^",;.()]*)[ ,.;]')



re_en_adelante=re.compile(r'en adelante.*“(?P<term>[^”"]+)”')


def get_splits(spans):
    splits=[]
    if len(spans)==0:
        return None
    for span in spans[1:]:
        splits.append(span[0][0])
    if len(splits)==0:
        return [spans[0][0]]
    return splits



def enadelante(text,spans):
    splits=get_splits(spans)
    if not splits:
        splits=[len(text)]
    for s in splits:
        text_=text[s:s+1]
        for m in re_en_adelante.finditer(text_):
            spans.append((m.span('articles'),
                         m.span('source')))
    return spans

t_definitions = [
    enadelante,
]

def test_definition(par, spans,cntx):
    deff = []
    text = "".join([x for x in par.itertext()])
    text_ = text.lower()

    definitions = []
    for idd, t in enumerate(t_definitions):
        definitions.extend(t(text_,spans))
    print("---->",definitions)
    return definitions


def articlede(text):
    spans = []
    for m in re_recovery.finditer(text):
        spans.append((m.span('articles'),
                     m.span('source')))
    return spans

t_articles = [
    articlede,
]

def test_articles(par, cntx):
    arts = []
    text = "".join([x for x in par.itertext()])
    text_ = text.lower()

    spans = []
    definitions = []
    for idd, t in enumerate(t_articles):
        spans_=t(text_)
        spans.extend(spans)
        definitions_ = test_definition(par,spans,cntx)
        definitions.extend(definitions_)

    return spans


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
    (footnote, 'footnote', True),
    (pagenumber, 'pagenumber', True),
    (namesection, 'namesection', False),
    (numericalindex, 'numericalindex', False)
]


