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
from tinydb import Query

re_enters = re.compile(r"\n+")
re_spaces = re.compile(r"\s+")
re_fromltoc = re.compile(r"^[a-z ]+(?P<caption>[A-Z]+\D*)")
re_espace_or_enter = re.compile(r"[ \n]")
re_numbers = re.compile(r'([\d.]+| [IXVixv]+ )')


def split_arts(text):
    return " ".join(re_numbers.findall(text))


def resolve_document(tag, cntx, definitions, db):
    text = tag.text
    attrib = tag.attrib
    text = re_enters.sub(" ", text)
    text = re_spaces.sub(" ", text)
    text_ = re_espace_or_enter.sub("[ \n]", text)
    # Avoid solving
    flag = False
    for exception in exceptions:
        if exception.search(text):
            flag = True
            break


    if flag:
        return text, "document"

    # Solve cases
    if text_.startswith("Caso"):
        Filter = Query()
        if "serie" in attrib:
            doc = db.get(Filter.meta_name.number.search(attrib['serie']))
            if doc:
                return str(doc.doc_id), "case_cidh"
        elif "case" in attrib:
            case_name=str(attrib["case"])
            case_name=case_name.replace("(","\(")
            case_name=case_name.replace(")","\)")
            doc = db.get(Filter.meta_name.name.search(case_name))
            if doc:
                return str(doc.doc_id), "case_cidh"


    # Solve definitions
    if definitions == 0:
        for defi in cntx.definitions_.keys():
            if text_.find(defi) >= 0:
                return cntx.definitions_[defi], cntx.t_definitions_[defi]
    for lower, red, res, t in reductions:
        if lower:
            m = red.match(text.lower())
        else:
            m = red.match(text)
        if m:
            return res, t
    m = re_fromltoc.match(text)
    if m:
        text = m.group('caption')
    return text, "document"


reductions = [
    (False, re.compile(r'mism[ao]'),
        'PENDING', "pending"),
    (False, re.compile(r'MISM[AO]'),
        'PENDING', "pending"),
    (False, re.compile(r'dicha Convención'),
        'Convención', "pending"),
    (False, re.compile(r'dich[oa]'),
        'PENDING', "pending"),
    (False, re.compile(r'presente'),
        'PENDING', "pending"),
    (False, re.compile(r'esta ley'),
        'PENDING', "pending"),
    (False, re.compile(r'Son'),
        'PENDING', "pending"),
    (False, re.compile(r'est[ae] últim[oa]'),
        'PENDING', "pending"),
    (False, re.compile(r'Convención [I|i]\w*'),
        'Convención Interamericana de Derechos Humanos', "document"),
    (False, re.compile(r'Convención [A|a]\w*'),
        'Convención Americana sobre Derechos Humanos', "document"),
    (False, re.compile(r'RAAN'),
        'Regiones Autónomas del Atlántico Norte', "institution"),
    (False, re.compile(r'MARENA'),
        'Ministerio del Ambiente y Recursos Naturales de Nicaragua',
        "instiution"),
    (False, re.compile(r'RAAS'),
        'Regiones Autónomas del Atlántico Sur', "institution"),
    (False, re.compile(r'CONVENCIÓN [I|i]\w*'),
        'Convención Interamericana de Derechos Humanos', "document"),
    (False, re.compile(r'CONVENCIÓN [A|a]\w*'),
        'Convención Americana de Derechos Humanos', "document"),
    (False, re.compile(r'Estatuto.*(corte)*'),
        'Estatuto de la Corte', "document"),
    (False, re.compile(r'^Reglamento$'),
        'Reglamento de la Corte', "document"),
    (False, re.compile(r'CP'),
        'Código Penal', 'document'),
    (False, re.compile(r'CIDFP'),
        'Convención Interamericana sobre Desaparición Forzada de Personas',
        'document'),
    (False, re.compile(r'Ley 14'),
        'Código de Justicia Miliar Ley 14.029', "document"),
    (False, re.compile(r'CJM'),
        'Comisión de Justicia Militar', "document"),
    (False, re.compile(r'OEA'),
        'Organización de Estados Americanos', "institutions"),
    (False,
     re.compile(
       r'^Sentencia de Excepción Preliminar, Fondo, Reparaciones y Costas.*'),
        'Sentencia de Excepción Preliminar, Fondo, Reparaciones y Costas',
        "document"),
    (False, re.compile(r'Reglamento establece'),
        'Reglamento de la Corte', "document"),
    (False, re.compile(r'de su Reglamento'),
        'Reglamento de la Corte', "document"),
]

exceptions = [
    re.compile(r"Caso.*"),
    re.compile(r".*.eglamento de la .omisi.n")
]
