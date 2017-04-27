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

    verbose("Connecting to DB:",args.dbname)
    db = TinyDB(args.dbname)
    contensiosos = db.table('contensiosos')

    error_counter = 0
    for case in contensiosos.all():
        title = case['title']
        verbose('-->\nExtracting data from : ',title)
        meta = re.split('(?<!Vs|No)\. ', title)
        verbose(meta)
        # Data fields
        court = ""
        involved = ""
        name = ""
        actions = ""
        date_sentence = ""
        number = ""
        try:
            court = meta[0]
            involved = re.split(' Vs\. ',meta[1])
            involved[0] = re.sub('(Caso )', '', involved[0])
            name = meta[1]
            actions = meta[2]
            date_sentence = re.search('\d{1,2}[a-zA-Z ]*\d{4}',meta[3]).group(0)
            number = meta[4][:len(meta[4]) - 1]
            contensiosos.update(
                {
                    'date_modification':datetime.datetime.now().isoformat(' '),
                    'meta_name': {
                        'court': court,
                        'involved': {
                            'involved_a': involved[0],
                            'involved_b': involved[1]
                        },
                        'name': name,
                        'actions' : actions,
                        'date_sentence': date_sentence,
                        'number': number
                    }
                },
                eids=[case.eid]
            )
        except:
            contensiosos.update(
                {
                    'date_modification': datetime.datetime.now().isoformat(' '),
                    'meta_name': {
                        'court': "N/A",
                        'involved': {
                            'involved_a': "N/A",
                            'involved_b': "N/A"
                        },
                        'name': "N/A",
                        'actions': "N/A",
                        'date_sentence': "N/A",
                        'number': "N/A"
                    }
                },
                eids=[case.eid]
            )
            message = "**********Some error just happened :(*********\nPlease verify the partitioned data :/"
            error_counter += 1
            if args.interactive:
                partitioned_data = \
                    '\tcourt: %s\n' \
                    '\tinvolved: %s\n' \
                    '\tname: %s\n' \
                    '\tactions: %s\n' \
                    '\tdate_sentence: %s\n' \
                    '\tnumber: %s'
                if not args.verbose:
                    print(message)
                    print(partitioned_data % (court, involved, name, actions, date_sentence, number))
                else:
                    verbose(message)
                    verbose(partitioned_data % (court, involved, name, actions, date_sentence, number))
                input("Press Enter to continue...")


        partitioned_data = \
            '\tcourt: %s\n' \
            '\tinvolved: %s\n' \
            '\tname: %s\n' \
            '\tactions: %s\n' \
            '\tdate_sentence: %s\n' \
            '\tnumber: %s'
        if not args.interactive:
            verbose(partitioned_data % (court, involved, name, actions, date_sentence, number))

    print("Errors: %s" % error_counter)
