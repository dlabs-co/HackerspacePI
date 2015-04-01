#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Status API for dlabs hackerspace.
    This one is actually capable of managing multiple
    hackerspaces
    It relies on sensor modules for the status management.
    You can have them configured in plugins.inc
    Have in account that all plugins must:
        - Be importable
        - Have a class named HackerspaceAPI
        - With a method status() and optionally setup()
"""

import os
from flask import render_template, redirect, url_for, Flask, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager, ProcessingException
from flask.ext.login import current_user, login_user, LoginManager, UserMixin
from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField, TextField
from ConfigParser import ConfigParser


def read_config():
    """
        config reading
    """
    cfgparser = ConfigParser()
    cfgparser.optionxform = str
    cfgparser.read(os.path.expanduser('~/.hackerspaceapi.cfg'))
    return cfgparser


CONFIG = read_config()

APP = Flask(__name__)
APP.config.update(dict(CONFIG.items('main')))
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.setup_app(APP)
DATABASE = SQLAlchemy(APP)
API_MANAGER = APIManager(APP, flask_sqlalchemy_db=DATABASE)


class User(DATABASE.Model, UserMixin):
    """
        User
    """
    __tablename__ = "user"
    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    username = DATABASE.Column(DATABASE.Unicode(200))
    password = DATABASE.Column(DATABASE.Unicode(200))


class HackerSpace(DATABASE.Model):
    """
        Main hackerspace object
    """
    __tablename__ = "hackerspace"
    id = DATABASE.Column(
        DATABASE.Integer, primary_key=True
    )
    space = DATABASE.Column(DATABASE.Text)
    logo = DATABASE.Column(DATABASE.Text)
    url = DATABASE.Column(DATABASE.Text)
    issue_report_channels = DATABASE.Column(DATABASE.Text)
    location = DATABASE.relationship(
        'Location',
        backref=DATABASE.backref('hackerspace.id')
    )
    contact = DATABASE.relationship(
        'Contact',
        backref=DATABASE.backref('hackerspace.id')
    )
    state = DATABASE.relationship(
        'State',
        backref=DATABASE.backref('hackerspace.id')
    )
    # projects = DATABASE.Column(DATABASE.Text)


class Location(DATABASE.Model):
    """
        Hackerspace location
    """
    __tablename__ = "location"
    id = DATABASE.Column(
        DATABASE.Integer, primary_key=True
    )
    id_hs = DATABASE.Column(
        DATABASE.Integer,
        DATABASE.ForeignKey('hackerspace.id'))
    address = DATABASE.Column(DATABASE.Text)
    lat = DATABASE.Column(DATABASE.Text)
    lon = DATABASE.Column(DATABASE.Text)


class Contact(DATABASE.Model):
    """
        Hackerspace contact methods
    """
    __tablename__ = "contact"
    id = DATABASE.Column(
        DATABASE.Integer, primary_key=True
    )
    id_hs = DATABASE.Column(
        DATABASE.Integer,
        DATABASE.ForeignKey('hackerspace.id'))
    twitter = DATABASE.Column(DATABASE.Text)
    email = DATABASE.Column(DATABASE.Text)
    ml = DATABASE.Column(DATABASE.Text)
    irc = DATABASE.Column(DATABASE.Text)


class State(DATABASE.Model):
    """
        Status changes
        To update the hackerspace status
        we should create a new status object
        and update the hackerspace one to point
        to it
        As a norm, i propose to use trigger person
        as follows:
            - Username (if needed, get name from ID)
            - If not username, plugin_name
    """
    __tablename__ = "state"
    id = DATABASE.Column(
        DATABASE.Integer, primary_key=True
    )
    id_hs = DATABASE.Column(
        DATABASE.Integer,
        DATABASE.ForeignKey('hackerspace.id'))
    date = DATABASE.Column(DATABASE.Text)
    trigger_person = DATABASE.Column(DATABASE.Text)
    status = DATABASE.Column(DATABASE.Text)


class Test(DATABASE.Model):
    """
        Status changes
        To update the hackerspace status
        we should create a new status object
        and update the hackerspace one to point
        to it
        As a norm, i propose to use trigger person
        as follows:
            - Username (if needed, get name from ID)
            - If not username, plugin_name
    """
    __tablename__ = "test"
    id = DATABASE.Column(
        DATABASE.Integer, primary_key=True
    )
    date = DATABASE.Column(DATABASE.DateTime)


@LOGIN_MANAGER.user_loader
def load_user(userid):
    """
        Load user by userid
    """
    return User.query.get(userid)


class LoginForm(Form):
    """
        Main wtf loginform
    """
    username = TextField('username')
    password = PasswordField('password')
    submit = SubmitField('Login')


@APP.route('/', methods=['GET'])
def index():
    """
        main page
    """
    return render_template('index.html')


@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
        login
    """
    form = LoginForm()
    if form.validate_on_submit():
        user, passwd = form.username.data, form.password.data
        result = User.query.filter_by(
            username=user,
            password=passwd
        ).all()

        if result:
            login_user(result[0])
            return redirect(url_for('index'))
        flash('Wrong user or pass')
    return render_template('login.html', form=form)


def auth_func(**kw):
    """
        auth func
    """
    if not current_user.is_authenticated():
        raise ProcessingException(description='Unauthorized', code=401)


def main():
    """
        - Create all
        - Create initial user
    """
    DATABASE.create_all()
    if len(User.query.all()) == 0:
        DATABASE.session.add(User(username=u'admin', password=u'admin'))
    DATABASE.session.commit()
    auth = dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func])
    API_MANAGER.create_api(User, preprocessors=auth)
    API_MANAGER.create_api(State, preprocessors=auth, methods=['GET', 'POST'])
    API_MANAGER.create_api(HackerSpace, methods=['GET'])
    API_MANAGER.create_api(
        HackerSpace,
        methods=['POST', 'PUT', 'PATCH', 'DELETE'],
        preprocessors=auth
    )
    APP.run(debug=True)

if __name__ == "__main__":
    main()
