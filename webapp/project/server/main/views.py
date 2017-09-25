# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, send_from_directory
from datetime import datetime

#######################
#### loading JSONDB ###
#######################

from tinydb import TinyDB, Query
db = TinyDB('DB.json')
contensiosos = db.table('contensiosos')


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,
    url_prefix="/conectividad",
    static_folder='../../client/static'
    )


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

@main_blueprint.route("/graph/")
def graph():
    return render_template("main/graph.html",year=datetime.now().year)

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


