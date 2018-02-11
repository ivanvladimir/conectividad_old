#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Triggers for files
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2017/IIMAS/UNAM
# ----------------------------------------------------------------------

# System libraries
import re
import exceptions

re_pagenumber_ini = re.compile(r"(?P<num>\d+)\n")
re_pagenumber_fin = re.compile(r"\s+(?P<num>\d+)$")
re_footnote_mention = re.compile(r"[a-z](\d+)[,. ]")
re_footnote = re.compile(r'(?:^|\n)(?P<num>\d+)\n\s\s+\w+')

article_mention = r'(?:art.culos?) '\
                  r'(?P<articles>[\d.,y ixviabc]+-?) '\
                  r'(?:fracción [^,]*, )?(inciso [^,]*, )?'

title_rest = r'(?:(\w+[ \n]+)*(?:[A-Z]\w+,?[ \n]*)+)*'
re_interpretacion_sentencia =\
   re.compile(
     r'(?P<doc>(?:Interpretación (\w+ )*)?Sentencia[^"”\.,]{0})'.format(title_rest))

re_articlede = re.compile(article_mention +
                          r'(?:de esa|de esta|de la |del |de su |en la )?'
                          r'(?P<source>(dich[oa] '
                          r'|últim[oa] '
                          r'|presente ley '
                          r'|ley (\d+(\.\d+)?)?)?'
                          r'[^",;.()]*)[ ,.;]')


re_en_adelante = re.compile(r'en[ \n]*adelante[ \n]*.*')
re_definitions = re.compile(r'[“"](?P<term>[^”"]+)["”]')


def get_splits(spans):
    splits = []
    if isinstance(spans[-1][1],int):
        for spani, spanf in zip(spans, spans[1:]):
            splits.append((spani[1], spanf[0]))
        splits.append((spans[-1][1], None))
    else:
        for spani, spanf in zip(spans, spans[1:]):
            splits.append((spani[1][1], spanf[0][0]))
        splits.append((spans[-1][1][1], None))
    return splits


def enadelante(text, spans):
    if not spans:
        return [[]]
    splits = get_splits(spans)
    defis_span = []
    for ini, fin in splits:
        defis = []
        if not fin:
            fin = ini+100
        text_ = text[ini:fin]
        m = re_en_adelante.search(text_)
        if m:
            for defi in re_definitions.finditer(text_):
                span_ = defi.span("term")
                defis.append((span_[0]+ini, span_[1]+ini))
        defis_span.append(defis)
    return defis_span


t_definitions = [
    enadelante,
]


def test_definition(par, spans, cntx):
    text = "".join([x for x in par.itertext()])
    text_ = text.lower()

    definitions = []
    for idd, t in enumerate(t_definitions):
        definitions.extend(t(text_, spans))

    return definitions


def sentencia(text, cntx):
    docs = []
    for doc in re_interpretacion_sentencia.finditer(text):
        span = doc.span("doc")
        docs.append(span)
    return docs


t_docs = [
    sentencia,
]


def test_docs(par, cntx):
    text_ = "".join([x for x in par.itertext()])

    spans = []
    for idd, t in enumerate(t_docs):
        spans_ = t(text_, cntx)
        if len(spans_) == 0:
            continue
        spans_ = compatible_spans(spans_, spans)
        definitions_ = test_definition(par, spans_, cntx)
        spans.extend(zip(spans_, definitions_))
    return spans


def articlede(text, cntx):
    spans = []
    for m in re_articlede.finditer(text):
        spans.append((m.span('articles'),
                      m.span('source')))
    return spans


def article_mention_definition(text, cntx):
    spans = []
    for phrase, defis in cntx.definitions.items():
        re_mention = article_mention + r"(?:de )"\
                     r"(?P<source>" +\
                     r"|".join([d.lower() for d in defis]) +\
                     r")"
        for m in re.finditer(re_mention, text):
            spans.append((m.span('articles'),
                          m.span('source')))
    return spans


t_articles = [
    article_mention_definition,
    articlede,
]


def compatible_spans(spans1, spans):
    spans_ = []
    ii = 0
    jj = 0
    fin = 0
    if len(spans) == 0:
        return spans1
    spans__ = []
    for s, d in spans:
        spans__.append(s)
    spans = spans__
    while ii < len(spans) and jj < len(spans1):
        span = spans[ii][1]
        span1 = spans1[jj][1]
        if span[0] > fin and span[0] < span1[0]:
            fin = span[1]
            ii += 1
        elif span1[0] > fin and span1[0] < span[0]:
            spans_.append(spans1[jj])
            fin = span[1]
            jj += 1
        if span[0] < fin:
            ii += 1
        if span1[0] < fin:
            jj += 1
    return spans_


def test_articles(par, cntx):
    text = "".join([x for x in par.itertext()])
    text = text.replace('\n', ' ')
    text_ = text.lower()

    spans = []
    for idd, t in enumerate(t_articles):
        spans_ = t(text_, cntx)
        if len(spans_) == 0:
            continue
        spans_ = compatible_spans(spans_, spans)
        definitions_ = test_definition(par, spans_, cntx)
        spans.extend(zip(spans_, definitions_))
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


