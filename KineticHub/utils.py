"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : utils.py
@Author : Zhiyue Chen
@Time : 2023/7/28 4:09
"""
import re
from copy import deepcopy
from typing import Any

import brendapyrser


def extract_substrates(reaction_dict_list: list[dict]) -> list[Any]:
    """
    :param reaction_dict_list: the output of substratesAndProducts method
    :return: list contains all possible substrates
    """
    res = []
    for reaction_dict in reaction_dict_list:
        if reaction_dict.get('substrates', None):
            res = res + reaction_dict['substrates']
    return list(set(res))


def extract_products(reaction_dict_list: list[dict]) -> list[Any]:
    """
    :param reaction_dict_list: the output of substratesAndProducts method
    :return: list contains all possible products
    """
    res = []
    for reaction_dict in reaction_dict_list:
        if reaction_dict.get('products', None):
            res = res + reaction_dict['products']
    return list(set(res))


def extract_just_ec_number(ec_number: str) -> Any | None:
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


def extract_ec_annotation(ec_number: str) -> Any | None:
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


def parse_kcat(reaction: brendapyrser.Reaction) -> dict:
    """
    :param reaction: brendapyrser.parser.Reaction
    :return: dict with pure meta for kcat
    """
    res = reaction.Kcatvalues
    reference = reaction.references
    species = reaction.getSpeciesDict()
    species_pattern = r'#(.*?)#'
    reference_pattern = r'<(.*?)>'
    for substrates in reaction.Kcatvalues.keys():
        value_list = reaction.Kcatvalues[substrates]
        value_list_res = deepcopy(value_list)
        for i, value in enumerate(value_list):
            value_res = deepcopy(value)
            if value['meta']:
                reference_id_sub = re.findall(reference_pattern, value['meta'])
                species_id_sub = re.findall(species_pattern, value['meta'])
                meta = re.sub(species_pattern, '', value['meta'])
                meta = re.sub(reference_pattern, '', meta)[1:-1]
                value_res['meta'] = meta
                species_name_sub = set([species.get(j).get('name') for j in species_id_sub if species.get(j)])
                reference_name_sub = set([reference.get(j) for j in reference_id_sub])
                value_res['species'] = list(species_name_sub.union(set(value['species'])))
                value_res['refs'] = list(reference_name_sub.union(set(value['refs'])))
                value_list_res[i] = value_res
        res[substrates] = value_list_res
    return res


def parse_km(reaction: brendapyrser.Reaction) -> dict:
    """
    :param reaction: brendapyrser.parser.Reaction
    :return: dict with pure meta for km
    """
    res = reaction.KMvalues
    reference = reaction.references
    species = reaction.getSpeciesDict()
    species_pattern = r'#(.*?)#'
    reference_pattern = r'<(.*?)>'
    for substrates in reaction.KMvalues.keys():
        value_list = reaction.KMvalues[substrates]
        value_list_res = deepcopy(value_list)
        for i, value in enumerate(value_list):
            value_res = deepcopy(value)
            if value['meta']:
                reference_id_sub = re.findall(reference_pattern, value['meta'])
                species_id_sub = re.findall(species_pattern, value['meta'])
                meta = re.sub(species_pattern, '', value['meta'])
                meta = re.sub(reference_pattern, '', meta)[1:-1]
                value_res['meta'] = meta
                species_name_sub = set([species.get(j).get('name') for j in species_id_sub if species.get(j)])
                reference_name_sub = set([reference.get(j) for j in reference_id_sub])
                value_res['species'] = list(species_name_sub.union(set(value['species'])))
                value_res['refs'] = list(reference_name_sub.union(set(value['refs'])))
                value_list_res[i] = value_res
        res[substrates] = value_list_res
    return res


def parse_species(reaction: brendapyrser.Reaction) -> dict:
    """
    :param reaction: brendapyrser.parser.Reaction
    :return: dict with full references
    """
    species_dict = reaction.getSpeciesDict()
    reference = reaction.references
    res = deepcopy(species_dict)
    for key in species_dict.keys():
        res_refs = []
        for i in species_dict.get(key).get('refs'):
            try:
                res_refs.append(reference[i])
            except KeyError as e:
                pass
        res[key]['refs'] = res_refs
    return res


def merge_substrates(substrates_list: list[str], reaction: brendapyrser.parser.Reaction) -> list[set]:
    """
    :param substrates_list: list contains substrates in Reaction
    :param reaction: brendapyrser.parser.Reaction
    :return: list contains both substrates in k_m and k_cat
    """
    substrates_km = set(parse_km(reaction).keys())
    substrates_kcat = set(parse_kcat(reaction).keys())
    return list(set(substrates_list) | substrates_kcat | substrates_km)
