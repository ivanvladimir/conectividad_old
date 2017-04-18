#!/usr/bin/env python3
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Download cases form webpage
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2017/IIMAS/UNAM
# ----------------------------------------------------------------------

# System libraries
import argparse
import sys
import os.path
import os
import requests
from bs4 import BeautifulSoup
import json
import datetime
from tinydb import TinyDB, Query



def download_file(url,odir,simulate=False):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    if not simulate:
        r = requests.get(url, stream=True)
        with open(os.path.join(odir,local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    return os.path.join(odir,local_filename)


# MAIN
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser(description="Download files")
    p.add_argument("--url",
            default="http://www.corteidh.or.cr/index.php/es/casos-contenciosos", type=str,
            action="store", dest="url",
            help="URL to download")
    p.add_argument("--json_name",
            default="info.json", type=str,
            action="store", dest="json_name",
            help="Name for the json file")
    p.add_argument("--odir",
            default="data/contenciosos/", type=str,
            action="store", dest="odir",
            help="File where to download data")
    p.add_argument("--force_download",
            default=False,
            action="store_true", dest="force_download",
            help="Force download of files")
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

    os.makedirs(os.path.dirname(args.odir), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(args.odir),'files'), exist_ok=True)
    verbose("Connecting to DB:",os.path.join(args.odir,args.json_name))
    db = TinyDB(os.path.join(args.odir,args.json_name))
    contensiosos = db.table('contensiosos')

    verbose("Requesting urls:",args.url)
    r = requests.get(args.url)
    verbose("> status:", r.status_code)
    main_page = BeautifulSoup(r.text, 'html.parser')
    verbose("> recovering iframe:", main_page.iframe['src'])

    new_url="/".join(args.url.split('/',3)[:3]+[main_page.iframe['src']])
    verbose("Requesting urls:",new_url)
    r = requests.get(new_url)
    verbose("> status:", r.status_code)
    main_page = BeautifulSoup(r.text, 'html.parser')

    icase=0
    for case in main_page.find_all('tr'):
        title=None
        info_pdf=None
        info_doc=None
        for child in case.find_all('td'):
            if not title and not (child.font and child.font.strong):
                continue
            elif not title and child.font and child.font.strong:
                title= child.font.strong.text
            else:
                for ref in child.find_all('a'):
                    if ref['href'].endswith('.pdf'):
                        info_pdf=ref['href']
                    elif ref['href'].endswith('.doc') or ref['href'].endswith('.docx') :
                        info_doc=ref['href']
                    else:
                        print("Other file type:",ref['href'])
        if title:
            contensiosos.insert(
                {
                    'doc_type':u'source',
                    'date_creation': datetime.datetime.now().isoformat(' '),
                    'date_modification':datetime.datetime.now().isoformat(' '),
                    'title':title,
                    'source_pdf':info_pdf,
                    'source_doc':info_doc
                })


    verbose(len(contensiosos)," extracted cases")
    verbose("Starting to download files")
    for case in contensiosos.all():
        if case['source_pdf']:
            filename=download_file(case['source_pdf'],os.path.join(args.odir,"files"),simulate=True)
            if args.force_download or not os.path.exists(filename): 
                verbose("Dowloading ",case['source_pdf'])
                filename=download_file(case['source_pdf'],os.path.join(args.odir,"files"),simulate=False)
            contensiosos.update({'pdf':filename,'date_modification':datetime.datetime.now().isoformat(' ')},eids=[case.eid])
        if case['source_doc']:
            filename=download_file(case['source_doc'],os.path.join(args.odir,"files"),simulate=True)
            if args.force_download or not os.path.exists(filename): 
                verbose("Dowloading ",case['source_doc'])
                filename=download_file(case['source_doc'],os.path.join(args.odir,"files"),simulate=False)
            contensiosos.update({'doc':filename,'date_modification':datetime.datetime.now().isoformat(' ')},eids=[case.eid])
 
    

       


