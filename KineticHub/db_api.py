"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : db_api.py
@Author : Zhiyue Chen
@Time : 2023/8/6 21:49
"""
import json
import statistics
from copy import deepcopy

import pymysql
from art import text2art
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
                cursor.execute("USE RAP")
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
                cursor.execute("USE RAP")
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
                cursor.execute("USE RAP")
                cursor.execute(f"SELECT ec_number FROM reactions WHERE ec_number LIKE '%{input_ec_number}%' LIMIT 5")
                rows = cursor.fetchall()
                cursor.close()
                res = [row[0] for row in rows]
                return jsonify(res), 200
        except pymysql.Error as e:
            return jsonify({"message": str(e)}), 500
        finally:
            connection.close()
    except pymysql.Error as e:
        return jsonify({"message": str(e)}), 500


def add_kcat2mysql(db_config: dict, data: dict) -> tuple[Response, int]:
    """
    :param db_config: dict, database configuration of mysql
    :param data: dict, the input of '/api/addEnzyme'
    :return: json format response that could be used in api
    """
    if data.get('species'):
        data['species'] = json.dumps(data['species'])
    if data.get('refs'):
        data['refs'] = json.dumps([data['refs']])
    if not data.get('meta'):
        data['meta'] = None
    for key in data:
        if not data[key]:
            data[key] = None
    try:
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute("USE RAP")
                insert_query = f"INSERT INTO kcat ({', '.join(data.keys())}) VALUES ({', '.join(['%s'] * len(data))})"
                cursor.execute(insert_query, tuple(data.values()))
                if data.get('substrate'):
                    ec_number = data['ec_number']
                    search_query = f"SELECT substrates FROM reactions WHERE ec_number = %s"
                    cursor.execute(search_query, ec_number)
                    rows = cursor.fetchall()
                    if rows:
                        substrates_new = list(set(json.loads(rows[0][0])) | {data.get('substrate')})
                        update_query = f"UPDATE reactions SET substrates = %s WHERE ec_number = %s"
                        cursor.execute(update_query, (json.dumps(substrates_new), ec_number))
                connection.commit()
                cursor.close()
                return jsonify({"message": "Your record has been successfully added to RAP!"}), 200
        except pymysql.Error as e:
            return jsonify({"message": str(e)}), 500
        finally:
            connection.close()
    except pymysql.Error as e:
        return jsonify({"message": str(e)}), 500


def get_reaction_data(db_config: dict, reactions: list[dict]) -> tuple[Response, int]:
    """
    :param db_config: dict, database configuration of mysql
    :param reactions: list[dict], the reaction that added from client
    :return: json format response that could be used in api
    """
    try:
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                json_data = []
                cursor.execute("USE RAP")
                for reaction in reactions:
                    reaction_new = deepcopy(reaction)
                    ec_number = reaction.get('ec_number')
                    kinetic_id = reaction.get('id')
                    search_query = f"SELECT name,str FROM reactions WHERE ec_number = %s"
                    cursor.execute(search_query, ec_number)
                    rows = cursor.fetchall()
                    reaction_new['name'] = rows[0][0]
                    reaction_new['str'] = rows[0][1]
                    search_query = f"SELECT substrate,k_cat,species FROM kcat WHERE id = %s"
                    cursor.execute(search_query, kinetic_id)
                    rows = cursor.fetchall()
                    reaction_new['substrate'] = rows[0][0]
                    reaction_new['kcat'] = rows[0][1]
                    reaction_new['species'] = rows[0][2]
                    json_data.append(reaction_new)
                cursor.close()
        except pymysql.Error as e:
            return jsonify({"message": str(e)}), 500
        finally:
            connection.close()
    except pymysql.Error as e:
        return jsonify({"message": str(e)}), 500
    return jsonify(json_data), 200


def calc_optimal_ratio(db_config: dict, data: dict[str:int]) -> tuple[Response, int]:
    """
    :param db_config: dict, database configuration of mysql
    :param data: dict[str:float], the key is the KineticHub ID of the reaction and the value is stoichiometric value
    :return: json format response that could be used in api
    """
    # get kcat of the enzyme
    try:
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                kcat = {}
                cursor.execute("USE RAP")
                for kinetic_id in data.keys():
                    search_query = f"SELECT k_cat FROM kcat WHERE id = %s"
                    cursor.execute(search_query, kinetic_id)
                    rows = cursor.fetchall()
                    kcat[kinetic_id] = rows[0][0]
                cursor.close()
        except pymysql.Error as e:
            return jsonify({"message": str(e)}), 500
        finally:
            connection.close()
    except pymysql.Error as e:
        return jsonify({"message": str(e)}), 500
    # calculate the optimal ratio of the reactions in balance status
    recip_kcat_mul_sv = {}
    recip_kcat_mul_sv_list = []
    for kinetic_id in data.keys():
        recip_kcat_mul_sv[kinetic_id] = 1 / (data.get(kinetic_id) * kcat[kinetic_id])
        recip_kcat_mul_sv_list.append(1 / (data.get(kinetic_id) * kcat[kinetic_id]))
    recip_kcat_mul_sv_list.sort()
    median_value = recip_kcat_mul_sv_list[len(recip_kcat_mul_sv_list) // 2]
    optimal_ratio_json_data = []
    for kinetic_id in data.keys():
        optimal_ratio_json_data.append({kinetic_id: recip_kcat_mul_sv[kinetic_id] / median_value})
    return jsonify(optimal_ratio_json_data), 200


def get_reaction_data_from_optimal_ratio(db_config: dict, optimal_ratio: list[dict]) -> tuple[Response, int]:
    """
    :param db_config: dict, database configuration of mysql
    :param optimal_ratio: dict, optimal concentration ratio of the enzyme
    :return: json format response that could be used in api
    """
    try:
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                json_data = []
                cursor.execute("USE RAP")
                for kinetic_id in optimal_ratio:
                    reaction_data = {}
                    search_query = f"SELECT ec_number FROM kcat WHERE id = %s"
                    cursor.execute(search_query, list(kinetic_id.keys())[0])
                    rows = cursor.fetchall()
                    reaction_data['ec_number'] = rows[0][0]
                    reaction_data['id'] = list(kinetic_id.keys())[0]
                    json_data.append(reaction_data)
                cursor.close()
        except pymysql.Error as e:
            return jsonify({"message": str(e)}), 500
        finally:
            connection.close()
    except pymysql.Error as e:
        return jsonify({"message": str(e)}), 500
    return jsonify(json_data), 200


def test_connection() -> tuple[Response, int]:
    """
    :return: message of RAP to test client's connection with server
    """
    hello = '🍻 Welcome to RAP!\n' + text2art('RAP') + 'RAP ©2023 Created by mistyfield'
    return jsonify({"message": hello}), 200
