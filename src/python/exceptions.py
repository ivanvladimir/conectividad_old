#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Triggers for files
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2017/IIMAS/UNAM
# ----------------------------------------------------------------------

import re

footnotementions = [
    ('resolutiva 4.', 4),
    ('decisión 6,', 6),
    ('oportunamente 8.', 8),
]

institutions = [
    "Corte Interamericana de Derechos Humanos",
    "Comisión Interamericana de Derechos Humanos",
    "Defensores Interamericanos",
    "República Argentina",
    "OEA",
    "Estados Unidos de América",
    "Gobierno de Honduras",
    "Universidad Nacional Autónoma de Honduras"
]

documents = [
    "Fondo de Asistencia Legal de Víctimas de la Corte Interamericana",
    "Fondo de Asistencia Legal de Víctimas",
]

avoid_defs_arts = [
    ", en los términos del artículo 50 de la Convención Americana"
]

avoid_defs_mentions = [
    ", en los términos del artículo 50 de la Convención Americana"
]
