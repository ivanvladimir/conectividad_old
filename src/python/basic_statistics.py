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
from collections import Counter
import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import stopwords
import datetime
from tinydb import TinyDB, Query

# local libraries
from utils import pdf2text, extract_topics, search_regexp

sws=stopwords.words('spanish')

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
            print("".join([str(x) for x in args]),file=sys.stderr)
    else:
        verbose = lambda *a: None

    verbose("Connecting to DB:",args.dbname)
    db = TinyDB(args.dbname)
    contensiosos = db.table('contensiosos')

    re_selector=re.compile(args.re_selector)

    # Initialization counting
    raws=[]
    tokens=[]
    texts=[]
    titles=[]
    vocab=Counter()

    graph={'nodes':[],'edges':[]}
    idg=0;
    Filter = Query()
    for case in contensiosos.search(Filter.title.search(re_selector)):
        verbose('Analysing ',case['title'])
        with open(case['txt']) as text:
            titles.append(case['title'])
            graph['nodes'].append({'title':case['title'],'id':'d'+str(idg)})
            idg+=1
            raws.append(text.read())
            tokens.append(word_tokenize(raws[-1]))
            texts.append(nltk.Text(tokens[-1]))
            vocab.update([w.lower() for w in tokens[-1]])

    print("Número total de documentos       : {0}".format(len(raws)))
    print("Longitud promedia de documentos  : {0:10.2f} (caracteres)".format(sum([len(x) for x in raws])/len(raws)))
    print("Longitud promedia de documentos  : {0:10.2f} (líneas)".format(sum([len(x.split('\n')) for x in raws])/len(raws)))

    print("Número total de palabras (token) : {0}".format(sum(vocab.values())))
    print("Número total de palabras (type)  : {0}".format(len(vocab.keys())))

    i=0
    xs=[]
    ws=[]
    for w,c in vocab.most_common():
        if w not in sws and w not in [',','.','(',')','[',']',';','...',':']:
            if i<20:
                xs.append(w)
                ws.append(c)
            if i>40:
                break
            print("  {0:30s} : {1}".format(w,c))
            i+=1

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    rects1 = ax.bar(range(len(xs)), ws, color='b')
    plt.xticks(range(len(xs)), xs, rotation='vertical')
    plt.subplots_adjust(bottom=0.30)
    plt.savefig('vocabulario.png')


    mentions_articulo=Counter()
    for i,text in enumerate(texts):
        verbose('Analysing ',titles[i])
        mash = nltk.text.TokenSearcher(text)
        pattern = mash.findall('(<artículo> <\d+>)')
        mentions_articulo.update([(i,"{0}".format(x[1])) for x in pattern])

    print('Total de menciones de artículos', sum(mentions_articulo.values()))
    art2id={}
    for (i,w),c in mentions_articulo.most_common():
        if i < 20:
            print("  {0:30s} : {1}".format(w,c))
        try:
            tar=art2id[w]
        except KeyError:
            art2id[w]='a'+w
            graph['nodes'].append({'title':w,'id':'a'+w})
            tar='a'+w
            idg+=1
        graph['edges'].append({
                    'source':'d'+str(i),
                    'target':tar
                })


    with open(os.path.join("./","graph.graphml"), 'w') as outfile:
        print('<?xml version="1.0" encoding="UTF-8"?>',file=outfile)
        print('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"',file=outfile)
        print('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',file=outfile)
        print('xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns',file=outfile)
        print('http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">',file=outfile)
        print('<graph id="G" edgedefault="directed">',file=outfile)
        for node in graph['nodes']:
            print('<node id="{0}"/>'.format(node['id']),file=outfile)
        for edge in graph['edges']:
            print('<edge source="{0}" target="{1}"/>'.format(edge['source'],edge['target']),file=outfile)
        print('</graph>',file=outfile)
        print('</graphml>',file=outfile)

    extract_topics(raws,sws=sws)
