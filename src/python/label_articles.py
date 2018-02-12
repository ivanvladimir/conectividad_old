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
from triggers import (test_format, test_articles, test_docs, test_institutions,
                      compatible_spans, flat_spans)
from cleaning import resolve_document, re_espace_or_enter, split_arts
from collections import Counter


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
        self.definitions = {}
        self.definitions_ = {}
        self.t_definitions_ = {}
        self.type = "normal"

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

    def escape_phrase(self, phrase):
        phrase = re_espace_or_enter.sub("[ \n]", phrase)
        return phrase

    def add_definition(self, doc, phrase, t):
        escaped_phrase = self.escape_phrase(phrase)
        try:
            self.definitions[doc].append(escaped_phrase)
        except KeyError:
            self.definitions[doc] = [escaped_phrase]
        self.definitions_[escaped_phrase] = doc
        self.t_definitions_[escaped_phrase] = t

    def __str__(self):
        res = []
        if self.section:
            res.append("Sec. "+str(self.section))
        if self.paragraph:
            res.append("par. "+str(self.paragraph))
        if self.page:
            res.append(" pp. "+str(self.page))
        # if len(self.footnotes):
        #     res.append("\nfn. "+str(", ".join(list(self.footnotes))))
        # if len(self.definitions):
        #     res.append("\n"+str(self.definitions))
        return ", ".join(res)

    def info(self):
        res = {}
        if self.section:
            res["secction"] = str(self.section)
        if self.paragraph:
            res["paragraph"] = str(self.paragraph)
        if self.page:
            res["page"] = str(self.page)
        if len(self.footnotes):
            res["open_footnotes"] = str(", ".join(list(self.footnotes)))
        if self.type:
            res["type"] = str(self.type)
        return res


def get_context(par, cntx):
    results = test_format(par)
    cntx.type = "normal"
    for res in results:
        if res[0] is None:
            return None
        if res[0].startswith('namesection'):
            if len(res[1]) > 0:
                cntx.section = res[1]
                cntx.type = "title"
        elif res[0].startswith('numericalindex'):
            if len(res[1]) > 0:
                cntx.paragraph = res[1]
                cntx.type = "normal"
        elif res[0].startswith('pagenumber'):
            if len(res[1]) > 0:
                cntx.page = res[1]
                cntx.type = "pagenumber"
        elif res[0].startswith('footnotemention'):
            if len(res[1]) > 0:
                cntx.add_footnotes(res[1])
                cntx.type = "normal"
        elif res[0].startswith('footnote'):
            if len(res[1]) > 0:
                cntx.footnote(res[1])
                cntx.type = "footnote"


def preprocess_paragraph(par):
    par_ = ET.Element("paragraph")
    par_.text = par.text
    par_.tail = par.tail
    prev = None
    for child in par:
        if child.tag == "Articles":
            if prev is not None:
                prev.tail += child.text + child.tail
            else:
                par_.text += child.text + child.tail
        elif child.tag == "Date2":
            if prev is not None:
                prev.tail += child.text + child.tail
            else:
                par_.text += child.text + child.tail
        elif child.tag == "Actions":
            if prev is not None:
                prev.tail += child.text
                if child.tail:
                    prev.tail += child.tail
            else:
                par_.text += child.text + child.tail
        else:
            par_.append(child)
            prev = child
    return par_


def add_tags(par, info_tags, offset=0, parent=None):
    if len(info_tags) == 0:
        return [par], info_tags, offset
    par_ = [ET.Element(par.tag)]
    o_text = par.text
    cur = o_text
    prev_tag = None
    prev_span_end = None
    # Check the text
    first = True
    while len(info_tags) > 0:
        span, tag, info = info_tags[0]
        if o_text is None or span[1] >= len(o_text):
            break
        middle = o_text[span[0]-offset:span[1]-offset]
        tag = ET.Element(tag, **info)
        tag.text = middle
        par_[0].append(tag)
        if first:
            cur = o_text[:span[0]-offset]
            first = False
        else:
            prev_tag.tail = o_text[prev_span_end:span[0]-offset]
        prev_span_end = span[1]-offset
        prev_tag = tag
        prev_tag.tail = o_text[prev_span_end:span[0]-offset]
        info_tags.pop(0)
    par_[0].text = cur
    if not first:
        prev_tag.tail = o_text[prev_span_end:]

    if o_text:
        offset += len(o_text)
    o_text = par.tail
    cur = o_text
    # Check the children
    for element in par:
        tag_, info_tags, offset = add_tags(element,
                                           info_tags,
                                           offset=offset,
                                           parent=par_)
        for t_ in tag_:
            par_[0].append(t_)
    # Check TAIL
    first = True
    while len(info_tags) > 0:
        span, tag, info = info_tags[0]
        if o_text is None or span[1] >= offset+len(o_text):
            break
        middle = o_text[span[0]-offset:span[1]-offset]
        tag = ET.Element(tag, **info)
        tag.text = middle
        if parent:
            par_.append(tag)
        else:
            par_[0].append(tag)

        if first:
            cur = o_text[:span[0]-offset]
            first = False
        else:
            prev_tag.tail = o_text[prev_span_end:span[0]-offset]
        prev_span_end = span[1]-offset
        prev_tag = tag
        prev_tag.tail = o_text[prev_span_end:span[0]-offset]
        info_tags.pop(0)
    par_[0].tail = cur
    if not first:
        prev_tag.tail = o_text[prev_span_end:]
    if o_text:
        return par_, info_tags, len(o_text)+offset
    else:
        return par_, info_tags, offset


def compatible_tags(candidates, gs_labeling):
    candidates_ = []
    for span_, defi_ in candidates:
        ini_len = len(defi_)
        flag = True
        for gs_tags in gs_labeling:
            span__ = compatible_spans([span_]+defi_,
                                     flat_spans(gs_tags))
            if not ini_len == len(span__)-1:
                flag = False
        if flag:
            candidates_.append((span_, defi_))
    return candidates_


def process_articles(par, cntx, counter):
    arts = test_articles(par, cntx)
    docs = test_docs(par, cntx)
    docs = compatible_tags(docs, [arts])
    insts = test_institutions(par, cntx)
    insts = compatible_tags(insts, [arts, docs])
    tags = []
    for idd, (art, definitions) in enumerate(arts):
        counter.update(["art", "doc"])
        info_art = {}
        info_doc = {}
        info_art['id'] = str(counter["art"])
        info_art['document'] = str(counter["doc"])
        info_doc['id'] = str(counter["doc"])
        tags.append((art[0], 'ArticleMention', info_art))
        tags.append((art[1], 'DocumentMention', info_doc))
        for defi in definitions:
            counter["def"] += 1
            info_def = {'id': str(counter["def"]),
                        "document": str(counter["doc"])}
            tags.append((defi, 'Definition', info_def))
    for idd, (doc, definitions) in enumerate(docs):
        counter.update(["doc"])
        info_doc = {}
        info_doc['id'] = str(counter["doc"])
        tags.append((doc, 'DocumentMention', info_doc))
        for defi in definitions:
            counter["def"] += 1
            info_def = {'id': str(counter["def"]),
                        "document": str(counter["doc"])}
            tags.append((defi, 'Definition', info_def))
    for idd, (inst, definitions) in enumerate(insts):
            counter.update(["inst"])
            info_inst = {}
            info_inst['id'] = str(counter["inst"])
            tags.append((inst, 'InstitutionMention', info_inst))
            for defi in definitions:
                counter["def"] += 1
                info_def = {'id': str(counter["def"]),
                            "institution": str(counter["inst"])}
                tags.append((defi, 'Definition', info_def))
    tags = sorted(tags, key=lambda x: x[0])
    par_, _, _ = add_tags(par, tags)
    return par_[0]


def label_xml(root):
    cntx = Context()
    counter = Counter([])
    for par in root.findall('.//paragraph'):
        counter.update(["par"])
        verbose(fg.YELLOW, "")
        verbose(fg.YELLOW, "Raw text: ",
                style.RESET, "".join([x for x in par.itertext()]))
        verbose(fg.BLUE, "Context: ", fg.BLUE, cntx)
        par = preprocess_paragraph(par)
        # Eliminates article tags
        get_context(par, cntx)
        par_ = process_articles(par, cntx, counter)
        for k, i in cntx.info().items():
            par_.attrib[k] = i

        # Shows some labelling in the document
        for doc in par_.findall('.//DocumentMention'):
            definitions = par_.findall('.//Definition[@document="{0}"]'
                                       .format(doc.attrib['id']))
            resolution, t = resolve_document(doc.text, cntx, len(definitions))
            doc.attrib['name'] = resolution
            doc.attrib['type'] = t
            verbose(fg.GREEN, "Document: ",
                    bg.WHITE, resolution, bg.RESET, "/", doc.text)
            for defi in definitions:
                cntx.add_definition(resolution, defi.text, "document")
                verbose(fg.YELLOW, "Definition: ", bg.WHITE,
                        "".join([x for x in defi.itertext()]),
                        bg.RESET, "->", resolution)
            for art in par_.findall('.//ArticleMention[@document="{0}"]'
                                    .format(doc.attrib['id'])):
                art.attrib["articles"] = split_arts(art.text)
                verbose(fg.BLUE, "Article: ", bg.WHITE, art.text,
                        bg.RESET, '->', art.attrib["articles"])
            pass
        # Shows some labelling in the document
        for inst in par_.findall('.//InstitutionMention'):
            definitions = par_.findall('.//Definition[@institution="{0}"]'
                                       .format(inst.attrib['id']))
            resolution, t = resolve_document(inst.text, cntx, len(definitions))
            inst.attrib['name'] = resolution
            inst.attrib['type'] = t
            verbose(fg.MAGENTA, "Institution: ",
                    bg.WHITE, resolution, bg.RESET, "/", inst.text)
            for defi in definitions:
                cntx.add_definition(resolution, defi.text, "institution")
                verbose(fg.YELLOW, "Definition: ", bg.WHITE,
                        "".join([x for x in defi.itertext()]),
                        bg.RESET, "->", resolution)

        verbose(fg.CYAN, bg.WHITE, "Paragraph: ", bg.RESET, ET.tostring(par_))


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

        # Writing out the XML
        xmloutfilename = os.path.join(args.labelled_dir,
                                      os.path.basename(case['txt']) + ".xml")

        verbose(style.BRIGHT, 'Saving file ', xmloutfilename)
        ET.ElementTree(root).write(xmloutfilename)
