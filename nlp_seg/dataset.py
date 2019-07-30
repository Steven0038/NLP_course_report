#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: willc
"""

import json
from collections import defaultdict
import sys
import os

def init_dict():
    trans_dict = {}  # 存儲狀態轉移機率
    emit_dict = {}  # 發射機率(狀態->詞語的條件機率)
    Count_dict = {}  # 存儲所有狀態序列 ，用於歸一化分母，每個狀態出現的次數
    start_dict = {}  # 存儲狀態的初始機率
    state_list = ['B', 'M', 'E', 'S']  # 狀態序列

    for state in state_list:
        trans_dict[state] = {}
        for state1 in state_list:
            trans_dict[state][state1] = 0.0

    for state in state_list:
        start_dict[state] = 0.0
        emit_dict[state] = {}
        Count_dict[state] = 0

    return trans_dict, emit_dict, start_dict, Count_dict

'''輸出模型'''
def write2file(filename, word_dict, model_path):
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    with open('./' + model_path + '/' + filename + '.json', 'w', encoding='utf-8-sig') as f:
        json.dump(word_dict, f, indent=2, ensure_ascii=False)

def split2combine(filename, outname, outputpath, test=False):
    '''
    將分詞後的文件還原成為分詞狀態
    :param filename:
    :param outname:
    :param putpath:
    :return:
    '''
    file_type = "測試" if test else "驗證"
    print("========== 還原"+file_type+"集文件 ==========")

    with open(filename, 'r', encoding='utf-8-sig') as fr, open(outputpath+'/'+outname+'.txt','w', encoding='utf-8-sig') as outp:
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)
        for line in fr:
            line = line.rstrip()
            sentence = line.replace(' ', '')
            outp.write(sentence + '\n')
    print("========== 還原"+file_type+"集文件完成 ==========")
    print()

'''根據詞語，輸出詞語對應的SBME狀態'''
def get_word_status(word):
    '''
    S:單字詞
    B:詞的開頭
    M:詞的中間
    E:詞的末尾
    '''
    word_status = []
    if len(word) == 1:
        word_status.append('S')
    elif len(word) == 2:
        word_status = ['B', 'E']
    else:
        M_num = len(word) - 2
        M_list = ['M'] * M_num
        word_status.append('B')
        word_status.extend(M_list)
        word_status.append('E')
    return word_status

def train(train_filepath, output_path):

    print("========== 模型參數生成 ==========")
    line_index = 0
    char_set = set()
    trans_dict, emit_dict, start_dict, Count_dict = init_dict()

    print('載入訓練數據, 開始訓練...')

    for line in open(train_filepath, encoding='utf-8-sig'):
        line_index += 1
        line = line.strip()
        if not line:
            continue

        char_list = []
        for i in range(len(line)):
            if line[i] == " ":
                continue
            char_list.append(line[i])

        char_set = set(char_list)  # 訓練預料庫中所有字的集合

        word_list = line.split(" ")
        line_status = []  # 統計狀態序列

        for word in word_list:
            line_status.extend(get_word_status(word))  # 一句話對應一行連續的狀態

        if len(char_list) == len(line_status):
            # print(word_list) # ['但', '從', '生物學', '眼光', '看', '就', '並非', '如此', '了', '。']
            # print(line_status) # ['S', 'S', 'B', 'M', 'E', 'B', 'E', 'S', 'S', 'B', 'E', 'B', 'E', 'S', 'S']
            # print('******')
            for i in range(len(line_status)):
                if i == 0:  # 如果隻有一個詞，則直接算作是初始機率
                    start_dict[line_status[0]] += 1  # start_dict記錄句子第一個字的狀態，用於計算初始狀態機率
                    Count_dict[line_status[0]] += 1  # 記錄每一個狀態的出現次數
                else:  # 統計上一個狀態到下一個狀態，兩個狀態之間的轉移機率
                    trans_dict[line_status[i - 1]][line_status[i]] += 1  # 用於計算轉移機率
                    Count_dict[line_status[i]] += 1
                    # 統計發射機率
                    if char_list[i] not in emit_dict[line_status[i]]:
                        emit_dict[line_status[i]][char_list[i]] = 0.0
                    else:
                        emit_dict[line_status[i]][char_list[i]] += 1  # 用於計算發射機率
        else:
            continue

    # 進行歸一化
    for key in start_dict:  # 狀態的初始機率
        start_dict[key] = start_dict[key] * 1.0 / line_index
    for key in trans_dict:  # 狀態轉移機率
        for key1 in trans_dict[key]:
            trans_dict[key][key1] = trans_dict[key][key1] / Count_dict[key]
    for key in emit_dict:  # 發射機率(狀態->詞語的條件機率)
        for word in emit_dict[key]:
            emit_dict[key][word] = emit_dict[key][word] / Count_dict[key]

    print('訓練完成，保存參數模型...')
    #輸出參數模型
    write2file('transition', trans_dict, output_path)
    write2file('pi', start_dict, output_path)
    write2file('emission', emit_dict, output_path)
    write2file('count', Count_dict, output_path)
    print('保存成功...')
    print("========== 模型參數生成完成 ==========")
    print()

    return trans_dict, emit_dict, start_dict




if __name__ == "__main__":
    train('./train_cws.txt', 'model2')