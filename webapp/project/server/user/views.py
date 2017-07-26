# project/server/user/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required

from project.server import bcrypt, db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm

################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Gracias por suscribirte', 'success')
        return redirect(url_for("main.home"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Bienvenido', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Password o usuario incorrectos', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has entrado al sistema', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/members')
@login_required
def members():
    return render_template('user/members.html')
