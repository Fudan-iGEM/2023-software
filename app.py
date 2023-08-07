"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : app.py
@Author : Zhiyue Chen
@Time : 2023/7/17 1:01
"""
from flask import Flask, render_template, request, jsonify
from flask_compress import Compress
from os import path

import config
from KineticHub.db_api import search_reaction, search_kcat

db_config = config.db_config
template_folder = path.abspath('webUI/template')
static_folder = path.abspath('webUI/static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='')
Compress(app)


# for web pages
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/reaction')
def reaction():
    return render_template('reaction.html')


@app.route('/comment')
def comment():
    return render_template('comment.html')


@app.route('/addEnzyme')
def add_enzyme():
    return render_template('addEnzyme.html')


# for apis
@app.route('/api/search/reaction', methods=['POST'])
def handle_search_reaction():
    form_data = request.json
    query = form_data.get('searchQuery')
    search_type = form_data.get('searchType')
    if not query or not search_type:
        return jsonify({"message": "Missing query or type"}), 400
    return search_reaction(db_config, query, search_type)


@app.route('/api/search/kcat', methods=['POST'])
def handle_search_kcat():
    data = request.json
    ec_number = data.get('ecNumber')
    if not ec_number:
        return jsonify({"message": "Missing ec_number"}), 400
    return search_kcat(db_config, ec_number)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
