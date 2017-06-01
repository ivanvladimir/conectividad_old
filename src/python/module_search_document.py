#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Search documents by words or phrase on "title"
# ----------------------------------------------------------------------
# Paul Sebastian Aguilar Enriquez/ penserbjorne at the world
# 05-2017/FI-IIMAS/UNAM
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
    p = argparse.ArgumentParser(description="Search documents by words or phrase on \"title\"")
    p.add_argument("--dbname",
            default="data/DB.json", type=str,
            action="store", dest="dbname",
            help="Name for the db file")
    p.add_argument("-w", "--words",
            default="", nargs='*',
            action="store", dest="words",
            help="Words to match, will search separately")
    p.add_argument("-p", "--phrase",
            default="", nargs='*',
            action="store", dest="phrase",
            help="Phrase to match")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
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

    #Busqueda por palabras

    # Si hay palabras procedemos a buscar
    if args.words :
        words = args.words
        #Begin
        for word in words:
            print("Palabra a buscar: %s" % word)
            print("Resultados:")

            # Creamos objeto para hacer los querys
            Doc = Query()

            # Realizamos la busqueda
            docs = contensiosos.search(Doc.title.search(word))
            i = 0

            # Begin for
            for case in docs:
                i += 1
                title = case['title']
                doc = case['doc']
                source_doc = case['source_doc']
                pdf = case['pdf']
                source_pdf = case['source_pdf']
                print ("-->\t" + title + "\n"
                    "\tDocumento: " + doc + "\n"
                    "\tFuente: " + source_doc + "\n"
                    "\tPDF: " + pdf + "\n"
                    "\tFuente: " + source_pdf + "\n"
                       )
                #   End for

            print("Resultados de \"" + word + "\": " + str(i))
        #End Begin
    else:   # No hubo palabras para buscar
        print("No hay palabras a buscar.")

    # Si hay frase procedemos a buscar
    if args.phrase:
        words = args.phrase

        phrase = " ".join(words)

        print("Frase a buscar: %s" % phrase)
        print("Resultados:")

        # Creamos objeto para hacer los querys
        Doc = Query()

        # Realizamos la busqueda
        docs = contensiosos.search(Doc.title.search(phrase))
        i = 0

        # Begin for
        for case in docs:
            i += 1
            title = case['title']
            doc = case['doc']
            source_doc = case['source_doc']
            pdf = case['pdf']
            source_pdf = case['source_pdf']
            print ("-->\t" + title + "\n"
                "\tDocumento: " + doc + "\n"
                "\tFuente: " + source_doc + "\n"
                "\tPDF: " + pdf + "\n"
                "\tFuente: " + source_pdf + "\n"
                )
            #   End for

        print("Resultados de \"" + phrase + "\": " + str(i))
    else:  # No hubo palabras para buscar
        print("No hay frase a buscar.")