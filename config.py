"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : config.py
@Author : Zhiyue Chen
@Time : 2023/8/6 21:50
"""
import os
db_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': 'root',
    'password': os.environ.get('MYSQL_PASSWORD'),
    'charset': 'utf8mb4'
}
parthub_config = {
    "serverUrl": os.environ.get('SERVER_URL'),
    "serverUser": os.environ.get('SERVER_USER'),
    "serverPassword": os.environ.get('SERVER_PASSWORD')
}
