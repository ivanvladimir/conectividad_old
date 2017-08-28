#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Extract metadata from "title"
# ----------------------------------------------------------------------
# Paul Sebastian Aguilar Enriquez/ penserbjorne at the world
# 04-2017/FI-IIMAS/UNAM
# ----------------------------------------------------------------------

# System libraries
import argparse
import sys
import os.path
import os
import requests
from bs4 import BeautifulSoup
import json
import datetime
from tinydb import TinyDB, Query
import re

#   Update node in contensiosos
def update_contenciosos(contensiosos, case, court, involved, name, actions, date_sentence, number, error):
    contensiosos.update(  # Actualizamos
        {
            'date_modification': datetime.datetime.now().isoformat(' '),
            'meta_name': {
                'court': court,
                'involved': {
                    'involved_a': involved[0],
                    'involved_b': involved[1]
                },
                'name': name,
                'actions': actions,
                'date_sentence': date_sentence,
                'number': number,
                'error' : error
            }
        },
        eids=[case.eid]
    )
    return

# MAIN
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser(description="Extract metadata from \"title\"")
    p.add_argument("--dbname",
            default="data/DB.json", type=str,
            action="store", dest="dbname",
            help="Name for the db file")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
    p.add_argument("-i", "--interactive",
            action="store_true", dest="interactive",
            help="Interactive mode for errors [Off]")
    # Parsing commands line arguments
    args = p.parse_args()

    # Defining verbose function
    if args.verbose:
       def verbose(*args):
            print("".join([str(x) for x in args]),file=sys.stderr)
    else:   
        verbose = lambda *a: None

    #   Connecting to database
    verbose("Connecting to DB:",args.dbname)
    db = TinyDB(args.dbname)
    #   Selecting table
    contensiosos = db.table('contensiosos')

    error_counter = 0

    # Begin for
    for case in contensiosos.all():
        title = case['title']
        verbose('-->\nExtracting data from : ',title)
        meta = re.split('(?<!(Vs|No))\. ', title)
        verbose(meta)
        court = "N\A"
        involved = []
        involved.append("N\A")
        involved.append("N\A")
        name = "N\A"
        actions = "N\A"
        date_sentence = "N\A"
        number = "N\A"
        error = "Yes"
        #   Try to get metadata , this should break ;@ need a better method, sorry ;@
        try:
            if len(meta) == 11:
                # Vs. separado
                court = meta[0]
                name = meta[2] + ". " + meta[4]
                involved[0] = re.sub('(Caso )', '', meta[2]) + "."  # Retiramos la palabra Caso del inicio
                                                                    # no se han presentado otras palabras a retirar
                involved[1] = re.sub('(Vs\. )', '', meta[4])  # Retiramos la palabra Vs. del inicio
                actions = meta[6]
                date_sentence = re.search('\d{1,2}[a-zA-Z ]*\d{4}', meta[8]).group(0)  # Obtenemos solamente la fecha
                number = meta[10][:len(meta[10]) - 1]  # Retiramos el punto del final, no pertenece al dato.
            elif len(meta) == 9:
                if meta[8].__contains__("Sentencia") and meta[8].__contains__("Serie"):
                    # Vs. separado pero ...
                    # ... no existe punto final/separador en la fecha de la sentencia
                    court = meta[0]
                    name = meta[2] + ". " + meta[4]
                    involved[0] = re.sub('(Caso )', '', meta[2]) + "."  # Retiramos la palabra Caso del inicio
                    # no se han presentado otras palabras a retirar
                    involved[1] = re.sub('(Vs\. )', '', meta[4])  # Retiramos la palabra Vs. del inicio
                    actions = meta[6]

                    temp = re.split(' Serie ', meta[8])  # Separamos la cadena en dos
                    date_sentence = re.search('\d{1,2}[a-zA-Z ]*\d{4}', temp[0]).group(0)  # Obtenemos solamente la fecha
                    number = "Serie " + temp[1][:len(temp[1]) - 1]  # Retiramos el punto del final, no pertenece al dato.
                else:
                    # Vs. junto
                    court = meta[0]
                    name = meta[2]
                    involved = re.split(' Vs\. ', meta[2])  # Separamos la cadena en dos, por ahora no hay mas involucrados
                    involved[0] = re.sub('(Caso )', '', involved[0])  # Retiramos la palabra Caso del inicio
                                                                        # no se han presentado otras palabras a retirar
                    actions = meta[4]
                    date_sentence = re.search('\d{1,2}[a-zA-Z ]*\d{4}', meta[6]).group(0)  # Obtenemos solamente la fecha
                    number = meta[8][:len(meta[8]) - 1]  # Retiramos el punto del final, no pertenece al dato.
            elif len(meta) == 7:
                if meta[6].__contains__("Sentencia") and meta[6].__contains__("Serie"):
                    # Vs. Junto y con acciones, pero ...
                    # ... no existe punto final/separador en la fecha de la sentencia

                    court = meta[0]
                    name = meta[2]
                    involved = re.split(' Vs\. ', meta[2])  # Separamos la cadena en dos, por ahora no hay mas involucrados
                    involved[0] = re.sub('(Caso )', '', involved[0])  # Retiramos la palabra Caso del inicio
                                                                        # no se han presentado otras palabras a retirar
                    actions = meta[4]
                    temp = re.split(' Serie ',meta[6])  # Separamos la cadena en dos
                    date_sentence = re.search('\d{1,2}[a-zA-Z ]*\d{4}', temp[0]).group(0)  # Obtenemos solamente la fecha
                    number = "Serie " + temp[1][:len(temp[1]) - 1]  # Retiramos el punto del final, no pertenece al dato.
                else:
                    # Vs. junto y sin acciones
                    court = meta[0]
                    name = meta[2]
                    involved = re.split(' Vs\. ', meta[2])  # Separamos la cadena en dos, por ahora no hay mas involucrados
                    involved[0] = re.sub('(Caso )', '', involved[0])  # Retiramos la palabra Caso del inicio
                                                                        # no se han presentado otras palabras a retirar
                    actions = "No especificado."
                    date_sentence = re.search('\d{1,2}[a-zA-Z ]*\d{4}', meta[4]).group(0)  # Obtenemos solamente la fecha
                    number = meta[6][:len(meta[6]) - 1]  # Retiramos el punto del final, no pertenece al dato.

            error = "No"
            update_contenciosos(contensiosos, case, court, involved, name, actions, date_sentence, number, error)
        #   End try
        #   Begin except
        except:
            message = "**********Some error just happened :(*********\nPlease verify the partitioned data :/"
            error_counter += 1
            partitioned_data = \
                '\tcourt: %s\n' \
                '\tinvolved: %s\n' \
                '\tname: %s\n' \
                '\tactions: %s\n' \
                '\tdate_sentence: %s\n' \
                '\tnumber: %s'
            if args.interactive:
                print(message)
                if not args.verbose:
                    print (meta)
                print(partitioned_data % (court, involved, name, actions, date_sentence, number))
                input("Press Enter to continue...")
            elif args.verbose:
                verbose(message)
                verbose(partitioned_data % (court, involved, name, actions, date_sentence, number))
            update_contenciosos(contensiosos, case, court, involved, name, actions, date_sentence, number, error)
        #   End except
    #   End for

    print("Errors: %s" % error_counter)
