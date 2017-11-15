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
from bs4 import BeautifulSoup

# local libraries
from utils import pdf2text, extract_topics, search_regexp

from string import punctuation
non_words = list(punctuation)
#we add spanish punctuation
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))

sws=stopwords.words('spanish')

re_articulo=re.compile('[\d\.]+')
re_articulos=re.compile('art.culos?')
re_recovery=re.compile('(art.culos?|art.culos?) (?P<articles>[\d.,y ixviabc]+-?) (fracción [^,]*, )?(inciso [^,]*, )?(de esa|de esta|de la |del |de su |en la )?(?P<source>(dich[oa] |últim[oa] |presente ley |ley )?[^",;.()]*)[,.;]?')
re_numbers=re.compile('([\d.]+|[ixv]+)')
re_mismo=re.compile('(últim[ao]|mism[oa]|dicha Convención|dich[oa]|presente|esta ley|([A-Z][^ \d]+ *([A-Z][^ \d]+ *|\d +|mexicana|por +|al +|para +|do +|de +|en +|las? +|del +|sobre +|en +|contra +|los? +|\[\w+\][ .,;]+)*)\d*)')
re_spaces=re.compile("\s+")
re_en_adelante=re.compile('([A-Z]\w*( [A-Z]\w*| para| y| contra| Prevenir,| Educación, | sobre| del| en| de| la| los| y| el)*) \( ?en *adelante,? *(?:también *)?"([^"]+)"(?: o "([^"]+)")?')
re_corchetes=re.compile('([A-Z]\w*) \[(.*)\]')
re_anafora=re.compile("[A-Z]\w*( de| [A-Z]\w*)*")

reductions=[
(re.compile('mism[ao]'),'PENDING'),
(re.compile('MISM[AO]'),'PENDING'),
(re.compile('dicha Convención'),'Convención'),
(re.compile('dich[oa]'),'PENDING'),
(re.compile('presente'),'PENDING'),
(re.compile('esta ley'),'PENDING'),
(re.compile('Son'),'PENDING'),
(re.compile('est[ae] últim[oa]'),'PENDING'),
(re.compile('Convención [I|i]\w*'),'Convención Interamericana de Derechos Humanos'),
(re.compile('Convención [A|a]\w*'),'Convención Americana sobre Derechos Humanos'),
(re.compile('RAAN'),'Regiones Autónomas del Atlántico Norte'),
(re.compile('MARENA'),'Ministerio del Ambiente y Recursos Naturales de Nicaragua'),
(re.compile('RAAS'),'Regiones Autónomas del Atlántico Sur'),
(re.compile('CONVENCIÓN [I|i]\w*'),'Convención Interamericana de Derechos Humanos'),
(re.compile('CONVENCIÓN [A|a]\w*'),'Convención Americana de Derechos Humanos'),
(re.compile('Estatuto.*(corte)*'),'Estatuto de la Corte'),
(re.compile('Reglamento.*(corte)*'),'Reglamento de la Corte'),
(re.compile('CP'),'Código Penal'),
(re.compile('CIDFP'),'Convención Interamericana sobre Desaparición Forzada de Personas'),
]


replacements=[
(re.compile(', numeral (\d+),'),'.\\1'),
(re.compile(' numeral (\d+)'),'.\\1'),
(re.compile(', párrafo (\d+),'),'.\\1'),
]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ORANGE = '\033[101m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# MAIN
if __name__ == "__main__":
    # Command line options

    p = argparse.ArgumentParser(description="Extracti articles")
    p.add_argument("--re_selector",
            default=".*", type=str,
            action="store", dest="re_selector",
            help="ER to select files")
    p.add_argument("--annotated_dir",
            default="data/annotatedDocuments", type=str,
            action="store", dest="annotated_dir",
            help="Directory with the annotated documents")
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
            print(*args)
    else:
        verbose = lambda *a: None

    # Connecting to DB
    verbose("Connecting to DB:",args.dbname)
    db = TinyDB(args.dbname)
    contensiosos = db.table('contensiosos')

    re_selector=re.compile(args.re_selector)

    # Initialization counting
    Filter = Query()
    mentions=[]
    for case in contensiosos.search(Filter.title.search(re_selector)):
        xmlfile=os.path.join(args.annotated_dir,os.path.basename(case['txt'])+".xml")
        verbose('Analysing ',case['txt'])
        verbose('Looking for ',xmlfile)
        try:
            with open(xmlfile) as fp:
                soup = BeautifulSoup(fp,'lxml')
        except FileNotFoundError:
            verbose(bcolors.FAIL + 'ARCHIVO FALTANTE ' + bcolors.ENDC,xmlfile)
            continue
        prev_source=None
        ##definitions={}
        definitions={'convención':"Convención Americana sobre Derechos Humanos"}
        for par in soup.select('paragraph'):
            text=par.text.replace("“",'"').replace("”",'"').replace("No.",'Num')
            text=text.replace("ó",'ó')
            text=text.replace('"la Convención Americana o','"la Convención Americana" o')
            text=text.replace('Proyecto de Artículo','Proyecto de Art')
            text=text.replace('Convención26','Convención')
            sentences = sent_tokenize(text)
            for sentence in sentences:
                sentence_original=sentence.replace('\n',' ')
                sentence_original=re_spaces.sub(' ',sentence_original)
                sentence_original=sentence_original.replace('protección de todas las personas contra las desapariciones forzadas','Protección de Todas las Personas contra las Desapariciones Forzadas')
                verbose(bcolors.OKBLUE +'> Sentence '+ bcolors.ENDC ,sentence_original)
                sentence_lower=sentence_original.lower()
                m=re_articulo.search(sentence_lower)
                if m:
                    verbose(bcolors.OKGREEN +'> Candidate '+ bcolors.ENDC ,sentence_lower)
                    starts=[]
                    for m in re_en_adelante.finditer(sentence_original):
                        definitions[m.group(3).lower().replace('la ','').replace('el ','').strip()+" "]=m.group(1)
                        verbose(bcolors.HEADER +'> Definition '+ bcolors.ENDC,m.group(3),'to',m.group(1))
                        if m.group(4):
                            definitions[m.group(4).lower().replace('la ','').replace('el ','').strip()+" "]=m.group(1)
                            verbose(bcolors.HEADER +'> Definition '+ bcolors.ENDC,m.group(4),'to',m.group(1))
                    for m in re_corchetes.finditer(sentence_original):
                        definitions[m.group(1).lower()]=m.group(1)+" "+m.group(2)
                        verbose(bcolors.HEADER +'> Definition '+ bcolors.ENDC,m.group(1)+" "+m.group(2),'to',m.group(1))

                    for m in re_articulos.finditer(sentence_lower):
                        start,end=m.span()
                        starts.append(start)
                    starts.append(len(sentence_lower))

                    segs=zip(starts[:-1],starts[1:])
                    if len(starts)<=1:
                        for m in re_anafora.finditer(sentence_original):
                            verbose(bcolors.FAIL +'> ANAFORA '+ bcolors.ENDC,m.group(0))
                            anafora=m.group(0)

                    for ini,fin in segs:
                        bit=sentence_lower[ini:fin]

                        m=re_recovery.search(bit)
                        if not m:
                            continue
                        verbose(bcolors.WARNING +'> BIT '+ bcolors.ENDC,bit)
                        print(m.groups())
                        source_start,source_end=m.span('source')
                        SOURCE=sentence_original[ini+source_start:ini+source_end].strip()
                        mismo=re_mismo.search(SOURCE)

                        if not mismo:
                            continue
                        source=mismo.group(1).strip()
                        print(mismo.groups())

                        definitions_=[(len(k),k) for k in definitions.keys()]
                        definitions_.sort()
                        definitions_.reverse()
                        for re_, source_ in reductions:
                            if re_.search(source):
                                source=source_
                                break

                        for _,definition in definitions_:
                            #print(source.lower().strip().find(definition),definition,source.lower().strip())
                            if (source.lower().strip()+" ").find(definition)==0:
                                source=definitions[definition]
                                break

                        if source.startswith('PENDING'):
                            if prev_source:
                                source=prev_source
                            elif len(anafora.split())>1:
                                source=anafora
                            else:
                                verbose(bcolors.FAIL +'> PREV_SOURCE '+ bcolors.ENDC,SOURCE)

                        arts=m.group('articles')
                        for re_,rep_ in replacements:
                            arts=re_.sub(rep_,arts)

                        articles=re_numbers.findall(arts)
                        if len(articles)==0:
                            continue
                            prev_source=None
                        if source in ["de",'en','del','los','II','El','Las','La','Los',"De"]:
                            continue
                            prev_source=None

                        source = ''.join([c for c in source if c not in non_words])
                        verbose(bcolors.ORANGE +'> SOURCE '+ bcolors.ENDC,source)
                        verbose(bcolors.ORANGE +'> ARTICLES '+ bcolors.ENDC,articles)
                        for article in articles:
                            mentions.append((case['title'],source,article,case))
                        prev_source=source

hist_dest=Counter([y for x,y,z,w in mentions])
hist_dest2=Counter([(y,z) for x,y,z,w in mentions])
hist_sources=Counter([x for x,y,z,w in mentions])
hist_sources_=dict([(x,w) for x,y,z,w in mentions])
hist_full=Counter([(x,y) for x,y,z,w in mentions])
cases_xy={}
for x,y,z,w in mentions:
    cases_xy[(x,y)]=w
name2id={}

for c,y in hist_dest.most_common():
    print(y,c)

JSON={}
JSON["nodes"]=[]
JSON["links"]=[]
id2node={}

re_pais=re.compile(r".*\.([^.]*)$")
for idd,k in enumerate(hist_sources.keys()):
    if hist_sources[k]>4:
        case=hist_sources_[k]
        m=re_pais.match(case['meta_name']['name'])
        pais="unknown"
        if m:
            pais=m.group(1)
        try:
            JSON['nodes'].append({"id":case.doc_id,"type":1,"country":pais.lower().strip(),"name":case["meta_name"]['name'],"year":case["meta_name"]['date_sentence'][-4:] })
            name2id[k]=case.doc_id
        except: ## Penserbjorne
            continue

nnode=len(contensiosos)+1
for idd,k in  enumerate(hist_dest.keys()):
    if hist_dest[k]>4:
        JSON['nodes'].append({"id":nnode,"type":2,"name":k})
        name2id[k]=nnode
        nnode+=1

#for idd,(k,a) in  enumerate(hist_dest2.keys()):
#    if k in name2id:
#        JSON['nodes'].append({"id":nnode,"type":3,"name":k+":"+a})
#        JSON['links'].append({"source":name2id[k],"target":nnode,"value":1,"article":a})
#        name2id[k+":"+a]=nnode
#        nnode+=1

#if len(hist_full.most_common()):
    #Untab
#    vals,c_max=hist_full.most_common()[0]

vals=hist_full.most_common()
vals.reverse()
for (x,y),c in vals:
    try:
        w=cases_xy[(x,y)]
        JSON['links'].append({"source":name2id[x],"target":name2id[y],"value":c+1})
    except KeyError:
        continue

with open(args.graph, 'w') as outfile:
    json.dump(JSON, outfile)
