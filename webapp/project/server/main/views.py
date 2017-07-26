# project/server/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint

#######################
#### loading JSONDB ###
#######################

from tinydb import TinyDB, Query
db = TinyDB('DB.json')
contensiosos = db.table('contensiosos')


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


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
    return render_template("main/graph.html")

@main_blueprint.route("/doc/")
def doc():
    return render_template("main/documents.html")

