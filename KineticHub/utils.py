"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : utils.py
@Author : Zhiyue Chen
@Time : 2023/7/28 4:09
"""
import re


def extract_substrates(reaction_dict_list: list[dict]):
    """
    :param reaction_dict_list: the output of substratesAndProducts method
    :return: list contains all possible substrates
    """
    res = []
    for reaction_dict in reaction_dict_list:
        if reaction_dict.get('substrates', None):
            res = res + reaction_dict['substrates']
    return list(set(res))


def extract_products(reaction_dict_list: list[dict]):
    """
    :param reaction_dict_list: the output of substratesAndProducts method
    :return: list contains all possible products
    """
    res = []
    for reaction_dict in reaction_dict_list:
        if reaction_dict.get('products', None):
            res = res + reaction_dict['products']
    return list(set(res))


def extract_just_ec_number(ec_number: str):
    """
    :param ec_number: the output of ec_number method
    :return: just ec_number like 2.7.1.69
    """
    ec_number_pattern = r'\b\d+\.\d+\.\d+\.\d+\b'
    ec_numbers = re.findall(ec_number_pattern, ec_number)
    if ec_numbers:
        return ec_numbers[0]
    else:
        return None


def extract_ec_annotation(ec_number: str):
    """
    :param ec_number: the output of ec_number method
    :return: the annotation of the ec_number like (deleted, reaction covered by EC 1.1.1.264)
    """
    ec_number_pattern = r'\b\d+\.\d+\.\d+\.\d+\b'
    ec_numbers = re.findall(ec_number_pattern, ec_number)
    if ec_numbers:
        ec_index = ec_number.find(ec_numbers[0])
        return ec_number[ec_index + len(ec_numbers[0]):].strip()
    else:
        return None
