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

re_enters=re.compile(r"\n+")
re_spaces=re.compile(r"\s+")
re_fromltoc=re.compile(r"^[a-z ]+(?P<caption>[A-Z]+.*)")

def resolve_document(text,cntx):
    text = re_enters.sub(" ",text)
    text = re_spaces.sub(" ",text)
    for lower,red,res in reductions:
        if lower:
            m = red.match(text.lower())
        else:
            m = red.match(text)
        if m:
            return res
    m = re_fromltoc.match(text)
    if m:
        text=m.group('caption')
    return text


reductions=[
    (False, re.compile('mism[ao]'),
        'PENDING'),
    (False, re.compile('MISM[AO]'),
        'PENDING'),
    (False, re.compile('dicha Convención'),
        'Convención'),
    (False, re.compile('dich[oa]'),
        'PENDING'),
    (False, re.compile('presente'),
        'PENDING'),
    (False, re.compile('esta ley'),
        'PENDING'),
    (False, re.compile('Son'),
        'PENDING'),
    (False, re.compile('est[ae] últim[oa]'),
        'PENDING'),
    (False, re.compile('Convención [I|i]\w*'),
        'Convención Interamericana de Derechos Humanos'),
    (False, re.compile('Convención [A|a]\w*'),
        'Convención Americana sobre Derechos Humanos'),
    (False, re.compile('RAAN'),
        'Regiones Autónomas del Atlántico Norte'),
    (False, re.compile('MARENA'),
        'Ministerio del Ambiente y Recursos Naturales de Nicaragua'),
    (False, re.compile('RAAS'),
        'Regiones Autónomas del Atlántico Sur'),
    (False, re.compile('CONVENCIÓN [I|i]\w*'),
        'Convención Interamericana de Derechos Humanos'),
    (False, re.compile('CONVENCIÓN [A|a]\w*'),
        'Convención Americana de Derechos Humanos'),
    (False, re.compile('Estatuto.*(corte)*'),
        'Estatuto de la Corte'),
    (True,  re.compile('reglamento.*tribunal'),
        'Reglamento de la Corte'),
    (False, re.compile('Reglamento.*(corte)*'),
        'Reglamento de la Corte'),
    (False, re.compile('CP'),
        'Código Penal'),
    (False, re.compile('CIDFP'),
        'Convención Interamericana sobre Desaparición Forzada de Personas'),
    (False, re.compile('Ley 14'),
        'Código de Justicia Miliar Ley 14.029'),
    (False, re.compile('CJM'),
        'Comisión de Justicia Militar'),
]
   

