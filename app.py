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
from art import tprint

import config
from KineticHub.db_api import search_reaction, search_kcat, get_all_ec_numbers, add_kcat2mysql, test_connection, \
    get_reaction_data

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


@app.route('/buildReactions')
def build_reactions():
    return render_template('buildReactions.html')


# for apis
@app.route('/api/search/reaction', methods=['POST'])
def handle_search_reaction():
    form_data = request.json
    query = form_data.get('searchQuery')
    search_type = form_data.get('searchType')
    if not query or not search_type:
        app.logger.warning('Missing query or type')
        return jsonify({"message": "Missing query or type"}), 400
    res = search_reaction(db_config, query, search_type)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/search/kcat', methods=['POST'])
def handle_search_kcat():
    data = request.json
    ec_number = data.get('ecNumber')
    if not ec_number:
        app.logger.warning('Missing ec_number')
        return jsonify({"message": "Missing ec_number"}), 400
    res = search_kcat(db_config, ec_number)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/addEnzyme/sug/ec_number', methods=['POST'])
def handle_sug_ec_number():
    data = request.json
    ec_number = data.get('ecNumber')
    if not ec_number:
        app.logger.warning('Missing ec_number')
        return jsonify({"message": "Missing ec_number"}), 400
    res = get_all_ec_numbers(db_config, ec_number)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/build/reactionData', methods=['POST'])
def handle_get_add_reaction_data():
    data = request.json
    reactions = data.get('reactions')
    if not reactions:
        app.logger.warning('Missing reactions on /buildReactions')
        return jsonify({"'Missing reactions on /buildReactions"}), 400
    res = get_reaction_data(db_config, reactions)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/addEnzyme', methods=['POST'])
def handle_add_enzyme():
    form_data = request.json
    if not form_data.get('values'):
        app.logger.warning('Missing data on /addEnzyme')
        return jsonify({"message": 'Missing data on /addEnzyme'}), 400
    res = add_kcat2mysql(db_config, form_data.get('values'))
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/test/connection')
def handle_test_connection():
    return test_connection()


if __name__ == '__main__':
    print('🍻 Welcome to RAP!')
    tprint('RAP')
    app.run(host='0.0.0.0')
