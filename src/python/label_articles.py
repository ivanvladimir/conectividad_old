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
from triggers import test_format, test_articles


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


# Section, paragraph
class Context:
    def __init__(self):
        self.section = "Preamble"
        self.paragraph = None
        self.page = None
        self.part = None
        self.footnotes = set([])
        self.footnotes_ = set([])

    def add_footnotes(self, fns):
        for fn in fns:
            if fn < len(self.footnotes_)+5:
                if not str(fn) in self.footnotes_:
                    self.footnotes.add(str(fn))
                    self.footnotes_.add(str(fn))

    def footnote(self, fns):
        for fn in fns:
            if fn in self.footnotes:
                self.footnotes.remove(fn)

    def __str__(self):
        res = []
        if self.section:
            res.append("Sec. "+str(self.section))
        if self.paragraph:
            res.append("par. "+str(self.paragraph))
        if self.page:
            res.append(" pp. "+str(self.page))
        if len(self.footnotes):
            res.append("\nfn. "+str(", ".join(list(self.footnotes))))
        if len(res) == 0:
            res = ["Empty"]
        return ", ".join(res)


def get_context(par, cntx):
    results = test_format(par)
    for res in results:
        if res[0] is None:
            return None
        if res[0].startswith('namesection'):
            cntx.section = res[1]
        elif res[0].startswith('numericalindex'):
            cntx.paragraph = res[1]
        elif res[0].startswith('pagenumber'):
            cntx.page = res[1]
        elif res[0].startswith('footnotemention'):
            cntx.add_footnotes(res[1])
        elif res[0].startswith('footnote'):
            cntx.footnote(res[1])


def preprocess_paragraph(par):
    for art in par.findall('./Articles'):
        ntext = art.text+art.tail
        par.remove(art)
        if par.text:
            par.text += ntext
        else:
            par.text = ntext
    return par


def process_articles(par, cntx):
    arts = test_articles(par, cntx)
    for art in arts:
        verbose(fg.GREEN, "article: ", fg.GREEN, art)



def label_xml(root):
    cntx = Context()
    for par in root.findall('.//paragraph'):
        verbose(fg.YELLOW, "Raw text: ",
                style.RESET, "".join([x for x in par.itertext()]))
        # Eliminates article tags
        get_context(par, cntx)
        par = preprocess_paragraph(par)
        process_articles(par, cntx)
        verbose(fg.BLUE, "Context: ", fg.BLUE, cntx)


# MAIN
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser(description="Extracti articles")
    p.add_argument("--re_selector",
                   default=".*", type=str, action="store", dest="re_selector",
                   help="ER to select files")
    p.add_argument("--annotated_dir",
                   default="data/annotatedDocuments", type=str,
                   action="store", dest="annotated_dir",
                   help="Directory with the annotated documents")
    p.add_argument("--output_dir",
                   default="data/labelledDocuments", type=str,
                   action="store", dest="labelled_dir",
                   help="Directory with the resulting documents")
    p.add_argument("--dbname",
                   default="data/DB.json", type=str,
                   action="store", dest="dbname",
                   help="Name for the db file")
    p.add_argument("--graph",
                   default="data/graph.json", type=str,
                   action="store", dest="graph",
                   help="Name for the grap file")
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

        label_xml(root)

        ## Writing out the XML
        xmloutfilename = os.path.join(args.labelled_dir,
                                      os.path.basename(case['txt']) + ".xml")

        verbose(style.BRIGHT, 'Saving file ', xmloutfilename)
        ET.ElementTree(root).write(xmloutfilename)
