# project/server/main/views.py


#################
#### imports ####
#################
import matplotlib
matplotlib.use('Agg')
from flask import render_template, Blueprint, send_from_directory, request
from flask import jsonify, url_for
from datetime import datetime
from collections import Counter

import os.path
import os

import nltk
#from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

#######################
#### loading JSONDB ###
#######################

from tinydb import TinyDB, Query
db = TinyDB('DB.json')
contensiosos = db.table('contensiosos')
CaseQ = Query()

#######################
#### loading JSONGRPAH ###
#######################
import json
with open('graph.json') as data_file:
    json_graph = json.load(data_file)

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,
    url_prefix="/conectividad",
    static_folder='../../client/static'
    )


import re

################
#### forms ####
################
from wtforms import IntegerField, StringField, BooleanField, Form
from wtforms.validators import DataRequired


class GraphForm(Form):
    include = StringField('include')
    exclude = StringField('exclude')
    include_doc = StringField('include_doc')
    exclude_doc = StringField('exclude_doc')
    min = IntegerField()
    arts = BooleanField()

################
#### routes ####
################

name_country={
"argentina":"Argentina",
"barbados":"Barbados",
"bolivia":"Bolivia",
"brasil":"Brasil",
"chile":"Chile",
"colombia":"Colombia",
"costa rica":"Costa Rica",
"dominicana":"Dominicana",
"ecuador":"Ecuador",
"el salvador":"El Salvador",
"guatemala":"Guatemala",
"granada":"Granada",
"haití":"Haití",
"honduras":"Honduras",
"jamaica":"Jamaica",
"méxico":"México",
"nicaragua":"Nicaragua",
"panamá":"Panama",
"paraguay":"Paraguay",
"perú":"Perú",
"república dominicana":"República Dominicana",
"trinidad y tobago":"Trinidad y Tobago",
"surinam":"Surinam",
"uruguay":"Uruguay",
"venezuela":"Venezuela",
}



color_country={
"argentina":"#922b21",
"barbados":"#cb4335",
"bolivia":"#884ea0",
"brasil":"#7d3c98",
"chile":"#2471a3",
"colombia":"#2e86c1",
"costa rica":"#2e86c1",
"dominicana":"#17a589",
"ecuador":"#138d75",
"el salvador":"#f1c40f",
"guatemala":"#d68910",
"granada":"#d68910",
"haití":"#800000",
"honduras":"#008080",
"jamaica":"#ffff00",
"méxico":"#008000",
"nicaragua":"#0000ff",
"panama":"#000080",
"paraguay":"#800080",
"perú":"#ff0000",
"república dominicana":"#ff5733",
"trinidad y tobago":"#808000",
"surinam":"#ffce00",
"uruguay":"#5ac8d8",
"venezuela":"#cf0a2c",
}

common_documents=[
 "comisión interamericana de derechos humanos",
 "convención interamericana de derechos humanos",
 "convención americana sobre derechos humanos",
 "reglamento de la corte",
]

@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

@main_blueprint.route("/laws/")
def laws():
    return render_template("main/laws.html",docs=contensiosos.all())

@main_blueprint.route("/law/<int:idd>")
def law(idd):
    return render_template("main/law.html",doc=contensiosos.get(eid=idd))


@main_blueprint.route("/doc/", methods=["GET","POST"])
def doc():
    # Para GET
    xmlName = request.args.get('docXmlName')
    docNum = request.args.get('docNum')
    # Para POST , no funciona actualmente :(
    #xmlName = request.args['docXmlName']
    #docNum = request.args['docNum']
    docNum = eval(docNum)

    stop_words = set(stopwords.words('spanish'))
    stop_words.update(
        ['.', ',', '“', "”", '"', "'", '¿', '?', '!', '¡', ':', ';', '(', ')', '°',
        ".(", ").","(”", "”)", "”),", "”).", "),", '[', ']', "[.", ".]", '{', '}',
        "”.", "].", "[.]", '_','-','/', "_________________________"]
    )

    with open('contenciosos/text/'+xmlName) as filename:
        lines=filename.readlines()

    cleaned = ""
    for line in lines:
        cleaned += line + " "

    cleanLines = [i.lower() for i in wordpunct_tokenize(cleaned) if i.lower() not in stop_words]

    fdist = FreqDist(cleanLines)


    with open('labelledDocuments/'+xmlName+".xml") as filename:
        lines=filename.readlines()
        lines=[line.replace("\n",'') for line in lines]



    return render_template("main/documents.html",filename=xmlName+".xml", xml=lines,
        doc=contensiosos.get(eid=docNum),fdist=fdist,nwords=20,nvoc=100)


@main_blueprint.route("/xml/<string:filename>")
def xml(filename):
    gate_css_url=url_for('main.static', filename='gate.css')
    gate_js_url=url_for('main.static', filename='gate.js')
    string="""
<!DOCTYPE html>
<html xml:lang="en" lang="en">
    <head>
        <base>
            <title>Conectividad Normativa</title>
            <link href="{0}" rel="stylesheet" media="screen"></link>
        </base>
    </head>
    <body>
        {2}
        <script src="{1}" type="text/javascript"></script>
    </body>
</html>
"""
    with open('labelledDocuments/'+filename) as filename:
        lines=filename.readlines()

    return string.format(gate_css_url,gate_js_url,"<br/>".join(lines))

@main_blueprint.route("/graph/",methods=["GET","POST"])
def graph():
    form = GraphForm(request.form)
    if request.method == 'POST' and form.validate():
        query={}
        if form.include.data:
            query["include"]=form.include.data
        if form.exclude.data:
            query["exclude"]=form.exclude.data
        if form.include_doc.data:
            query["include_doc"]=form.include_doc.data
        if form.exclude_doc.data:
            query["exclude_doc"]=form.exclude_doc.data
        if form.min.data:
            query["min"]=int(form.min.data)
        if form.arts.data:
            query["exp_arts"]="true"
        if len(query)>0:
            return render_template("main/graph.html",params=query,year=datetime.now().year)
        else:
            return render_template("main/graph.html",params={},year=datetime.now().year)
    return render_template("main/graph_selection.html",form=form,common_documents="({})".format("|".join(common_documents)))

@main_blueprint.route("/numbers/")
def numbers():
    return render_template("main/list_numbers.html")

@main_blueprint.route("/numbers/cases_country")
def cases_country():
    country_cases= Counter()

    countries=[]
    for node in json_graph['nodes']:
        if node['type']==1:
            countries.append(node['country'])
    country_cases=Counter(countries)

    return render_template("main/cases_country.html",
			data=country_cases,
			color_country=color_country,
			name_country=name_country,
			total_cases=sum(country_cases.values()))



@main_blueprint.route("/numbers/documents_citation/<int:ntop>")
@main_blueprint.route("/numbers/documents_citation")
def documents_citation(ntop=200):
    country_cases= Counter()

    documents=[]
    for node in json_graph['nodes']:
        documents.append((node['id'],node['name']))
    documents=dict(documents)

    documents_citation=Counter()
    for link in json_graph['links']:
        try:
            documents_citation[documents[link["target"]]]+=int(link['ori_val'])
        except KeyError:
            documents_citation[documents[link["target"]]]=int(link['ori_val'])


    return render_template("main/documents_citation.html",
			data=documents_citation,
			total_cases=sum(documents_citation.values()),ntop=ntop)


@main_blueprint.route("/graph_full/")
def graph_full():
    return render_template("main/graph.html",params={},year=datetime.now().year,query="")



@main_blueprint.route("/contensioso/<int:case_id>")
def case_json(case_id):
   case = contensiosos.get(doc_id=case_id)
   return jsonify(case)



@main_blueprint.route("/graph.json")
def graph_json():
    if len(request.args)==0:
        return jsonify(json_graph)
    graph_={'nodes':[],'links':[]}
    nodes_=set()
    graph_nodes=[]
    min_nodes=5
    exp_arts=False
    if request.args.get('min'):
        min_nodes=int(request.args.get('min'))
    if request.args.get('exp_arts'):
        if request.args.get('exp_arts')=="true":
            exp_arts=True
    if request.args.get('include'):
        re_include=re.compile(request.args.get('include'))
    if request.args.get('include_doc'):
        re_include_doc=re.compile(request.args.get('include_doc'))

    for node in json_graph['nodes']:
        if node['type']==1:
            if request.args.get('include'):
                if re_include.search(node['name'].lower()):
                    if not node['id'] in nodes_:
                        nodes_.add(node['id'])
                        graph_nodes.append(node)
            else:
                if not node['id'] in nodes_:
                    graph_nodes.append(node)
                    nodes_.add(node['id'])
        elif not exp_arts and node['type']==2:
            if request.args.get('include_doc'):
                if re_include_doc.search(node['name'].lower()):
                    if not node['id'] in nodes_:
                        graph_nodes.append(node)
                        nodes_.add(node['id'])
            else:
                if not node['id'] in nodes_:
                    graph_nodes.append(node)
                    nodes_.add(node['id'])
        elif exp_arts and node['type']==3:
            if request.args.get('include_doc'):
                if re_include_doc.search(node['name'].lower()):
                    if not node['id'] in nodes_:
                        graph_nodes.append(node)
                        nodes_.add(node['id'])
            else:
                if not node['id'] in nodes_:
                    graph_nodes.append(node)
                    nodes_.add(node['id'])

    graph_nodes_=[]
    nodes_=set()

    if request.args.get('exclude'):
        re_exclude=re.compile(request.args.get('exclude'))
    if request.args.get('exclude_doc'):
        re_exclude_doc=re.compile(request.args.get('exclude_doc'))


    for node in graph_nodes:
        if node['type']==1:
            if request.args.get('exclude'):
                if not re_exclude.search(node['name'].lower()):
                    if not node['id'] in nodes_:
                        graph_nodes_.append(node)
                        nodes_.add(node['id'])
            else:
                if not node['id'] in nodes_:
                    graph_nodes_.append(node)
                    nodes_.add(node['id'])
        elif not exp_arts and node['type']==2:
            if request.args.get('exclude_doc'):
                if not re_exclude_doc.search(node['name'].lower()):
                    if not node['id'] in nodes_:
                        graph_nodes_.append(node)
                        nodes_.add(node['id'])
            else:
                if not node['id'] in nodes_:
                    graph_nodes_.append(node)
                    nodes_.add(node['id'])
        elif exp_arts and node['type']==3:
            if request.args.get('exclude_doc'):
                if not re_exclude_doc.search(node['name'].lower()):
                    if not node['id'] in nodes_:
                        graph_nodes_.append(node)
                        nodes_.add(node['id'])
            else:
                if not node['id'] in nodes_:
                    graph_nodes_.append(node)
                    nodes_.add(node['id'])



    targets_=set()
    sources_=set()
    for edge in json_graph['links']:
        if edge['source'] in nodes_ and edge['target'] in nodes_:
            if int(edge['ori_val'])>= min_nodes:
                graph_['links'].append(edge)
                targets_.add(edge['target'])
                sources_.add(edge['source'])


    for node in graph_nodes_:
        if node['type']==1:
            if node['id'] in sources_:
                graph_['nodes'].append(node)
        if node['type']>1:
            if node['id'] in targets_:
                graph_['nodes'].append(node)


    return jsonify(graph_)
