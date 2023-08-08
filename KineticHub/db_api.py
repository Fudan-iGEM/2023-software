"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : db_api.py
@Author : Zhiyue Chen
@Time : 2023/8/6 21:49
"""

import pymysql
from flask import jsonify, Response


def convert_reaction_data_to_json(data: tuple) -> list:
    """
    :param data: tuple, from cursor.fetchall()
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


def search_reaction(db_config: dict, query: str, search_type: str) -> tuple[Response, int]:
    """
    :param db_config: dict, database configuration of mysql
    :param query: the inputted query from the frontend
    :param search_type: the inputted type from the frontend
    :return: json format data that could be used in api
    """
    try:
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute("USE pRAPer")
                search_query = f"SELECT * FROM reactions WHERE {search_type} LIKE '%{query}%'"
                cursor.execute(search_query)
                rows = cursor.fetchall()
                cursor.close()
                return jsonify(convert_reaction_data_to_json(rows)), 200
        except pymysql.Error as e:
            return jsonify({"message": str(e)}), 500
        finally:
            connection.close()
    except pymysql.Error as e:
        return jsonify({"message": str(e)}), 500


def convert_kcat_data_to_json(data: tuple) -> list:
    """
    :param data: tuple, from cursor.fetchall()
    :return: list format of data
    """
    json_data = []
    for row in data:
        json_data.append({
            'database_id': row[0],
            'kcat': row[2],
            'species': row[3],
            'meta': row[4],
            'refs': row[5],
            'substrate': row[6],
        })
    return json_data


def search_kcat(db_config: dict, ec_number: str) -> tuple[Response, int]:
    """
    :param db_config: dict, database configuration of mysql
    :param ec_number: the ec number of each reaction row
    :return: json format data that could be used in api
    """
    try:
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute("USE pRAPer")
                search_query = f"SELECT * FROM kcat WHERE ec_number = '{ec_number}'"
                cursor.execute(search_query)
                rows = cursor.fetchall()
                cursor.close()
                return jsonify(convert_kcat_data_to_json(rows)), 200
        except pymysql.Error as e:
            return jsonify({"message": str(e)}), 500
        finally:
            connection.close()
    except pymysql.Error as e:
        return jsonify({"message": str(e)}), 500


def get_all_ec_numbers(db_config: dict, input_ec_number: str) -> tuple[Response, int]:
    """
    :param input_ec_number: str, the inputted ec number
    :param db_config: dict, database configuration of mysql
    :return: json format data that could be used in api
    """
    try:
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute("USE pRAPer")
                cursor.execute(f"SELECT ec_number FROM reactions WHERE ec_number LIKE '%{input_ec_number}%'")
                rows = cursor.fetchall()
                cursor.close()
                res = [row[0] for row in rows[:5]]
                return jsonify(res), 200
        except pymysql.Error as e:
            return jsonify({"message": str(e)}), 500
        finally:
            connection.close()
    except pymysql.Error as e:
        return jsonify({"message": str(e)}), 500
