#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:27:31 2019

@author: willc
"""
from collections import defaultdict
import json
import re

def find_last_time_max_prob_and_state(states, viterbi_matrix, T):
    max_prob_final_state = None
    max_prob = 0
    for state in states:
        if viterbi_matrix[T-1][state] > max_prob:
            max_prob = viterbi_matrix[T-1][state]
            max_prob_final_state = state
    return max_prob_final_state, max_prob

def traceback(traceback_matrix, max_prob_final_state, T):
    best_path = [max_prob_final_state]
    for time in range(T-1, 0, -1):
        try:
            prev_state = traceback_matrix[time][best_path[-1]]
            best_path.append(prev_state)
        except:
            best_path.append(None)
    return list(reversed(best_path))
    
    

def viterbi(obs, pi, transition, emission):
    viterbi_matrix = defaultdict(dict)
    traceback_matrix = defaultdict(dict)
    
    STATUS_LEN = len(transition)
    OBS_LEN = len(obs)
    
    # hidden states
    # 給出句子, 計算其最有可能的 hidden state(詞性) 序列
    states = transition.keys()
    
    # 計算第一個詞的詞性, 初始化兩個矩陣
    for state in states:
        # like normal in emission[healthy]
        if obs[0] in emission[state]: 
            viterbi_matrix[0][state] = pi[state] * emission[state][obs[0]]
        else:
            viterbi_matrix[0][state] = 1e-4
        traceback_matrix[0][state] = '<start>'
        
    def get_max_from_dict(time, to_state):
        max_prob = max_state = 0
        for s in states:
            # example:
            # health -> health, health -> cold; health -> fever, fever -> cold
            if obs[time] in emission[to_state]:
                prob = viterbi_matrix[time-1][s] * transition[s][to_state] * emission[to_state][obs[time]]
            else:
                prob = viterbi_matrix[time-1][s] * transition[s][to_state] * 1e-4
            
            if prob > max_prob:
                max_prob = prob
                max_state = s
        
        return max_prob, max_state
    
    # 遞推, 從第二個詞開始
    for time in range(1, OBS_LEN): # 觀測序列長度
        for state in states:
            max_prob, max_state = get_max_from_dict(time, state)
            viterbi_matrix[time][state] = max_prob
            traceback_matrix[time][state] = max_state
    
    # 查找最後時刻的最大概率和相應狀態
    max_prob_final_state, max_prob = find_last_time_max_prob_and_state(states, viterbi_matrix, OBS_LEN)
    
    
    return traceback(traceback_matrix, max_prob_final_state, OBS_LEN)
    
