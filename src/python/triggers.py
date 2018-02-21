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

re_parrafodela = re.compile(
                    r'p.rrafo[ \n](?P<parr>\d+)[ \n]de[ \n]'
                    r'(?P<source>la sentencia)')

#artículos 31.3 y 68
article_mention = r'(?:art.culos?[\n ])'\
                  r'(?P<articles>[\d\.,y ixvabc]+-?)[\n ]'\
                  r'(?:fracción [^,]*, )?(inciso [^,]*, )?'
source_mention = r'(?P<source>(?:de[\n ]esa|'\
                 r'de[\n ]esta[\n ]+|'\
                 r'de[\n ]la[\n ]+|'\
                 r'del[ \n]+|'\
                 r'de[\n ]su[\n ]+|'\
                 r'en[\n ]la[\n ]+)'\
                 r'(?:\w+[ \n]){0,8}\w+)'


title_rest = r'(?:(\w+[ \n]+){0,3}(?:[A-Z]\w+,?[ \n]*)+)*'
re_interpretacion_sentencia =\
   re.compile(
     r'(?P<doc>(?:Interpretación (\w+ )*)?Sentencia[^"”\.,]{0})'
     .format(title_rest))

re_articlede = re.compile(article_mention + source_mention)
re_yarticle = re.compile(r' y '
                         r'(?P<articles>[\d.y ]+)'
                         r' del (?P<source>(?:(\w+[\n ]+)+\w+))\.')
#los artículos 4 (Derecho a la Vida)
re_articlenum = re.compile(r'(?:art.culos?[ \n])(?P<articles>\d+[\n ]'
                            r"\(.+\))[ \n]de[ \n]la[ \n]"+
                            r'(?P<source>\w*)')


re_enadelante = re.compile(r'en[ \n]*adelante[ \n]*.*')
re_definitions = re.compile(r'[“"](?P<term>[^”"]+)["”]')
re_documents = re.compile(r"(?P<doc>{0})".format(r"|"
                          .join(
                                [doc.replace(" ", "[ \n]") for doc
                                 in exceptions.documents])))
re_institutions = re.compile(r"(?P<inst>{0})".format(r"|"
                             .join(
                              [ins.replace(" ", "[ \n]") for ins
                               in exceptions.institutions])))
re_avoid_defs_arts = re.compile(r"(?P<inst>{0})".format(r"|"
                                .join(
                                  [ins.lower().replace(" ", "[ \n]") for ins
                                   in exceptions.avoid_defs_arts])))
re_avoid_defs_mentions = re.compile(r"(?P<inst>{0})".format(r"|"
                                    .join(
                                      [ins.replace(" ", "[ \n]")
                                       for ins
                                       in exceptions.avoid_defs_mentions])))
#
#
# Caso Loayza Tamayo Vs. Perú. Interpretación de la Sentencia de Fondo.
# Resolución de la Corte Interamericana de Derechos Humanos de 8 de marzo
# de 1998. Serie C No. 47, párr. 16,
re_fullcase = re.compile(r'(?P<case>Caso[ \n][\n \w\(\)]+Vs\.'
                         r'[ \n](?:[A-Z]\w+[\n ]?)+)\.'
                         r'(?P<exception>[ \n]Excepciones[^\.]+\.)?'
                         r'(?P<interpretations>[ \n]Interpretaci.n[^\.]+\.)?'
                         r'(?P<resolution>[ \n]Resoluci.n[^\.]+\.)?'
                         r'(?P<case_name>[ \n]Sentencia[^\.]+\.)?'
                         r'(?P<serie>[ \n]Serie[^,]+\,)?'
                         r'(?P<paragraph>[ \n]p.rr\.[ \n][^,]+)+[,\.]'
                         )
# Caso Loayza Tamayo Vs. Perú.
re_case = re.compile(r"(?P<case>Caso .*) Vs. ([A-Z]\w+ ?)+")

# resolución 30/83
re_resolucion = re.compile(r"(?P<doc>resoluci.n[\ ]+\d+/\d+)")
# Acta
capitals_words = r'([A-Z]\w+[\n ]'\
                 r'|[a-zñ]{0,6}[\n ]|Vs\.[\n ])+[A-Z]\w+[a-z](?:[ \n]\d+)?'

re_capitals= re.compile(capitals_words)
capitals_types=[
    ("acta", re.compile(r"Acta[\n ]")),
    ("acuerdo", re.compile(r"Acuerdo[\n ]")),
    ("agencia", re.compile(r"Agencia[\n ]")),
    ("archivo", re.compile(r"Archivos?[\n ]")),
    ("asamblea", re.compile(r"Asamblea[\n ]")),
    ("asociacion", re.compile(r"Asociación[\n ]")),
    ("banco", re.compile(r"Banc.[\n ]")),
    ("boletin", re.compile(r"Bolet.n[\n ]")),
    ("batallon", re.compile(r"Batall.n[\n ]")),
    ("bases", re.compile(r"Bases?[\n ]")),
    ("brigada", re.compile(r"Brigada[\n ]")),
    ("carta", re.compile(r"Carta[\n ]")),
    ("caso", re.compile(r"Case[\n ]")),
    ("caso", re.compile(r"Caso[\n ]")),
    ("centro", re.compile(r"Centro[\n ]")),
    ("certificacion", re.compile(r"Certifica...?.?[\n ]")),
    ("clinica", re.compile(r"Cl.nica[\n ]")),
    ("colegio", re.compile(r"Colegio[\n ]")),
    ("comandancia", re.compile(r"Comandancia[\n ]")),
    ("comando", re.compile(r"Comando[\n ]")),
    ("comisaria", re.compile(r"Comisar.a[\n ]")),
    ("comision", re.compile(r"Comisi.n.?.?[\n ][^y]+[\n ]")),
    ("comite", re.compile(r"Comit.[\n ][^y]+[\n ]")),
    ("compania", re.compile(r"Compa..a[\n ]")),
    ("corporacion", re.compile(r"Corporaci.n[\n ]")),
    ("conferencia", re.compile(r"Conferencias?[\n ]")),
    ("congreso", re.compile(r"Congreso[\n ]")),
    ("consejo", re.compile(r"Consejo[\n ]")),
    ("constitucion", re.compile(r"Constituci.n[\n ][^y]+[\n ]")),
    ("consulado", re.compile(r"Consulado[\n ]")),
    ("convencion", re.compile(r"Convenci.n.?.?[\n ]")),
    ("corte", re.compile(r"Corte[\n ]")),
    ("cuartel", re.compile(r"Cuartel[\n ]")),
    ("camara", re.compile(r"C.mara[\n ]")),
    ("codigo", re.compile(r"C.digo[\n ]")),
    ("decision", re.compile(r"Decisi.n.?.?[\n ]")),
    ("decreto", re.compile(r"Decreto[\n ]")),
    ("defensor", re.compile(r"Defens..?.?.?[\n ]")),
    ("departamento", re.compile(r"Departamento[\n ]")),
    ("dictament", re.compile(r"Dictamen[\n ]")),
    ("direccion", re.compile(r"Direcci.n[\n ](General|Provincial|Nacional)[\n ]")),
    ("documento", re.compile(r"Ej.rcito[\n ]")),
    ("embajada", re.compile(r"Embajada[\n ]")),
    ("escrito", re.compile(r"Escrito[\n ]")),
    ("fiscalia", re.compile(r"Fiscal.a[\n ]")),
    ("fondo", re.compile(r"Fondo[\n ]")),
    ("fuerza", re.compile(r"Fuerza[\n ]")),
    ("fundacion", re.compile(r"Fundaci.n[\n ]")),
    ("gobernador", re.compile(r"Gobernador[\n ]")),
    ("gobernacion", re.compile(r"Gobernaci.nr[\n ]")),
    ("grupo", re.compile(r"Grupo[\n ]")),
    ("informe", re.compile(r"Informe[\n ]")),
    ("instituto", re.compile(r"Instituto[\n ]")),
    ("international", re.compile(r"International[\n ]")),
    ("jefatura", re.compile(r"Jefatura[\n ]")),
    ("juzgado", re.compile(r"Juzgado[\n ]")),
    ("laboratorio", re.compile(r"Laboratorio[\n ]")),
    ("ley", re.compile(r"Ley[\n ]")),
    ("ministerio", re.compile(r"Ministerio[\n ]")),
    ("movimiento", re.compile(r"Movimiento[\n ]")),
    ("notaria", re.compile(r"Notaria[\n ]")),
    ("oficialia", re.compile(r"Oficilia[\n ]")),
    ("oficina", re.compile(r"Oficina[\n ]")),
    ("organizacion", re.compile(r"Organiza...n[\n ]")),
    ("oficio", re.compile(r"Oficio[\n ]")),
    ("pacto", re.compile(r"Pacto[\n ]")),
    ("plan", re.compile(r"Plan[\n ]")),
    ("poder", re.compile(r"Poder[\n ]")),
    ("policia", re.compile(r"Policia[\n ]")),
    ("presidencia", re.compile(r"Precidencia[\n ]")),
    ("principios", re.compile(r"Principios[\n ]")),
    ("procedimiento", re.compile(r"Procedimiento[\n ]")),
    ("programa", re.compile(r"Programa[\n ]")),
    ("protocolo", re.compile(r"Protoc.lo[\n ]")),
    ("proyecto", re.compile(r"Proyecto[\n ]")),
    ("registro", re.compile(r"Registro[\n ]")),
    ("reglamento", re.compile(r"Reglamento[\n ]")),
    ("sala", re.compile(r"Sala[\n ]")),
    ("secretaria", re.compile(r"Secreatar.a[\n ]")),
    ("sala", re.compile(r"Sala[\n ]")),
    ("the", re.compile(r"The[\n ]")),
    ("tratado", re.compile(r"Tratado[\n ]")),
    ("tribunal", re.compile(r"Tribunal[\n ]")),
    ("unidad", re.compile(r"Unidad[\n ]")),
    ("universidad", re.compile(r"Universidad[\n ]")),
]


def groups2dic(m):
    return m.groupdict()


def get_splits(spans):
    splits = []
    if isinstance(spans[-1][1], int):
        for spani, spanf in zip(spans, spans[1:]):
            splits.append((spani[1], spanf[1]))
        splits.append((spans[-1][1], None))
    else:
        for spani, spanf in zip(spans, spans[1:]):
            if spans[-1][1] is not None:
                splits.append((spani[1][1], spanf[0][0]))
            else:
                splits.append((spani[0][1], spanf[0][0]))

        if spans[-1][1] is not None:
            splits.append((spans[-1][1][1], None))
        else:
            splits.append((spans[-1][0][1], None))

    return splits


def enadelante(text, spans):
    if not spans:
        return [[]]
    splits = get_splits(spans)
    defis_span = []
    for ini, fin in splits:
        defis = []
        limit = 200
        for w in [".", "caso", ")"]:
            limit_ = text[ini:].find(w)
            if limit_ >= 0:
                if limit_ < limit:
                    limit = limit_
        fin = ini+limit
        text_ = text[ini:fin]
        m = re_enadelante.search(text_)
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


# Procesa instituciones
def institutions(text, cntx):
    insts = []
    for inst in re_institutions.finditer(text):
        span = inst.span("inst")
        insts.append((span, groups2dic(inst)))
    return insts


t_institutions = [
    ("institutions", institutions),
]


def test_institutions(par, cntx):
    text_ = "".join([x for x in par.itertext()])

    spans = []
    values = []
    for type_, t in t_institutions:
        spans_m = t(text_, cntx)
        if len(spans_m) == 0:
            continue
        spans_m_dict = dict(spans_m)
        spans_ = [s for s, m in spans_m]
        flat_spans_ = compatible_spans(spans_, flat_spans(spans))
        final_spans_ = []
        for span_ in spans_:
            if span_ in flat_spans_:
                final_spans_.append(span_)
                vals = spans_m_dict[span_]
                vals["extraction"] = type_
                values.append(vals)
        definitions_ = test_definition(par, final_spans_, cntx)
        spans.extend(zip(final_spans_, definitions_, values))
    return spans


# Procesa documentos
def sentencia(text, cntx):
    docs = []
    for doc in re_interpretacion_sentencia.finditer(text):
        doc_name = doc.group("doc")
        if not len(doc_name.split()) == 1:
            span = doc.span("doc")
            docs.append((span, groups2dic(doc)))
    return docs, True


def fullcase(text, cntx):
    spans_ = []
    for m in re.finditer("Caso", text):
        ini, fin = m.span()
        if len(spans_) > 0:
            spans_[-1][0][1] = ini - 1
        spans_.append(([ini, fin], groups2dic(m)))
    if len(spans_) > 0:
        spans_[-1][0][1] = len(text)
    return [(tuple(s), m) for s, m in spans_], True


def case(text, cntx):
    spans = []
    for case in re_case.finditer(text):
        span = case.span('case')
        spans.append((span, groups2dic(case)))
    return spans, True


def documents(text, cntx):
    docs = []
    for doc in re_documents.finditer(text):
        span = doc.span("doc")
        docs.append((span, groups2dic(doc)))
    return docs, True


def resolucion(text, cntx):
    docs = []
    for doc in re_resolucion.finditer(text):
        span = doc.span("doc")
        docs.append((span, groups2dic(doc)))
    return docs, True


def mention_definition(text, cntx):
    spans = []
    for phrase, defis in cntx.definitions.items():
        re_mention = r"(?P<source>" +\
                     r"|".join([d.replace("*", '\*')
                                 .replace("(", "\(")
                                 .replace(")", "\)") for d in defis
                                                     if len(d) > 0]) +\
                     r")+"
        for m in re.finditer(re_mention, text):
            spans.append((m.span('source'), groups2dic(m)))
    if not re_avoid_defs_mentions.search(text):
        definitions_ = True
    else:
        definitions_ = False
    return spans, definitions_


def capital_docs(text, cntx):
    spans = []

    for doc in re_capitals.finditer(text):
        span = doc.span(0)
        text = doc.group(0)
        for type_, re_ in capitals_types:
            m = re_.match(text)
            if m:
                spans.append((span, groups2dic(m)))
                break
    return spans, []

t_docs = [
    ("fullcalse", fullcase),
    ("sentencia", sentencia),
    ("docuemnts", documents),
    ("case", case),
    ("resolucion", resolucion),
    ("mention_definition", mention_definition),
    ("capital", capital_docs),
]


def test_docs(par, cntx):
    text_ = "".join([x for x in par.itertext()])

    spans = []
    values = []
    for type_, t in t_docs:
        spans_m, flag_def = t(text_, cntx)
        spans_m_dict = dict(spans_m)
        if len(spans_m) == 0:
            continue
        spans_ = [s for s, m in spans_m]
        flat_spans_ = compatible_spans(spans_, flat_spans(spans))
        final_spans_ = []
        for span_ in spans_:
            if span_ in flat_spans_:
                final_spans_.append(span_)
                vals = spans_m_dict[span_]
                vals['extraction'] = type_
                values.append(vals)
        if flag_def:
            definitions_ = test_definition(par, final_spans_, cntx)
        else:
            definitions_ = []
        spans.extend(zip(final_spans_, definitions_, values))
    return spans


# Functions to extract article information
def articlede(text, cntx):
    spans = []
    for m in re_articlede.finditer(text):
        spans.append(((m.span('articles'),
                       m.span("source")), groups2dic(m)))
    return spans


def articlenum(text, cntx):
    spans = []
    for m in re_articlenum.finditer(text):
        spans.append(((m.span('articles'),
                      m.span('source')), groups2dic(m)))
    return spans


def yarticle(text, cntx):
    spans = []
    for m in re_yarticle.finditer(text):
        spans.append(((m.span('articles'),
                      m.span('source')), groups2dic(m)))
    return spans


def parrafodela(text, cntx):
    spans = []
    for m in re_parrafodela.finditer(text):
        spans.append(((m.span('parr'),
                      m.span('source')), groups2dic(m)))
    return spans


def article_mention_definition(text, cntx):
    spans = []
    for phrase, defis in cntx.definitions.items():
        re_mention = article_mention + r"(?:de )"\
                     r"(?P<source>" +\
                     r"|".join([d.replace("*", '')
                                 .replace("(", "\(")
                                 .replace(")", "\)")
                                 .lower() for d in defis]) +\
                     r")"
        for m in re.finditer(re_mention, text):
            spans.append(((m.span('articles'),
                          m.span('source')), groups2dic(m)))
    return spans


t_articles = [
    ("yarticle", yarticle),
    ("articlede", articlede),
    ("article_mention_definition", article_mention_definition),
    ("article_num", articlenum),
    ("parrafodela", parrafodela),
]


def compatible_spans(spans1, spans):
    spans = sorted([s for s in spans if s], key=lambda x: x[0])
    spans_ = []
    ii = 0
    jj = 0
    fin = 0
    if len(spans) == 0 or len(spans1) == 0:
        return spans1
    while ii < len(spans) and jj < len(spans1):
        span = spans[ii]
        span1 = spans1[jj]
        if span[0] > fin and span[1] < span1[0]:
            fin = span[1]
            ii += 1
            continue
        elif span1[0] > fin and span1[0] < span[0] and span1[1] < span[0]:
            spans_.append(spans1[jj])
            fin = span1[1]
            jj += 1
            continue
        if span1[0] > span[0] and span1[0] <= span[1]:
            fin = span[1]
            jj += 1
            continue
        if span1[0] <= span[0] and span1[1] <= span[1]:
            fin = span[1]
            jj += 1
            continue
        if span1[0] <= span[0] and span1[1] >= span[1]:
            fin = span[1]
            jj += 1
        if span1[0] >= span[0] and span1[1] >= span[1]:
            fin = span[1]
            ii += 1
        if span[0] < fin:
            ii += 1
        if span1[0] < fin:
            jj += 1
        if span1 == span:
            ii += 1
            jj += 1
    for span1 in spans1[jj:]:
        if span1 not in spans_:
            spans_.append(span1)
    return spans_


def flat_spans(spans):
    flat = []
    for span, defi, vals in spans:
        if isinstance(span[0], int):
            flat.extend([span] + defi)
        else:
            flat.extend([span[0], span[1]] + defi)
    return flat


def flat_article_spans(spans):
    flat = []
    for span in spans:
        if span[0] == span[1]:
            continue
        if isinstance(span[0], int):
            flat.extend([span])
        else:
            flat.extend([span[0], span[1]])
    return flat


def test_articles(par, cntx):
    text = "".join([x for x in par.itertext()])
    text = text.replace('\n', ' ')
    text_ = text.lower()
    spans = []
    for type_, t in t_articles:
        spans_m = t(text_, cntx)
        if len(spans_m) == 0:
            continue
        spans_m_dict = dict(spans_m)
        spans_ = [s for s, m in spans_m]
        flat_spans_ = flat_article_spans(spans_)
        flat_spans_ = compatible_spans(flat_spans_, flat_spans(spans))
        final_spans_ = []
        values = []
        for span_ in spans_:
            if span_[0] in flat_spans_ and span_[1] in flat_spans_:
                final_spans_.append(span_)
                vals = spans_m_dict[span_]
                vals['extraction'] = type_
                values.append(vals)
        if not re_avoid_defs_arts.search(text_):
            definitions_ = test_definition(par, final_spans_, cntx)
        else:
            definitions_ = []
        spans.extend(zip(final_spans_, definitions_, values))
    return spans



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
        if res.tail and len(res.tail) > 0:
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


def test_format(par):
    res = []
    for t, flag, continuation in t_formats:
        val = t(par)
        if val is not None:
            res.append((flag, val))
        if not continuation and val is not None:
            break
    return res
