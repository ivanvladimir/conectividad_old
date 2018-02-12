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

re_enters = re.compile(r"\n+")
re_spaces = re.compile(r"\s+")
re_fromltoc = re.compile(r"^[a-z ]+(?P<caption>[A-Z]+.*)")


def resolve_document(text, cntx):
    text = re_enters.sub(" ", text)
    text = re_spaces.sub(" ", text)
    if text in cntx.definitions_:
        return cntx.definitions_[text]

    for lower, red, res in reductions:
        if lower:
            m = red.match(text.lower())
        else:
            m = red.match(text)
        if m:
            return res
    m = re_fromltoc.match(text)
    if m:
        text = m.group('caption')
    return text


reductions = [
    (False, re.compile(r'mism[ao]'),
        'PENDING'),
    (False, re.compile(r'MISM[AO]'),
        'PENDING'),
    (False, re.compile(r'dicha Convención'),
        'Convención'),
    (False, re.compile(r'dich[oa]'),
        'PENDING'),
    (False, re.compile(r'presente'),
        'PENDING'),
    (False, re.compile(r'esta ley'),
        'PENDING'),
    (False, re.compile(r'Son'),
        'PENDING'),
    (False, re.compile(r'est[ae] últim[oa]'),
        'PENDING'),
    (False, re.compile(r'Convención [I|i]\w*'),
        'Convención Interamericana de Derechos Humanos'),
    (False, re.compile(r'Convención [A|a]\w*'),
        'Convención Americana sobre Derechos Humanos'),
    (False, re.compile(r'RAAN'),
        'Regiones Autónomas del Atlántico Norte'),
    (False, re.compile(r'MARENA'),
        'Ministerio del Ambiente y Recursos Naturales de Nicaragua'),
    (False, re.compile(r'RAAS'),
        'Regiones Autónomas del Atlántico Sur'),
    (False, re.compile(r'CONVENCIÓN [I|i]\w*'),
        'Convención Interamericana de Derechos Humanos'),
    (False, re.compile(r'CONVENCIÓN [A|a]\w*'),
        'Convención Americana de Derechos Humanos'),
    (False, re.compile(r'Estatuto.*(corte)*'),
        'Estatuto de la Corte'),
    (False, re.compile(r'^Reglamento$'),
        'Reglamento de la Corte'),
    (False, re.compile(r'CP'),
        'Código Penal'),
    (False, re.compile(r'CIDFP'),
        'Convención Interamericana sobre Desaparición Forzada de Personas'),
    (False, re.compile(r'Ley 14'),
        'Código de Justicia Miliar Ley 14.029'),
    (False, re.compile(r'CJM'),
        'Comisión de Justicia Militar'),
    (False,
     re.compile(
       r'^Sentencia de Excepción Preliminar, Fondo, Reparaciones y Costas.*'),
        'Sentencia de Excepción Preliminar, Fondo, Reparaciones y Costas'),

]
