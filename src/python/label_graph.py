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
from collections import Counter
import json


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


def build_graph(data):
    nodes=[]
    nodes_={}
    for idd,node in enumerate(data[0]):
        nodes.append({"name":node,
                      "id":idd,
                      "type":1})
        nodes_[node]=idd

    links=[]
    for d1,c in data[1].items():
        for d2,val in c.items():
            links.append({"source":nodes_[d1],
                          "target":nodes_[d2],
                          "value":val
                         })
    return {"links":links,
            "nodes":nodes}
        



def extract_graph(root,case,data):
    for par in root.findall('.//paragraph'):
        # Shows some labelling in the document
        for doc in par.findall('.//DocumentMention'):
            try:
                data[0][doc.attrib["name"]]+=1
            except KeyError:
                data[0][doc.attrib["name"]]=1
            try:
                data[1][case['title']].update([doc.attrib["name"]])
            except KeyError:
                data[1][case['title']]=Counter([doc.attrib["name"]])
    return data

# MAIN
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser(description="Extracti articles")
    p.add_argument("--re_selector",
                   default=".*", type=str, action="store", dest="re_selector",
                   help="ER to select files")
    p.add_argument("--labelled_dir",
                   default="data/labelledDocuments", type=str,
                   action="store", dest="labelled_dir",
                   help="Directory with the annotated documents")
    p.add_argument("--graph",
                   default="data/graph.json", type=str,
                   action="store", dest="graph",
                   help="Graph name")
    p.add_argument("--dbname",
                   default="data/DB.json", type=str,
                   action="store", dest="dbname",
                   help="Name for the db file")
    p.add_argument("-n", "--new",
                   action="store_true", dest="new",
                   help="New graph [Off]")
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
    # Loading grpah
    if not args.new:
        verbose(style.BRIGHT, "Graph: ", args.graph)
        with open(args.graph, 'r') as f:
            graph = json.load(f)

    re_selector = re.compile(args.re_selector)

    # Initialization counting
    Filter = Query()
    
    # load graph into data
    data=({},{})

    # Polulate data with names
    filter_new_cases=set()
    for case in contensiosos.search(Filter.title.search(re_selector)):
        if case['title'] not in data[0]:
            data[0][case['title']]=0
            filter_new_cases.add(case['title'])

    for case in contensiosos.search(Filter.title.search(re_selector)):
        if case['title'] not in filter_new_cases:
            continue
        # Loading the XML file
        xmlinfilename = os.path.join(args.labelled_dir,
                                     os.path.basename(case['txt']) + ".xml")
        verbose(style.BRIGHT, 'Analysing ', case['txt'])
        verbose(style.BRIGHT, 'Looking for ', xmlinfilename)
        try:
            with open(xmlinfilename, "r") as file:
                xmltxt = file.read()
            root = ET.fromstring('<root>\n'+xmltxt+"\n</root>")
        except FileNotFoundError:
            verbose(fg.RED + 'ARCHIVO FALTANTE: ', style.NORMAL, xmlinfilename)
            continue

        data=extract_graph(root,case,data)

    graph=build_graph(data)
    verbose(style.BRIGHT, "Saving updated graph: ", args.graph)
    with open(args.graph,'w') as outfile:
        json.dump(graph, outfile)



