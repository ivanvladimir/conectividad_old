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
    r"Corte Interamericana de Derechos Humanos",
    r"Comisión Interamericana de Derechos Humanos",
    r"Defensores Interamericanos",
    r"República Argentina",
    r"República Federativa de Brasil",
    r"República de Brasil",
    r"República Honduras",
    r"OEA",
    r"Estados Unidos de América",
    r"Gobierno de Honduras",
    r"Universidad Nacional Autónoma de Honduras",
    r"Dirección Nacional de Investigación",
    r"Fuerzas Armadas de Honduras",
    r"Fuerza de Seguridad Pública",
    r"Centro por la Justicia y el Derecho Internacional",
    r"La Asociación Paz y Esperanza"
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
