#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Analyses texts
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2017/IIMAS/UNAM
# ----------------------------------------------------------------------

# System libraries
import argparse
import sys
import os.path
import requests
import json
import re
from tinydb import TinyDB, Query
import datetime


# local libraries
from utils import extract_text_from_pdf

# MAIN
if __name__ == "__main__":
    # Command line options

    p = argparse.ArgumentParser(description="Download files")
    p.add_argument("--dbname",
            default="data/DB.json", type=str,
            action="store", dest="dbname",
            help="Name for the db file")
    p.add_argument("--odir",
            default="data/contenciosos/", type=str,
            action="store", dest="odir",
            help="File where to download data")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")

    # Parsing commanls line arguments
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


    for case in contensiosos.all():
        h,t=os.path.split(case['pdf'])
        ofilename=os.path.join(args.odir,t.replace('.pdf','.txt'))
        verbose('Extracting text from ',case['pdf'], ' into ', ofilename)
        extract_text_from_pdf(case['pdf'],ofilename)
        contensiosos.update({'txt':ofilename,'date_modification':datetime.datetime.now().isoformat(' ')},eids=[case.eid])
