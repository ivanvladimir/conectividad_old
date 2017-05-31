#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Extract sentences
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
from collections import Counter
import nltk, re, pprint
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import datetime
from tinydb import TinyDB, Query

# local libraries
from utils import pdf2text, extract_topics, search_regexp

sws=stopwords.words('spanish')
    
re_articulo=re.compile('[\d\.]+')
re_articulos=re.compile('art[íi]culos?')
re_recovery=re.compile('(artículos?|articulos?) (?P<articles>.+?) (de la|del|de su) (?P<source>.*)[,.]')
re_numbers=re.compile('[\d.]+')
re_source=re.compile('(mism[oa]|[^,:()]+)')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# MAIN
if __name__ == "__main__":
    # Command line options

    p = argparse.ArgumentParser(description="Download files")
    p.add_argument("--re_selector",
            default=".*", type=str,
            action="store", dest="re_selector",
            help="ER to select files")
    p.add_argument("--dbname",
            default="data/DB.json", type=str,
            action="store", dest="dbname",
            help="Name for the db file")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")
 

    # Parsing commands line arguments
    args = p.parse_args()

    # Defining verbose function
    if args.verbose:
       def verbose(*args):
            print(*args)
    else:   
        verbose = lambda *a: None  

    verbose("Connecting to DB:",args.dbname)
    db = TinyDB(args.dbname)
    contensiosos = db.table('contensiosos')

    re_selector=re.compile(args.re_selector)

    # Initialization counting
    Filter = Query()
    mentions=[]
    for case in contensiosos.search(Filter.title.search(re_selector)):
        verbose('Analysing ',case['title'])
        with open(case['txt']) as text:
            doc=text.read()
        sentences = sent_tokenize(doc)
        for sentence in sentences:
            sentence_original=sentence.replace('\n',' ')
            verbose(bcolors.OKBLUE +'> Sentence '+ bcolors.ENDC ,sentence_original)
            sentence_lower=sentence_original.lower()
            m=re_articulo.search(sentence_lower)
            if m:
                verbose(bcolors.OKGREEN +'> Candidate '+ bcolors.ENDC ,sentence_lower)
                starts=[]
                for m in re_articulos.finditer(sentence_lower):
                    start,end=m.span()
                    starts.append(start)
                starts.append(len(sentence_lower))

                segs=zip(starts[:-1],starts[1:])
                for ini,fin in segs:
                    bit=sentence_lower[ini:fin]
                    m=re_recovery.search(bit)
                    if not m:
                        continue
                    start,end=m.span()
                    m_=re_source.search(m.group('source'))
                    

                    source=m_.group(0)
                    articles=re_numbers.findall(m.group('articles'))
                    mentions.append((source.strip(),articles))

hist_sources=Counter([x for x,y in mentions])

for x,y in hist_sources.most_common():
    print(y,x)


