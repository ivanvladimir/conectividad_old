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

    def info(self):
        res = {}
        if self.section:
            res["secction"]=str(self.section)
        if self.paragraph:
            res["paragraph"]=str(self.paragraph)
        if self.page:
            res["page"]=str(self.page)
        if len(self.footnotes):
            res["open_footnotes"]=str(", ".join(list(self.footnotes)))
        return res



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
    par_ = ET.Element("paragraph")
    par_.text = par.text
    par_.tail = par.tail
    flag=False
    prev=None
    for child in par:
        if child.tag == "Articles":
            if flag:
                prev.tail+=child.text+child.tail
            else:
                par_.text+=child.text+child.tail
        else:
            par_.append(child)
            flag=True
        prev=child
    return par_


def add_tags(par, info_tags, total=0, offset=0,parent=None):
    if len(info_tags) <= total:
        return par,total,offset
    par_ = ET.Element(par.tag)
    o_text = par.text
    cur = o_text
    prev_tag = None
    prev_span_end = None
    ## Check the text
    for ii, (span, tag, info) in enumerate(info_tags[total:]):
        if o_text is None or span[1] >= len(o_text):
            continue
        middle = o_text[span[0]-offset:span[1]-offset]
        tag = ET.Element(tag, **info)
        tag.text = middle
        par_.append(tag)
        if ii == 0:
            cur = o_text[:span[0]-offset]
        else:
            prev_tag.tail = o_text[prev_span_end:span[0]-offset]
        prev_span_end = span[1]-offset
        prev_tag = tag
        prev_tag.tail = o_text[prev_span_end:span[0]-offset]
        total += 1
    par_.text = cur
    if o_text:
        offset+=len(o_text)
    o_text= par.tail
    cur = o_text
    for ii, (span, tag, info) in enumerate(info_tags[total:]):
        if o_text is None or span[1] >= offset+len(o_text):
            continue
        middle = o_text[span[0]-offset:span[1]-offset]
        tag = ET.Element(tag, **info)
        tag.text = middle
        if parent:
            parent.append(tag)
        else:
            par.append(tag)
        if ii == 0:
            cur = o_text[:span[0]-offset]
        else:
            prev_tag.tail = o_text[prev_span_end:span[0]-offset]
        prev_span_end = span[1]-offset
        prev_tag = tag
        prev_tag.tail = o_text[prev_span_end:span[0]-offset]
        total += 1
    par_.tail = cur

    # Check the children
    for element in par:
        tag_,total,offset = add_tags(element, info_tags[total:],total=total,offset=offset,parent=par)
        par_.append(tag_)
    return par_,total,offset


def process_articles(par, cntx):
    arts = test_articles(par, cntx)
    tags = []
    for idd, art in enumerate(arts):
        info_art=cntx.info()
        info_doc=cntx.info()
        info_art['idd'] = str(idd)
        info_doc['idd'] = str(idd)
        tags.append((art[0], 'ArticleMention', info_art))
        tags.append((art[1], 'DocumentMention', info_doc))
    par_,_,_ = add_tags(par, tags)
    return par_

def label_xml(root):
    cntx = Context()
    for par in root.findall('.//paragraph'):
        verbose(fg.BLUE, "Context: ", fg.BLUE, cntx)
        verbose(fg.YELLOW, "Raw text: ",
                style.RESET, "".join([x for x in par.itertext()]))
        par = preprocess_paragraph(par)
        # Eliminates article tags
        get_context(par, cntx)
        par_ = process_articles(par, cntx)
        for art in par_.findall('.//DocumentMention'):
            verbose(fg.GREEN, "Document: ",
                style.RESET, "".join([x for x in art.itertext()]))


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
