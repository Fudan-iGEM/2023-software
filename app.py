"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : app.py
@Author : Zhiyue Chen
@Time : 2023/7/17 1:01
"""
import os.path

from flask import Flask, render_template, request, jsonify, send_file
from flask_compress import Compress
from os import path
from art import tprint

import config
from KineticHub.db_api import search_reaction, search_kcat, get_all_ec_numbers, add_kcat2mysql, test_connection, \
    get_reaction_data, calc_optimal_ratio, get_reaction_data_from_optimal_ratio
from RAPBuilderAPI.utils import build_pRAP_system

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


@app.route('/RAPBuilder')
def rap_builder():
    return render_template('rapBuilder.html')


@app.route('/PartHub2')
def parthub_2():
    return render_template('parthub2.html')


@app.route('/parts')
def parts():
    return render_template('parts.html')


# for apis
@app.route('/api/search/reaction', methods=['POST'])
def handle_search_reaction():
    form_data = request.json
    if not form_data or not form_data.get('searchQuery') or not form_data.get('searchType'):
        app.logger.warning('Missing query or type')
        return jsonify({"message": "Missing query or type"}), 400
    query = form_data.get('searchQuery')
    search_type = form_data.get('searchType')
    res = search_reaction(db_config, query, search_type)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/search/kcat', methods=['POST'])
def handle_search_kcat():
    data = request.json
    if not data or not data.get('ecNumber'):
        app.logger.warning('Missing ec_number')
        return jsonify({"message": "Missing ec_number"}), 400
    ec_number = data.get('ecNumber')
    res = search_kcat(db_config, ec_number)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/addEnzyme/sug/ec_number', methods=['POST'])
def handle_sug_ec_number():
    data = request.json
    if not data or not data.get('ecNumber'):
        app.logger.warning('Missing ec_number')
        return jsonify({"message": "Missing ec_number"}), 400
    ec_number = data.get('ecNumber')
    res = get_all_ec_numbers(db_config, ec_number)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/build/reactionData', methods=['POST'])
def handle_get_add_reaction_data():
    data = request.json
    if not data or not data.get('reactions'):
        app.logger.warning('Missing reactions on /buildReactions')
        return jsonify({"message": 'Missing reactions on /buildReactions'}), 400
    reactions = data.get('reactions')
    res = get_reaction_data(db_config, reactions)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/addEnzyme', methods=['POST'])
def handle_add_enzyme():
    form_data = request.json
    if not form_data or not form_data.get('values'):
        app.logger.warning('Missing data on /addEnzyme')
        return jsonify({"message": 'Missing data on /addEnzyme'}), 400
    res = add_kcat2mysql(db_config, form_data.get('values'))
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/buildReactions', methods=['POST'])
def handle_build_reactions():
    form_data = request.json
    if not form_data or not form_data.get('values'):
        app.logger.warning('Missing data on /addEnzyme')
        return jsonify({"message": 'Missing data on /addEnzyme'}), 400
    return calc_optimal_ratio(db_config, form_data.get('values'))


@app.route('/api/rap/reactionData', methods=['POST'])
def handle_rap_reactions():
    data = request.json
    if not data or not data.get('optimalRatio'):
        app.logger.warning('Missing reactions on /RAPBuilder')
        return jsonify({"message": 'Missing reactions on /RAPBuilder'}), 400
    optimal_ratio = data.get('optimalRatio')
    res = get_reaction_data_from_optimal_ratio(db_config, optimal_ratio)
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/rap/build', methods=['POST'])
def handle_rap_build():
    data = request.json
    if not data or not data.get('formData'):
        app.logger.warning('Missing sequences on /RAPBuilder')
        return jsonify({"message": 'Missing sequences on /RAPBuilder'}), 400
    data_list = data.get('formData')
    try:
        res = build_pRAP_system(data_list)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    if res[1] != 200:
        app.logger.warning(str(res[0].data.decode('utf-8')))
    return res


@app.route('/api/test/connection')
def handle_test_connection():
    return test_connection()


# for file download
@app.route('/download/<filename>')
def handle_download(filename):
    filepath = os.path.join('./results', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    print('🍻 Welcome to RAP!')
    tprint('RAP')
    app.run(host='0.0.0.0')
