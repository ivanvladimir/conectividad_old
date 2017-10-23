# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, send_from_directory, request
from flask import jsonify
from datetime import datetime

#######################
#### loading JSONDB ###
#######################

from tinydb import TinyDB, Query
db = TinyDB('DB.json')
contensiosos = db.table('contensiosos')


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


################
#### forms ####
################
from wtforms import StringField, BooleanField, Form
from wtforms.validators import DataRequired


class GraphForm(Form):
    include = StringField('include')
    exclude = StringField('exclude')
    include2 = StringField('include2')
    exclude2 = StringField('exclude2')


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
        query=[]
        if form.include.data:
            query.append("include="+form.include.data)
        if form.exclude.data:
            query.append("exclude="+form.exclude.data)
        if len(query)>0:
            return render_template("main/graph.html",query="?"+"&".join(query),year=datetime.now().year)
        else:
            return render_template("main/graph.html",query="",year=datetime.now().year)
    return render_template("main/graph_selection.html",form=form)


@main_blueprint.route("/graph_full/")
def graph_full():
    return render_template("main/graph.html",year=datetime.now().year,query="")


@main_blueprint.route("/graph.json")
def graph_json():
    if len(request.args)==0:
        return jsonify(json_graph)
    graph_={'nodes':[],'links':[]}
    nodes_=set()
    for node in json_graph['nodes']:
        if node['type']==1:
            if request.args.get('include'):
                if request.args.get('include') in node['name'].lower():
                    graph_['nodes'].append(node)
                    nodes_.add(node['id'])
            else:
                    graph_['nodes'].append(node)
                    nodes_.add(node['id'])

    targets_=set()
    for edge in json_graph['links']:
        if edge['source'] in nodes_:
            graph_['links'].append(edge)
            targets_.add(edge['target'])

    for node in json_graph['nodes']:
        if node['type']==2 and node['id'] in targets_:
            if request.args.get('include2'):
                if request.args.get('include2') in node['name'].lower():
                    graph_['nodes'].append(node)
            else:
                    graph_['nodes'].append(node)

    print(graph_)
    return jsonify(graph_)



@main_blueprint.route("/doc/<string:filename>")
def doc(filename):
    return render_template("main/documents.html",filename=filename+".xml")


@main_blueprint.route("/xml/<string:filename>")
def xml(filename):
    string="""
<!DOCTYPE html>
<html xml:lang="en" lang="en">  
<head>
    <base href="/conectividad/">
        <title>Conectividad Normativa</title>
        <link href="/static/gate.css" rel="stylesheet" media="screen"></link>
     </base>
</head>
<body>
{0}
</body>
</html>
"""
    with open('annotatedDocuments/'+filename) as filename:
        lines=filename.readlines()

    return string.format("<br/>".join(lines))


