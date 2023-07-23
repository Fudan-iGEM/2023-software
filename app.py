"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : app.py
@Author : Zhiyue Chen
@Time : 2023/7/17 1:01
"""
from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_compress import Compress
from os import path
import json

template_folder = path.abspath('webUI/template')
static_folder = path.abspath('webUI/static')
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='')
app.config['JWT_SECRET_KEY'] = 'iGEM_Fudan_2023'
jwt = JWTManager(app)
Compress(app)
with open('users.json', 'r+') as f:
    users = json.load(f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/api/login', methods=['POST'])
def handle_login():
    form_data = request.json
    username = form_data.get('userName')
    password = form_data.get('password')
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    user_pwd = users.get(username, None)
    if user_pwd and user_pwd == password:
        access_token = create_access_token(identity=username, expires_delta=False)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
