# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, send_from_directory, request
from flask import jsonify, url_for
from datetime import datetime

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
from wtforms import StringField, BooleanField, Form
from wtforms.validators import DataRequired


class GraphForm(Form):
    include = StringField('include')
    exclude = StringField('exclude')
    include_doc = StringField('include_doc')
    exclude_doc = StringField('exclude_doc')


################
#### routes ####
################


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
        if len(query)>0:
            return render_template("main/graph.html",params=query,year=datetime.now().year)
        else:
            return render_template("main/graph.html",params={},year=datetime.now().year)
    return render_template("main/graph_selection.html",form=form)


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
        elif node['type']==2:
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
        elif node['type']==2:
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
            graph_['links'].append(edge)
            targets_.add(edge['target'])
            sources_.add(edge['source'])

   
    for node in graph_nodes_:
        if node['type']==1:
            if node['id'] in sources_:
                graph_['nodes'].append(node)
        if node['type']==2:
            if node['id'] in targets_:
                graph_['nodes'].append(node)
    

    print(len(graph_['nodes']))
    print(len(graph_['links']))
    return jsonify(graph_)



@main_blueprint.route("/doc/<string:filename>")
def doc(filename):
    return render_template("main/documents.html",filename=filename+".xml")


@main_blueprint.route("/xml/<string:filename>")
def xml(filename):
    gate_url=url_for('main.static', filename='gate.css')
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
{1}
</body>
</html>
"""
    with open('annotatedDocuments/'+filename) as filename:
        lines=filename.readlines()

    return string.format(gate_url,"<br/>".join(lines))


