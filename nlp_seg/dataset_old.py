#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 22:36:02 2019

@author: willc
"""

import json, os

class HmmTrain:
    def __init__(self):
        self.line_index = -1
        self.char_set = set()

    def init(self):  # 初始化字典
        trans_dict = {}  # 存儲狀態轉移機率
        emit_dict = {}  # 發射機率(狀態->詞語的條件機率)
        Count_dict = {}  # 存儲所有狀態序列 ，用於歸一化分母
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

        # print(trans_dict) #{'B': {'B': 0.0, 'S': 0.0, 'M': 0.0, 'E': 0.0}, 'S': {'B': 0.0, 'S': 0.0, 'M': 0.0, 'E': 0.0},。。。}
        # print(emit_dict) # {'B': {}, 'S': {}, 'M': {}, 'E': {}}
        # print(start_dict) # {'B': 0.0, 'S': 0.0, 'M': 0.0, 'E': 0.0}
        # print(Count_dict) # {'B': 0, 'S': 0, 'M': 0, 'E': 0}
        return trans_dict, emit_dict, start_dict, Count_dict

    '''保存模型'''

    def save_model(self, word_dict, model_path):
        f = open(model_path, 'w')
        f.write(str(word_dict))
        f.close()

    '''輸出模型'''
    def write2file(self, filename, word_dict, model_path):
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        with open('./' + model_path + '/'+filename+'.json', 'w', encoding='utf-8-sig') as f:
            json.dump(word_dict, f, indent=2, ensure_ascii=False)

    '''詞語狀態轉換'''

    def get_word_status(self, word):  # 根據詞語，輸出詞語對應的SBME狀態
        '''
        S:單字詞
        B:詞的開頭
        M:詞的中間
        E:詞的末尾
        能 ['S']
        前往 ['B', 'E']
        科威特 ['B', 'M', 'E']
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

    '''基於人工標註語料庫，訓練發射機率，初始狀態， 轉移機率'''

    def train(self, train_filepath):
        trans_dict, emit_dict, start_dict, Count_dict = self.init()
        for line in open(train_filepath):
            self.line_index += 1

            line = line.strip()
            if not line:
                continue

            char_list = []
            for i in range(len(line)):
                if line[i] == " ":
                    continue
                char_list.append(line[i])

            self.char_set = set(char_list)  # 訓練預料庫中所有字的集合

            word_list = line.split(" ")
            line_status = []  # 統計狀態序列

            for word in word_list:
                line_status.extend(self.get_word_status(word))  # 一句話對應一行連續的狀態

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

        # print(emit_dict)#{'S': {'否': 10.0, '昔': 25.0, '直': 238.0, '六': 1004.0, '殖': 17.0, '仗': 36.0, '挪': 15.0, '朗': 151.0
        # print(trans_dict)#{'S': {'S': 747969.0, 'E': 0.0, 'M': 0.0, 'B': 563988.0}, 'E': {'S': 737404.0, 'E': 0.0, 'M': 0.0, 'B': 651128.0},
        # print(start_dict) #{'S': 124543.0, 'E': 0.0, 'M': 0.0, 'B': 173416.0}

        # 進行歸一化
        for key in start_dict:  # 狀態的初始機率
            start_dict[key] = start_dict[key] * 1.0 / self.line_index
        for key in trans_dict:  # 狀態轉移機率
            for key1 in trans_dict[key]:
                trans_dict[key][key1] = trans_dict[key][key1] / Count_dict[key]
        for key in emit_dict:  # 發射機率(狀態->詞語的條件機率)
            for word in emit_dict[key]:
                emit_dict[key][word] = emit_dict[key][word] / Count_dict[key]

        # print(emit_dict)#{'S': {'否': 6.211504202703743e-06, '昔': 1.5528760506759358e-05, '直': 0.0001478338000243491,
        # print(trans_dict)#{'S': {'S': 0.46460125869921165, 'E': 0.0, 'M': 0.0, 'B': 0.3503213832274479},
        # print(start_dict)#{'S': 0.41798844132394497, 'E': 0.0, 'M': 0.0, 'B': 0.5820149148537713}

        self.write2file('transition', trans_dict, 'model')
        self.write2file('pi', start_dict, 'model')
        self.write2file('emission', emit_dict, 'model')

        return trans_dict, emit_dict, start_dict


if __name__ == "__main__":
    train_filepath = './train_cws.txt'
    trans_path = './model/prob_trans.model'
    emit_path = './model/prob_emit.model'
    start_path = './model/prob_start.model'
    trainer = HmmTrain()
    trainer.train(train_filepath)
