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

template_folder = path.abspath('webUI/template')
static_folder = path.abspath('webUI/static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='')
Compress(app)


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


@app.route('/api/search/reaction', methods=['POST'])
def handle_search():
    form_data = request.json
    query = form_data.get('searchQuery')
    search_type = form_data.get('searchType')
    if not query or not search_type:
        return jsonify({"message": "Missing query or type"}), 400
    return jsonify([{'1':1},{'2':22}]), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
