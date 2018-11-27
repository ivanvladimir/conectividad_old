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
import networkx as nx
from py2neo import Graph
import operator

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


#######################
#### loading GRPAH ###
#######################
from project.server.main import config
graph__ = Graph("bolt://127.0.0.1:7687", auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,
    url_prefix="/conectividad",
    static_folder='../../client/static'
    )


api_blueprint = Blueprint('api', __name__,
    url_prefix="/conectividad/api",
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
    court_cases = BooleanField()
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
        if form.court_cases.data:
            query["court_cases"]="true"
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


@main_blueprint.route("/numbers/articles_citation/<int:ntop>")
@main_blueprint.route("/numbers/articles_citation")
def articles_citation(ntop=200):
    country_cases= Counter()

    articles=[]
    for node in json_graph['nodes']:
        if node['type']==3:
            articles.append((node['id'],(node['doc'],node['art'])))
    articles=dict(articles)

    articles_citation=Counter()
    for link in json_graph['links']:
        if  link['target'] in articles:
            try:
                articles_citation[articles[link["target"]]]+=int(link['ori_val'])
            except KeyError:
                articles_citation[articles[link["target"]]]=int(link['ori_val'])


    return render_template("main/articles_citation.html",
			data=articles_citation,
			total_articles=sum(articles_citation.values()),ntop=ntop)


@main_blueprint.route("/numbers/density_country")
@main_blueprint.route("/numbers/density_country/<int:min_value>")
def numbers_density_country(min_value=5):
    countries={}
    for country in name_country.keys():
        G = nx.DiGraph()
        nodes_=set()
        edges_=[]
        targets_=set()
        for node in json_graph['nodes']:
            if node['type']==1 and node['country']==country:
                nodes_.add(node['id'])
            if node['type']==2:
                targets_.add(node['id'])
        for link in json_graph['links']:
            if link['source'] in nodes_ and link['target'] in targets_ and link['ori_val']>=min_value:
                nodes_.add(node['id'])
                edges_.append((link['source'],link['target'],link['ori_val']))

        G.add_nodes_from(nodes_ )
        G.add_weighted_edges_from([ e for e in edges_ ])
        d=nx.density(G)
        countries[country]=d

    return render_template("main/country.html",
                        title="Densidad grafo por país",
			data=countries,
                        country_names=[x for x,y in sorted(countries.items(), key=operator.itemgetter(1),reverse=True)],
			color_country=color_country,
			name_country=name_country)


@main_blueprint.route("/numbers/adc_country")
@main_blueprint.route("/numbers/adc_country/<int:min_value>")
def numbers_adc_country(min_value=5):
    countries={}
    for country in name_country.keys():
        G = nx.DiGraph()
        nodes_=set()
        edges_=[]
        targets_=set()
        for node in json_graph['nodes']:
            if node['type']==1 and node['country']==country:
                nodes_.add(node['id'])
            if node['type']==2:
                targets_.add(node['id'])
        for link in json_graph['links']:
            if link['source'] in nodes_ and link['target'] in targets_ and link['ori_val']>=min_value:
                nodes_.add(node['id'])
                edges_.append((link['source'],link['target'],link['ori_val']))

        G.add_nodes_from(nodes_ )
        G.add_weighted_edges_from([ e for e in edges_ ])
        dc=nx.degree_centrality(G)
        if len(dc)>0:
            countries[country]=sum([v for v in dc.values()])/len(dc)

    return render_template("main/country.html",
                        title="Promedio grado de centralidad grafo por país",
			data=countries,
                        country_names=[x for x,y in sorted(countries.items(), key=operator.itemgetter(1),reverse=True)],
			color_country=color_country,
			name_country=name_country)

@main_blueprint.route("/numbers/maxdc_country")
@main_blueprint.route("/numbers/maxdc_country/<int:min_value>")
def numbers_maxdc_country(min_value=5):
    countries={}
    for country in name_country.keys():
        G = nx.DiGraph()
        nodes_=set()
        edges_=[]
        targets_=set()
        for node in json_graph['nodes']:
            if node['type']==1 and node['country']==country:
                nodes_.add(node['id'])
            if node['type']==2:
                targets_.add(node['id'])
        for link in json_graph['links']:
            if link['source'] in nodes_ and link['target'] in targets_ and link['ori_val']>=min_value:
                nodes_.add(node['id'])
                edges_.append((link['source'],link['target'],link['ori_val']))

        G.add_nodes_from(nodes_ )
        G.add_weighted_edges_from([ e for e in edges_ ])
        dc=nx.degree_centrality(G)
        if len(dc)>0:
            m,nm=get_max(dc)
            countries[country]=m

    return render_template("main/country.html",
                        title="Máximo grado de centralidad grafo por país",
			data=countries,
                        country_names=[x for x,y in sorted(countries.items(), key=operator.itemgetter(1),reverse=True)],
			color_country=color_country,
			name_country=name_country)




@main_blueprint.route("/numbers/arcs_country")
@main_blueprint.route("/numbers/arcs_country/<int:min_value>")
def numbers_arcs_country(min_value=5):
    countries={}
    country_names={}
    for country in name_country.keys():
        nodes_=set()
        cases=0
        edges_=set()
        targets_=set()
        for node in json_graph['nodes']:
            if node['type']==1 and node['country']==country:
                nodes_.add(node['id'])
                cases+=1
            if node['type']==2:
                targets_.add(node['id'])
        for link in json_graph['links']:
            if link['source'] in nodes_ and link['target'] in targets_ and link['ori_val']>=min_value:
                nodes_.add(node['id'])
                edges_.add((link['source'],link['target'],link['ori_val']))

        if cases:
            countries[country]=len(edges_)/cases
            country_names[country]=name_country[country]+" ({})".format(cases)

    return render_template("main/country.html",
                        title="Arcos por país",
			data=countries,
                        country_names=[x for x,y in sorted(countries.items(), key=operator.itemgetter(1),reverse=True)],
			color_country=color_country,
			name_country=country_names)








@main_blueprint.route("/numbers/documents_citation/<int:ntop>")
@main_blueprint.route("/numbers/documents_citation")
def documents_citation(ntop=200):
    country_cases= Counter()

    documents=[]
    for node in json_graph['nodes']:
        if node['type']==2:
            documents.append((node['id'],node['name']))
    documents=dict(documents)

    documents_citation=Counter()
    for link in json_graph['links']:
        if link['target'] in documents:
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

def get_max(dic):
    m=0
    nm=None
    for k,v in dic.items():
        if v>m:
            m=v
            nm=k
    return m,nm



@main_blueprint.route("/graph.json")
def graph_json():
    if len(request.args)==0:
        return jsonify(json_graph)
    graph_={'nodes':[],'links':[]}
    nodes_=set()
    graph_nodes=[]
    min_nodes=5
    exp_arts=False
    court_cases=False
    if request.args.get('min'):
        min_nodes=int(request.args.get('min'))
    if request.args.get('exp_arts'):
        if request.args.get('exp_arts')=="true":
            exp_arts=True
    if request.args.get('court_cases'):
        if request.args.get('court_cases')=="true":
            court_cases=True
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
        elif not court_cases and not exp_arts and node['type']==2:
            if request.args.get('include_doc'):
                if re_include_doc.search(node['name'].lower()):
                    if not node['id'] in nodes_:
                        graph_nodes.append(node)
                        nodes_.add(node['id'])
            else:
                if not node['id'] in nodes_:
                    graph_nodes.append(node)
                    nodes_.add(node['id'])
        elif not court_cases and exp_arts and node['type']==3:
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
        elif not court_cases and not exp_arts and node['type']==2:
            if request.args.get('exclude_doc'):
                if not re_exclude_doc.search(node['name'].lower()):
                    if not node['id'] in nodes_:
                        graph_nodes_.append(node)
                        nodes_.add(node['id'])
            else:
                if not node['id'] in nodes_:
                    graph_nodes_.append(node)
                    nodes_.add(node['id'])
        elif not court_cases and exp_arts and node['type']==3:
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
            if node['id'] in sources_ or node['id'] in targets_:
                graph_['nodes'].append(node)
        if node['type']>1:
            if node['id'] in targets_:
                graph_['nodes'].append(node)


    G = nx.DiGraph()
    G.add_nodes_from([ n['id'] for n in graph_['nodes']])
    G.add_weighted_edges_from([ (e['source'],e['target'],e['ori_val']) for e in graph_['links']])

    graph_['stats']={}
    graph_['stats']['Density']=nx.density(G)
    dc=nx.degree_centrality(G)
    m,nm=get_max(dc)
    if m>0.0:
        graph_['stats']['avg Degree Centrality']=sum([v for v in dc.values()])/len(dc)
        graph_['stats']['max Degree Centrality']=m
        graph_['stats']['Node Degree Centrality']=nm

    for i,node in enumerate(graph_['nodes']):
        graph_['nodes'][i]['dc']=dc[node['id']]



    return jsonify(graph_)




@api_blueprint.route("/graph/case")
def graph_cases():
    cur=graph__.nodes.match("Case")
    j=[]
    for record in cur:
        j.append({u'title':record['name']})
    return jsonify(j)


