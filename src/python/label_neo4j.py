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
from collections import Counter, OrderedDict
import json
from py2neo import Graph, Node, Relationship
import config
import sys

re_year = re.compile("\d\d\d\d")
re_pais = re.compile(r".*\.([^.]*)$")


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





def build_graph(data,id2title):
    nodes=[]
    nodes_={}
    for idd,(name,node) in enumerate(data[0].items()):
        if 'type' in node and node['type']=="institution":
            continue
        nodes.append({"name":name,
                      "id":idd,
                      "type":2})
        for k,v in node.items():
            nodes[-1][k]=v

        nodes_[name]=idd

    len_nodes=len(nodes)
    for idd,(name,node) in enumerate(data[2].items()):
        if 'type' in node and node['type']=="institution":
            continue
        bits=name.split(":",2)
        nodes.append({"name":name,
                      "doc":bits[0],
                      "art":bits[1],
                      "id":idd+len_nodes,
                      "type":3})
        nodes_[name]=idd+len_nodes

    links=[]
    linked = set()
    for d1,c in data[1].items():
        for d2,val in c.items():
            if val > 0:
                ori_val=val
                tpe = "normal"
                if d2[1]=="case_cidh":
                    target=nodes_[id2title[d2[0]]]
                    val=val*50
                    tpe = "cidh"
                else:
                    target=nodes_[d2[0]]
                links.append({"source":nodes_[d1],
                              "target":target,
                              "value":val,
                              "ori_val":ori_val,
                              "type": tpe
                             })
                linked.add(nodes_[d1])
                linked.add(target)

    for d1,c in data[3].items():
        for d2,val in c.items():
            if val > 0:
                ori_val=val
                tpe = "artcle"
                target=nodes_["{0}:{1}".format(d2[0],d2[2])]
                links.append({"source":nodes_[d1],
                              "target":target,
                              "value":val,
                              "ori_val":ori_val,
                              "type": tpe
                             })
                linked.add(nodes_[d1])
                linked.add(target)

    for node in nodes:
        if not 'id' in node:
            print(node)

    return None

def get_info_node(doc,artn=None):
    if  artn:
        return (
            doc.attrib['name'],
            doc.attrib['type'],
            artn
        )
    else:
        return (
            doc.attrib['name'],
            doc.attrib['type']
        )


def extract_graph(root,graph,case,data):
    node_case=Node("Case",**data[0][case['title']])
    graph.create(node_case)
    for par in root.findall('.//paragraph'):
        # Shows some labelling in the document
        for doc in par.findall('.//DocumentMention'):
            if not doc.attrib['type']=="case_cidh":
                node_document=Node("Document",**doc.attrib)
                graph.create(node_document)
                cite=Relationship(node_case,'CITES',node_document)
                graph.create(cite)

            for art in par.findall('.//ArticleMention[@document="{0}"]'
                                    .format(doc.attrib['id'])):
                for artn in art.attrib['articles'].split():
                    node_article=Node("Article",**art.attrib)
                    graph.create(node_article)
                    mention=Relationship(node_document,'MENTION',node_article)
                    graph.create(mention)

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
                   default="bolt://127.0.0.1:7687", type=str,
                   action="store", dest="graph",
                   help="Graph db")
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

    # Loading grpah
    graph = Graph(args.graph, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))


    # Connecting to DB
    verbose(style.BRIGHT, "Connecting to DB: ", args.dbname)
    db = TinyDB(args.dbname)
    contensiosos = db.table('contensiosos')

    re_selector = re.compile(args.re_selector)

    # Initialization counting
    Filter = Query()

    # load graph into data
    data=(OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict())

    # Polulate data with names
    filter_new_cases=set()
    id2title={}
    for idd,case in enumerate(contensiosos.search(Filter.title.search(re_selector))):
        if case['title'] in data[0]:
            continue
        filter_new_cases.add(case['title'])
        m = re_year.search(case['title'])
        if m:
             year=m.group(0)
        m=re_pais.match(case['meta_name']['name'])
        pais="unknown"
        if m:
            pais=m.group(1).strip()
        data[0][case['title']]={'year':year}
        data[0][case['title']]['type']=1
        data[0][case['title']]['case_id']=case.doc_id
        data[0][case['title']]['country']=pais.lower()
        data[0][case['title']]['name']=case['meta_name']['name']
        id2title[str(case.doc_id)]=case['title']

    graph.delete_all()

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

        data=extract_graph(root,graph,case,data)

