"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : utils.py
@Author : Zhiyue Chen
@Time : 2023/8/24 0:36
"""
# References
# 1. Liu, Y., Wu, Z., Wu, D., Gao, N., & Lin, J. (2023). Reconstitution of Multi-Protein Complexes through
# Ribozyme-Assisted Polycistronic Co-Expression. ACS Synthetic Biology, 12(1), 136–143.
# https://doi.org/10.1021/acssynbio.2c00416
# 2. Salis, H. (2023). Hsalis/Ribosome-Binding-Site-Calculator-v1.0 [Python].
# https://github.com/hsalis/Ribosome-Binding-Site-Calculator-v1.0 (Original work published 2009)
# 3. Salis, H. M. (2011). The ribosome binding site calculator. Methods in Enzymology, 498, 19–42.
# https://doi.org/10.1016/B978-0-12-385120-8.00002-4
# 4. Lorenz, R., Bernhart, S. H., Höner zu Siederdissen, C., Tafer, H., Flamm, C., Stadler, P. F., &
# Hofacker, I. L. (2011). ViennaRNA Package 2.0. Algorithms for Molecular Biology, 6(1), 26.
# https://doi.org/10.1186/1748-7188-6-26
import random
import re
import sys
from copy import deepcopy

from tqdm import tqdm

from rapbuilder import config
from rapbuilder import constant
import math

from rapbuilder.rbs_predictor import RBSPredictor


def monte_carlo_rbs(pre_seq: str, post_seq: str, TIR_target: float = 0, rbs_init: str = None, dG_target: float = None,
                    max_iter: int = 10000) -> tuple:
    '''
    runs the monte carlo algorithm to find proper RBS accoring to the inputs. Just enter one of TIR_target and dG_target
    :param pre_seq: the pre sequence of the RBS
    :param post_seq: the post sequence of the RBS, generally CDS
    :param TIR_target: target translation initial rate
    :param rbs_init: initial rbs sequence(optional)
    :param dG_target: target delta_G total
    :param max_iter: maximum number of iterations
    :return: a tuple conrains results
    '''
    if TIR_target:
        dG_target = constant.RT_eff * (constant.logK - math.log(TIR_target))
    tol = 0.25  # kcal/mol
    annealing_accept_ratios = [0.01, 0.20]  # first is min, second is max
    annealing_min_moves = 50
    RT_init = 0.6  # roughly 300K
    weighted_moves = [('insert', 0.10), ('delete', 0.10), ('replace', 0.80)]

    # cost function
    def calc_energy(input_dG_total):
        return abs(input_dG_total - dG_target)

    if rbs_init is None:
        rbs, estimator = get_initial_rbs(pre_seq, post_seq, dG_target)
    else:
        rbs = rbs_init
        estimator = run_rbs_predictor(pre_seq, post_seq, rbs)
    counter = 0
    accepts = 0
    rejects = 0
    RT = RT_init
    dG_total = estimator.dG_total_list[0]
    energy = calc_energy(dG_total)
    pbar = tqdm(total=max_iter)
    while energy > tol and counter < max_iter:
        try:
            counter += 1
            move = weighted_choice(weighted_moves)
            rbs_new = ''
            if move == 'insert':
                pos = int(random.uniform(0.0, 1.0) * len(rbs))
                letter = random.choice(list(constant.nucleotides))
                rbs_new = rbs[0:pos] + letter + rbs[pos:]
            if move == 'delete':
                if len(rbs) > 1:
                    pos = int(random.uniform(0.0, 1.0) * len(rbs))
                    rbs_new = rbs[0:pos] + rbs[pos + 1:]
                else:
                    rbs_new = rbs
            if move == 'replace':
                pos = int(random.uniform(0.0, 1.0) * len(rbs))
                letter = random.choice(list(constant.nucleotides))
                rbs_new = rbs[0:pos] + letter + rbs[pos + 1:]
            rbs_new = remove_start_codons(rbs_new)
            if len(rbs_new) > constant.cutoff:
                rbs_new = rbs_new[len(rbs_new) - constant.cutoff:]
            estimator = run_rbs_predictor(pre_seq, post_seq, rbs_new)
            dG_total = estimator.dG_total_list[0]
            energy_new = calc_energy(dG_total)
            if calc_constraints(estimator):
                energy_new = sys.maxsize
            if energy_new < energy:
                rbs = rbs_new
                energy = energy_new
            else:
                ddE = (energy - energy_new)
                metropolis = math.exp(ddE / RT)
                prob = random.uniform(0.0, 1.0)
                if metropolis > prob:
                    # accept move based on conditional probability
                    rbs = rbs_new
                    energy = energy_new
                    accepts += 1
                else:
                    rejects += 1
            if accepts + rejects > annealing_min_moves:
                ratio = float(accepts) / float(accepts + rejects)
                if ratio > annealing_accept_ratios[1]:
                    # too many accepts, reduce RT
                    RT = RT / 2.0
                    accepts = 0
                    rejects = 0
                if ratio < annealing_accept_ratios[0]:
                    # too many rejects, increase RT
                    RT = RT * 2.0
                    accepts = 0
                    rejects = 0
            pbar.update(1)
        except KeyboardInterrupt:
            estimator = run_rbs_predictor(pre_seq, post_seq, rbs)
            dG_total = estimator.dG_total_list[0]
            return dG_total, rbs, estimator, counter
    pbar.close()
    if TIR_target:
        TIR_out = constant.K * math.exp(-dG_total / constant.RT_eff)
        return TIR_out, rbs, estimator, counter
    else:
        return dG_total, rbs, estimator, counter


def get_initial_rbs(pre_seq: str, post_seq: str, dG_target: float) -> tuple:
    """
    generate and select a suitable initial RBS.
    :param pre_seq: the pre sequence of the RBS
    :param post_seq: the post sequence of the RBS, generally CDS
    :param dG_target: target delta_G total
    :return: tuple contains RBS sequence and its RBSPredictor
    """
    pre_length = 25
    dG_target_nondim = (dG_target - constant.dG_range_high) / (constant.dG_range_low - constant.dG_range_high)
    if dG_target_nondim < 0.125:
        p_choose_sd = 0.50
        core_length = 4
        max_nonoptimal_spacing = 10
    elif dG_target_nondim < 0.25:
        p_choose_sd = 0.50
        core_length = 4
        max_nonoptimal_spacing = 10
    elif dG_target_nondim < 0.5:
        p_choose_sd = 0.75
        core_length = 4
        max_nonoptimal_spacing = 10
    elif dG_target_nondim < 0.7:
        p_choose_sd = 0.75
        core_length = 4
        max_nonoptimal_spacing = 5
    elif dG_target_nondim < 0.8:
        p_choose_sd = 0.75
        core_length = 6
        max_nonoptimal_spacing = 5
    elif dG_target_nondim < 0.9:
        p_choose_sd = 0.9
        core_length = 7
        max_nonoptimal_spacing = 3
    elif dG_target_nondim < 0.95:
        p_choose_sd = 0.90
        core_length = 8
        max_nonoptimal_spacing = 3
    else:
        p_choose_sd = 1.0
        core_length = 10
        max_nonoptimal_spacing = 1
    dG_total = constant.dG_range_high + 1
    rbs = None
    estimator = None
    while dG_total > constant.dG_range_high:
        rbs = generate_random_rbs(False, constant.cutoff, pre_length, p_choose_sd, core_length, max_nonoptimal_spacing)
        rbs = remove_start_codons(rbs)
        estimator = run_rbs_predictor(pre_seq, post_seq, rbs)
        rbs = remove_constrain_helical_loop(pre_seq, rbs, estimator)
        rbs, estimator = remove_lower_kinetic_score(pre_seq, post_seq, rbs, estimator)
        dG_total = estimator.dG_total_list[0]
    return rbs, estimator


def generate_random_rbs(all_Random: bool = False, max_length: int = 20, pre_length: int = 5, p_chooseSD: float = 0.5,
                        core_length: int = 6, max_nonoptimal_spacing: int = 5) -> str:
    """
    randomized generation of RBS
    :param all_Random: bool, if randomly generate RBS for each nucleotide
    :param max_length: the max length of RBS
    :param pre_length: the pre length of RBS
    :param p_chooseSD: the probability of selecting a nucleotide sequence in the SD sequence
    :param core_length: length of the selected nucleotide sequence of the SD sequence in RBS
    :param max_nonoptimal_spacing: maximum none-optional spacing length
    :return: RBS sequence
    """
    rbs = []
    if all_Random:
        for i in range(max_length):
            rbs.append(random.choice(["A", "T", "G", "C"]))
        return "".join(rbs)
    for i in range(pre_length):
        rbs.append(random.choice(["A", "T", "G", "C"]))
    core_length = min(len(constant.SD), core_length)
    diff = len(constant.SD) - core_length
    begin = int(random.random() * diff)
    for i in range(core_length):
        rand = random.random()
        if rand <= p_chooseSD:
            rbs.append(constant.SD[begin + i])
        else:
            choices = ["A", "T", "G", "C"]
            choices.remove(constant.SD[begin + i])
            rbs.append(random.choice(choices))
    offset = diff - begin
    spacing = random.choice(range(max(0, offset + constant.optimal_spacing - max_nonoptimal_spacing),
                                  offset + constant.optimal_spacing + max_nonoptimal_spacing))
    for i in range(spacing):
        rbs.append(random.choice(["A", "T", "G", "C"]))
    if len(rbs) > max_length:
        rbs = rbs[len(rbs) - max_length:]
    return "".join(rbs)


def remove_start_codons(rbs: str) -> str:
    """
    remove strat codon of RBS
    :param rbs: RBS sequence
    :return: the RBS sequence that removes potential start codon
    """
    regexp_str = "|".join(["ATG", "AUG", "GTG", "GUG", "TTG", "UUG"])
    pattern = re.compile(regexp_str)
    matches = pattern.finditer(rbs.upper())
    rbs_new = deepcopy(rbs)
    for match in matches:
        start_pos = match.start()
        triplet = [random.choice(['A', 'T', 'G', 'C']), random.choice(['A', 'G', 'C']), random.choice(['A', 'T', 'C'])]
        rbs_new = rbs_new[0:start_pos] + "".join(triplet) + rbs_new[start_pos + 3:]
    matches = pattern.search(rbs_new.upper())
    if matches is None:
        return rbs_new
    else:
        return remove_start_codons(rbs_new)


def remove_constrain_helical_loop(pre_seq: str, rbs: str, estimator: RBSPredictor) -> str:
    """
    remove constrain helical loop of RBS
    :param pre_seq:the pre sequence of RBS
    :param rbs:the sequence of RBS
    :param estimator: RBSPredictor of the mRNA
    :return: RBS sequence that removes constrain helical loop
    """
    structure = estimator.mRNA_structure_list[0]
    helical_loop_list, bulge_loop_list, helical_start_ends, bulge_start_ends = estimator.calc_longest_loop_bulge(
        structure, True, True, rbs)
    rbs_begin = len(pre_seq)
    rbs_end = rbs_begin + len(rbs)
    for (loop_length, start_end) in zip(helical_loop_list, helical_start_ends):
        if loop_length > config.max_helical_loop:
            rbs_range = set(range(rbs_begin + 1, rbs_end + 1))
            loop_range = set(range(start_end[0] + 1, start_end[1]))
            change_range = list(rbs_range & loop_range)
            if change_range:
                pos = random.choice(change_range) - len(pre_seq)
                rbs = rbs[0:pos] + rbs[pos + 1:]
        elif loop_length < config.min_helical_loop:
            RBS_range = set(range(rbs_begin + 1, rbs_end + 1))
            loop_range = set(range(start_end[0] + 1, start_end[1]))
            change_range = list(RBS_range & loop_range)
            if change_range:
                pos = random.choice(change_range) - len(pre_seq)
                letter = random.choice(['A', 'T', 'C', 'G'])
                rbs = rbs[0:pos] + letter + rbs[pos + 1:]
    return rbs


def dsu_sort(idx, seq):
    for i, e in enumerate(seq):
        seq[i] = (e[idx], e)
    seq.sort()
    seq.reverse()
    for i, e in enumerate(seq):
        seq[i] = e[1]
    return seq


def remove_lower_kinetic_score(pre_seq: str, post_seq: str, rbs: str, estimator: RBSPredictor) -> tuple:
    """
    remove RBS with lower kinetic score
    :param pre_seq:the pre sequence of RBS
    :param post_seq:the post sequence of the RBS, generally CDS
    :param rbs:RBS sequence
    :param estimator:RBSPredictor of the mRNA
    :return:tuple contains new RBS and its RBSPredictor
    """
    if estimator is None:
        estimator = run_rbs_predictor(pre_seq, post_seq, rbs)
    kinetic_score = estimator.kinetic_score_list[0]
    while kinetic_score > config.max_kinetic_score:
        structure = estimator.mRNA_structure_list[0]
        mRNA = structure["mRNA"]
        rbs_begin = mRNA.find(rbs)
        rbs_end = rbs_begin + len(rbs)
        ks_list = []
        mfe_res = structure['mfe_res']
        fold = estimator.convert_mfe_bracket_to_numbered_pairs(mfe_res, mRNA)
        bp_x = fold["bp_x"]
        bp_y = fold["bp_y"]
        for (nt_x, nt_y) in zip(bp_x, bp_y):
            ks_list.append((nt_y - nt_x, nt_x, nt_y))
        dsu_sort(0, ks_list)
        num_mutations = min(len(ks_list), 10)
        for i in range(num_mutations):
            nt_x = ks_list[i][1] - 1
            nt_y = ks_list[i][2] - 1
            if rbs_begin <= nt_x < rbs_end:
                pos = nt_x - rbs_begin
                letter = random.choice(list(constant.nucleotides ^ set(rbs[pos])))
                rbs = rbs[0:pos] + letter + rbs[pos + 1:]
            elif rbs_begin <= nt_y < rbs_end:
                pos = nt_x - rbs_begin
                letter = random.choice(list(constant.nucleotides ^ set(rbs[pos])))
                rbs = rbs[0:pos] + letter + rbs[pos + 1:]
            elif len(rbs) < constant.cutoff:
                rbs = random.choice(list(constant.nucleotides)) + rbs
        rbs = remove_start_codons(rbs)
        estimator = run_rbs_predictor(pre_seq, post_seq, rbs)
        kinetic_score = estimator.kinetic_score_list[0]
    return rbs, estimator


def run_rbs_predictor(pre_seq: str, post_seq: str, rbs: str) -> RBSPredictor:
    """
    run RBSPredictor
    :param pre_seq:the pre sequence of RBS
    :param post_seq:the post sequence of the RBS, generally CDS
    :param rbs:RBS sequence
    :return:RBSPredictor of mRNA
    """
    start_range = [len(pre_seq) + len(rbs) - 2, len(pre_seq) + len(rbs) + 2]
    mRNA = pre_seq.upper() + rbs.upper() + post_seq.upper()
    estimator = RBSPredictor(mRNA, start_range)
    estimator.calc_dG()
    return estimator


def weighted_choice(weighted_moves: list[tuple]) -> str:
    """
    choose operation of RBS
    :param weighted_moves:
    :return: the type of the operation
    """
    n = random.uniform(0.0, 1.0)
    item = None
    for item, weight in weighted_moves:
        if n < weight:
            break
        n = n - weight
    return item


def calc_constraints(estimator: RBSPredictor) -> bool:
    """
    calculate if the mRNA meets the constraints
    :param estimator: RBSPredictor of mRNA
    :return: bool result
    """
    kinetic_score = estimator.kinetic_score_list[0]
    three_state_indicator = estimator.three_state_indicator_list[0]
    if kinetic_score > config.max_kinetic_score:
        return True
    if three_state_indicator > config.max_three_state_indicator:
        return True
    return False
