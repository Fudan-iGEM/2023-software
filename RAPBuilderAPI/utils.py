"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : utils.py
@Author : Zhiyue Chen
@Time : 2023/8/26 2:27
"""
import csv
from datetime import datetime
import os
import shutil
import uuid

# References
# 1. Liu, Y., Wu, Z., Wu, D., Gao, N., & Lin, J. (2023). Reconstitution of Multi-Protein Complexes through
# Ribozyme-Assisted Polycistronic Co-Expression. ACS Synthetic Biology, 12(1), 136–143.
# https://doi.org/10.1021/acssynbio.2c00416
import rapbuilder as rb
from Bio import SeqFeature, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from flask import Response, jsonify

# pre_seq includes ribozyme
pre_seq = 'TTTGTAATGCAGCCGAGGGCGGTTACAAGCCCGCAAAAATAGCAGAGTA'
# default stem loop sequence for RBS design mode
stem_loop_seq = 'AAACACCCACCACAATTTCCACCGTTTCCCGACGCTTCGGCGTCGGG'
# default rbs sequence for stem loop design mode
rbs_seq = 'TTTAAGAAGGAGATATACAT'
geometric_mean_TIR_rbs = 263.4
geometric_mean_TIR_stem_loop = 263.4


def generate_rbs(cds: str, TIR_target: float, is_first: bool = False, is_last: bool = False) -> str:
    """
    :param cds: cds sequence
    :param TIR_target: target TIR
    :param is_first: if the sequence in the first position in pRAP system
    :param is_last: if the sequence in the last position in pRAP system
    :return: estimated rbs
    """
    if is_first and is_last:
        raise ValueError('The position of a sequence cannot be both first and last!')
    elif is_first:
        post_seq = cds + stem_loop_seq
        dG_total, rbs, estimator, iterations = rb.utils.monte_carlo_rbs('', post_seq, TIR_target=TIR_target)
    elif is_last:
        post_seq = cds
        dG_total, rbs, estimator, iterations = rb.utils.monte_carlo_rbs(pre_seq, post_seq, TIR_target=TIR_target)
    else:
        post_seq = cds + stem_loop_seq
        dG_total, rbs, estimator, iterations = rb.utils.monte_carlo_rbs(pre_seq, post_seq, TIR_target=TIR_target)
    return rbs

def generate_stem_loop(TIR_target: float) -> str:
    """
    :param TIR_target: target TIR
    :return: estimated stem loop
    """
    dG_stem_loop, stem_loop, estimator, iterations = rb.utils.monte_carlo_stem_loop(TIR_target)
    return rb.constant.pre_seq_stem_loop + stem_loop


def init_builder(folder_name:str) -> None:
    """
    :param folder_name: name of the folder
    :return: None
    """
    if not os.path.exists(r'./results'):
        os.makedirs(r'./results')
    if not os.path.exists(r'./results/temp'):
        os.makedirs(r'./results/temp')
    if not os.path.exists(os.path.join(r'./results/temp',folder_name)):
        os.makedirs(os.path.join(r'./results/temp',folder_name))


def build_pRAP_system_rbs(data_list: list[dict]) -> tuple[Response, int]:
    """
    :param data_list: list of data of reactions
    :return: json format data that could be used in api
    """
    mode = 'rbs design mode'
    task_id = str(uuid.uuid4())
    filename = 'sequence.gb'
    csv_name = "annotation.csv"
    csv_list = []
    init_builder(task_id)
    sequences = []
    combined_sequence = ''
    loc = 0
    for i, reaction in enumerate(data_list):
        if i == 0:
            is_first = True
        else:
            is_first = False
        if i == len(data_list) - 1:
            is_last = True
        else:
            is_last = False
        cds = reaction.get('sequence')
        optimal_ratio = reaction.get('optimalRatio')
        ec_number = reaction.get('ec_number')
        id = reaction.get('id')
        TIR_target = optimal_ratio * geometric_mean_TIR_rbs
        rbs = generate_rbs(cds, TIR_target, is_first, is_last)
        if is_first:
            combined_sequence += rbs
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs)], 'type': 'rbs',
                              'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs)], 'type': 'rbs',
                              'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence':rbs, 'mode':mode})
            loc += len(rbs)
            combined_sequence += cds
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                              'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                             'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': cds, 'mode':mode})
            loc += len(cds)
            combined_sequence += stem_loop_seq
            sequences.append(
                {'EC_number': ec_number, 'loc': [loc + len(stem_loop_seq) - 20, loc + len(stem_loop_seq)],
                 'type': 'stem_loop', 'description': f'stem-loop for {ec_number} at optimal ratio of {optimal_ratio}',
                 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc + len(stem_loop_seq) - 20, loc + len(stem_loop_seq)],
                             'type': 'stem_loop',
                             'description': f'stem-loop for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': stem_loop_seq, 'mode':mode})
            loc += len(stem_loop_seq)
        elif is_last:
            combined_sequence += pre_seq
            sequences.append({'EC_number': ec_number, 'loc': [loc + 5, loc + len(pre_seq)], 'type': 'ribozyme',
                              'description': f'ribozyme for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc + 5, loc + len(pre_seq)], 'type': 'ribozyme',
                             'description': f'ribozyme for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             "sequence": pre_seq, 'mode':mode})
            loc += len(pre_seq)
            combined_sequence += rbs
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs)], 'type': 'rbs',
                              'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs)], 'type': 'rbs',
                             'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': rbs, 'mode':mode})
            loc += len(rbs)
            combined_sequence += cds
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                              'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                             'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': cds, 'mode':mode})
            loc += len(cds)
        else:
            combined_sequence += pre_seq
            sequences.append({'EC_number': ec_number, 'loc': [loc + 5, loc + len(pre_seq)], 'type': 'ribozyme',
                              'description': f'ribozyme for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc + 5, loc + len(pre_seq)], 'type': 'ribozyme',
                             'description': f'ribozyme for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             "sequence": pre_seq, 'mode':mode})
            loc += len(pre_seq)
            combined_sequence += rbs
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs)], 'type': 'rbs',
                              'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs)], 'type': 'rbs',
                             'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': rbs, 'mode':mode})
            loc += len(rbs)
            combined_sequence += cds
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                              'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                             'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': cds, 'mode':mode})
            loc += len(cds)
            combined_sequence += stem_loop_seq
            sequences.append(
                {'EC_number': ec_number, 'loc': [loc + len(stem_loop_seq) - 20, loc + len(stem_loop_seq)],
                 'type': 'stem_loop', 'description': f'stem-loop for {ec_number} at optimal ratio of {optimal_ratio}',
                 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc + len(stem_loop_seq) - 20, loc + len(stem_loop_seq)],
                             'type': 'stem_loop',
                             'description': f'stem-loop for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': stem_loop_seq, 'mode':mode})
            loc += len(stem_loop_seq)
    now_utc = datetime.utcnow()
    format_date = now_utc.strftime("%d-%b-%Y")
    combined_seq_record = SeqRecord(Seq(combined_sequence), name=task_id[:8],annotations={"date": format_date.upper()})
    combined_seq_record.annotations["molecule_type"] = "DNA"
    for seq_record in sequences:
        feature = SeqFeature.SeqFeature(SeqFeature.FeatureLocation(seq_record['loc'][0], seq_record['loc'][1]),
                                        type=seq_record['type'], qualifiers=seq_record)
        combined_seq_record.features.append(feature)
    with open(os.path.join(r'./results', 'temp', task_id, filename), 'w') as f:
        SeqIO.write(combined_seq_record, f, "genbank")
    # add annotation of sequence
    with open(os.path.join(r'./results', 'temp', task_id, csv_name), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['EC_number', 'loc', 'type', 'description', 'id', 'sequence', 'mode'],
                                delimiter=',')
        writer.writeheader()
        for row in csv_list:
            writer.writerow(row)
    shutil.make_archive(os.path.join(r'./results',task_id), 'zip', os.path.join(r'./results', 'temp', task_id))
    return jsonify({'message': 'Your task is complete!', 'taskID': task_id}), 200


def build_pRAP_system_stem_loop(data_list: list[dict]) -> tuple[Response, int]:
    """
    :param data_list: list of data of reactions
    :return: json format data that could be used in api
    """
    mode = 'stem loop design mode'
    task_id = str(uuid.uuid4())
    filename = 'sequence.gb'
    csv_name = "annotation.csv"
    csv_list = []
    init_builder(task_id)
    sequences = []
    combined_sequence = ''
    loc = 0
    for i, reaction in enumerate(data_list):
        if i == 0:
            is_first = True
        else:
            is_first = False
        if i == len(data_list) - 1:
            is_last = True
        else:
            is_last = False
        cds = reaction.get('sequence')
        optimal_ratio = reaction.get('optimalRatio')
        ec_number = reaction.get('ec_number')
        id = reaction.get('id')
        TIR_target = optimal_ratio * geometric_mean_TIR_stem_loop
        if not is_last:
            stem_loop = generate_stem_loop(TIR_target)
        else:
            stem_loop = None
        if is_first:
            combined_sequence += rbs_seq
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs_seq)], 'type': 'rbs',
                              'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs_seq)], 'type': 'rbs',
                              'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence':rbs_seq, 'mode':mode})
            loc += len(rbs_seq)
            combined_sequence += cds
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                              'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                             'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': cds, 'mode':mode})
            loc += len(cds)
            combined_sequence += stem_loop
            sequences.append(
                {'EC_number': ec_number, 'loc': [loc + 27, loc + len(stem_loop)],
                 'type': 'stem_loop', 'description': f'stem-loop for {ec_number} at optimal ratio of {optimal_ratio}',
                 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc + 27, loc + len(stem_loop)],
                             'type': 'stem_loop',
                             'description': f'stem-loop for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': stem_loop, 'mode':mode})
            loc += len(stem_loop)
        elif is_last:
            combined_sequence += pre_seq
            sequences.append({'EC_number': ec_number, 'loc': [loc + 5, loc + len(pre_seq)], 'type': 'ribozyme',
                              'description': f'ribozyme for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc + 5, loc + len(pre_seq)], 'type': 'ribozyme',
                             'description': f'ribozyme for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             "sequence": pre_seq, 'mode':mode})
            loc += len(pre_seq)
            combined_sequence += rbs_seq
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs_seq)], 'type': 'rbs',
                              'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs_seq)], 'type': 'rbs',
                             'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': rbs_seq, 'mode':mode})
            loc += len(rbs_seq)
            combined_sequence += cds
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                              'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                             'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': cds, 'mode':mode})
            loc += len(cds)
        else:
            combined_sequence += pre_seq
            sequences.append({'EC_number': ec_number, 'loc': [loc + 5, loc + len(pre_seq)], 'type': 'ribozyme',
                              'description': f'ribozyme for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc + 5, loc + len(pre_seq)], 'type': 'ribozyme',
                             'description': f'ribozyme for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             "sequence": pre_seq, 'mode':mode})
            loc += len(pre_seq)
            combined_sequence += rbs_seq
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs_seq)], 'type': 'rbs',
                              'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(rbs_seq)], 'type': 'rbs',
                             'description': f'rbs for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': rbs_seq, 'mode':mode})
            loc += len(rbs_seq)
            combined_sequence += cds
            sequences.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                              'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc, loc + len(cds)], 'type': 'cds',
                             'description': f'cds for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': cds, 'mode':mode})
            loc += len(cds)
            combined_sequence += stem_loop
            sequences.append(
                {'EC_number': ec_number, 'loc': [loc + 27, loc + len(stem_loop)],
                 'type': 'stem_loop', 'description': f'stem-loop for {ec_number} at optimal ratio of {optimal_ratio}',
                 'id': id})
            csv_list.append({'EC_number': ec_number, 'loc': [loc + 27, loc + len(stem_loop)],
                             'type': 'stem_loop',
                             'description': f'stem-loop for {ec_number} at optimal ratio of {optimal_ratio}', 'id': id,
                             'sequence': stem_loop, 'mode':mode})
            loc += len(stem_loop)
    now_utc = datetime.utcnow()
    format_date = now_utc.strftime("%d-%b-%Y")
    combined_seq_record = SeqRecord(Seq(combined_sequence), name=task_id[:8], annotations={"date": format_date.upper()})
    combined_seq_record.annotations["molecule_type"] = "DNA"
    for seq_record in sequences:
        feature = SeqFeature.SeqFeature(SeqFeature.FeatureLocation(seq_record['loc'][0], seq_record['loc'][1]),
                                        type=seq_record['type'], qualifiers=seq_record)
        combined_seq_record.features.append(feature)
    with open(os.path.join(r'./results', 'temp', task_id, filename), 'w') as f:
        SeqIO.write(combined_seq_record, f, "genbank")
    # add annotation of sequence
    with open(os.path.join(r'./results', 'temp', task_id, csv_name), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['EC_number', 'loc', 'type', 'description', 'id', 'sequence', 'mode'],
                                delimiter=',')
        writer.writeheader()
        for row in csv_list:
            writer.writerow(row)
    shutil.make_archive(os.path.join(r'./results', task_id), 'zip', os.path.join(r'./results', 'temp', task_id))
    return jsonify({'message': 'Your task is complete!', 'taskID': task_id}), 200