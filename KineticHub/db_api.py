"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : db_api.py
@Author : Zhiyue Chen
@Time : 2023/8/6 21:49
"""
import pymysql
from flask import jsonify


def convert_reaction_data_to_json(data: tuple):
    """
    :param data: tuple from cursor.fetchall()
    :return: list format of data
    """
    json_data = []
    for row in data:
        json_data.append({
            'ec_number': row[0],
            'ec_annotation': row[1],
            'name': row[2],
            'systematic_name': row[3],
            'str': row[4],
            'type': row[5],
        })
    return json_data


def search_reaction(db_config: dict, query: str, type: str):
    """
    :param db_config: dict database configuration of mysql
    :param query: the inputted query from the frontend
    :param type: the inputted type from the frontend
    :return: json format data that could be used in api
    """
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("USE pRAPer")
            search_query = f"SELECT * FROM reactions WHERE {type} LIKE '%{query}%'"
            cursor.execute(search_query)
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            return jsonify(convert_reaction_data_to_json(rows)), 200
    except pymysql.Error as e:
        print(e)
        return jsonify({"message": str(e)}), 500
    finally:
        connection.close()
