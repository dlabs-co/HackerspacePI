#!/usr/bin/env python
"""
    Cliente de api de hackerspace
"""

import sys
import os
import json
import requests
import mechanize
import cookielib


def open_session(api_url, username, password):
    """
        Abrimos la sesion con mechanize y devolvemos una cookiejar
    """
    cookiejar = cookielib.LWPCookieJar()
    browser = mechanize.Browser()
    browser.set_cookiejar(cookiejar)
    browser.open(api_url + "/login")
    browser.response()
    browser.select_form(nr=0)
    browser.form['password'] = password
    browser.form['username'] = username
    browser.submit()
    browser.response()
    return cookiejar


def make_request(api_url, json_data, cookiejar, method="get"):
    """
        Hacemos la peticion
    """
    session = requests.session()
    session.cookies = cookiejar
    return getattr(session, method)(api_url, json=json_data)


def main(api_url, place, json_data, username, password, method):
    """
        Main
    """
    cookiejar = open_session(api_url, username, password)
    if os.path.exists(json_data):
        json_data = open(json_data).read()
    print json_data
    json_ = json.loads(json_data)
    return make_request(api_url + "/" + place, json_, cookiejar, method)


if __name__ == "__main__":
    print main(*sys.argv[1:])
