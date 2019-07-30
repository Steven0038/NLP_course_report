#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: willc
"""


import time

def read_from_file(filename):
    gold = []
    with open(filename, 'r', encoding='utf-8-sig') as fr:
        for line in fr:
            line = line.rstrip()
            goldlist = line.split(' ')

            gold.append(goldlist)
    return gold

def evaluate(target, predict, test=False):
    file_type = "測試" if test else "驗證"
    print("========== " + file_type + "集模型評估 ==========")
    target_gold = read_from_file(target)
    predict_gold = read_from_file(predict)
    start_time = time.time()
    count = 1
    count_right = 0
    count_split = 0
    count_gold = 0
    process_count = 0
    for i in range(len(target_gold)):
        count += 1
        count_split += len(predict_gold[i])
        count_gold += len(predict_gold[i])
        tmp_in = predict_gold[i]
        tmp_gold = target_gold[i]
        for key in tmp_in:
            if key in tmp_gold:
                count_right += 1
                tmp_gold.remove(key)
    P = count_right / count_split
    R = count_right / count_gold
    F = 2 * P * R / (P + R)

    end_time = time.time()
    cost = (end_time - start_time)
    print('Precision:\t', P)
    print('Recall:\t', R)
    print('F:\t', F)
    print("花費時間:\t", cost)
    print("========== " + file_type + "集模型評估完成 ==========")
    print()

    return P, R, F, cost



if __name__ == "__main__":
    target_gold = read_from_file('./dataset/original/test_cws1.txt')
    predict_goal = read_from_file('./dataset/original/test_cws1.txt')
    evaluate(target_gold, predict_goal)
