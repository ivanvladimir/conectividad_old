#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Label sentences
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2017/IIMAS/UNAM
# ----------------------------------------------------------------------

# System libraries
import argparse
import os.path
import re
from tinydb import TinyDB, Query
import xml.etree.ElementTree as ET


re_enters=re.compile(r"\n+")
re_espaces=re.compile(r"\s+")
words=["de","la","y"]
words_options="|".join([r"{0}[\n ]".format(w) for w in words])
#re_capitals_words = re.compile('[A-Z]\w+[\n ]([A-Z][a-zñ]+[\n ]|{0})+'.format(words_options))
re_capitals_words = re.compile('[A-Z]\w+[\n ]([A-Z]\w+[\n ]|[a-zñ]{0,6}[\n ]|Vs\.[\n ])*[A-Z]\w+')

class fg:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[39m'


class bg:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'
    RESET = '\033[49m'


class style:
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    NORMAL = '\033[22m'
    RESET = '\033[0m'


# MAIN
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser(description="Extracti articles")
    p.add_argument("--re_selector",
                   default=".*", type=str, action="store", dest="re_selector",
                   help="ER to select files")
    p.add_argument("--dbname",
                   default="data/DB.json", type=str,
                   action="store", dest="dbname",
                   help="Name for the db file")
    p.add_argument("--annotated_dir",
                   default="data/annotatedDocuments", type=str,
                   action="store", dest="annotated_dir",
                   help="Directory with the annotated documents")
    p.add_argument("--output",
                   default="data/ner_capitals.txt", type=str,
                   action="store", dest="output",
                   help="File with the list")
 
    p.add_argument("-v", "--verbose",
                   action="store_true", dest="verbose",
                   help="Verbose mode [Off]")

    # Parsing commands line arguments
    args = p.parse_args()

    # Defining verbose function
    if args.verbose:
        def verbose(*args):
            print(args[0], end="", sep="")
            print(args[1], end="", sep="")
            print(style.NORMAL, end="")
            for a in args[2:]:
                print(a, end="")
            print(style.RESET)
    else:
        def verbose(*args):
            return None

    # Connecting to DB
    verbose(style.BRIGHT, "Connecting to DB: ", args.dbname)
    db = TinyDB(args.dbname)
    contensiosos = db.table('contensiosos')

    re_selector = re.compile(args.re_selector)

    # Initialization counting
    Filter = Query()

    phrases=set()
    for case in contensiosos.search(Filter.title.search(re_selector)):
        # Loading the XML file
        xmlinfilename = os.path.join(args.annotated_dir,
                                     os.path.basename(case['txt']) + ".xml")
        verbose(style.BRIGHT, 'Analysing ', case['txt'])
        verbose(style.BRIGHT, 'Looking for ', xmlinfilename)
        try:
            with open(xmlinfilename, "r") as file:
                xmltxt = file.read()
            root = ET.fromstring('<root>\n'+xmltxt+"\n</root>")
        except FileNotFoundError:
            verbose(fg.RED + 'ARCHIVO FALTANTE', style.NORMAL, xmlinfilename)
            continue

        
        for par in root.findall('.//paragraph'):
                verbose(fg.YELLOW, "")
                text="".join([x for x in par.itertext()])
                text= re_enters.sub(" ",text)
                text= re_espaces.sub(" ",text)
                #verbose(fg.YELLOW, "Raw text: ",
                #        style.RESET, text)

                for m in re_capitals_words.finditer(text):
                    ner =  m.group()
                    if len(ner.split()) > 1:
                        verbose(fg.GREEN, "Frase: ",
                                style.RESET,ner)
                        phrases.add(ner)
    print("size",len(phrases))
    phrases=sorted(phrases)
    ofile= open(args.output,"w")
    for phrase in phrases:
        print(phrase,file=ofile)
    ofile.close()


