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
        meta = re.split('(?<!Vs|No)\. ', title)
        verbose(meta)
        court = ""
        involved = ""
        name = ""
        actions = ""
        date_sentence = ""
        number = ""
        error = "No"
        #   Try to get metadata
        try:
            court = meta[0]
            involved = re.split(' Vs\. ',meta[1])   # Separamos la cadena en dos, por ahora no hay mas involucrados
            involved[0] = re.sub('(Caso )', '', involved[0])    #   Retiramos la palabra Caso del inicio
                                                                # no se han presentado otras palabras a retirar
            name = meta[1]
            actions = meta[2]
            date_sentence = re.search('\d{1,2}[a-zA-Z ]*\d{4}',meta[3]).group(0)    #   Obtenemos solamente la fecha
            number = meta[4][:len(meta[4]) - 1] #   Retiramos el punto del final, no pertenece al dato.
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
            court = "N\A"
            involved[0] = "N\A"
            involved.append("N\A")
            name = "N\A"
            actions = "N\A"
            date_sentence = "N\A"
            number = "N\A"
            error = "Yes"
            update_contenciosos(contensiosos, case, court, involved, name, actions, date_sentence, number, error)
        #   End except
    #   End for

    print("Errors: %s" % error_counter)
