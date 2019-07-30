#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 10:29:04 2019

@author: willc
"""
import json
from collections import defaultdict
import sys
import os


def read_from_train(filename):
    '''
    統計詞列表和詞性列表
    輸入：訓練語料庫集
    輸出：1. 詞列表, 2. 命名實體標注列表
    '''
    words_list = []
    postags_list = []
    with open(filename, 'r', encoding='utf-8-sig') as fr:
        for line in fr.readlines():
            line = line.rstrip()
            line = line.split(' ')
            for word in line:
                #word = word.split('/')
                if word == '':
                    pass
                elif word[0] == '/':
                    words_list.append(word[0])
                    postags_list.append(word.split('/')[-1])
                
                elif len(word.split('/')) == 3:
                    words_list.append(word.split('/')[0])
                    rr = word.split('/')[1] + '/' + word.split('/')[2]
                    postags_list.append(rr)
                else:
                    words_list.append(word.split('/')[0])
                    postags_list.append(word.split('/')[1])
        
    
    return words_list, postags_list

def cal_vocab(word_list):
    '''
    統計ner頻
    輸入：ner列表
    輸出：ner頻字典
    '''
    vocab = defaultdict(int)
    for w in range(len(word_list)):
        vocab[word_list[w]] += 1
    return vocab

def cal_postag_set(postags_list):
    '''
    統計ner集合
    輸入：ner列表
    輸出：ner集合
    '''
    pos   = set()
    for p in range(len(postags_list)):
        pos.add(postags_list[p])
    return pos
    

def cal_pi(postags_list):
    '''
    計算初始概率
    輸入：ner列表
    輸出：初始概率字典
    '''
    # 計算初始 pi頻率次數
    pi_freq = defaultdict(int)
    for tag in range(len(postags_list)):
        pi_freq[postags_list[tag]] += 1
    
    # 將頻率次數轉成概率
    pi = freq2prob(pi_freq, True)
    return pi


def cal_transition(pos_set, postags_list):
    '''
    計算詞性轉移概率
    輸入：詞集合, ner列表
    輸出：ner轉移概率字典
    '''
    # 計算初始轉移頻率次數
    transition_freq = {}
    for p in pos_set:
        transition_freq[p] = defaultdict(int)
    for tag in range(len(postags_list)):
        if tag != len(postags_list)-1:
            transition_freq[postags_list[tag]][postags_list[tag+1]] += 1
    for p1 in pos_set:
        for p2 in pos_set:
            if p2 not in transition_freq[p1]:
                transition_freq[p1][p2] = 1e-3
    # 將頻率次數轉成概率
    transition = freq2prob(transition_freq)
    return transition

def cal_emission(pos_set, postags_list, words_list, vocab):
    '''
    計算放射概率
    輸入：ner集合, ner列表, 詞列表, 詞集合
    輸出：放射概率字典
    '''
    # 計算初始轉發射頻率次數
    emission_freq = {}
    for p in pos_set:
        emission_freq[p] = defaultdict(int)
    for tag in range(len(postags_list)):
        emission_freq[postags_list[tag]][words_list[tag]] += 1
    for p in pos_set:
        for v in vocab:
            if v not in emission_freq[p]:
                emission_freq[p][v] = 1e-3
    # 將頻率次數轉成概率
    emission = freq2prob(emission_freq)
    return emission
    
    
def freq2prob(dic, pi=False):
    '''
    輸入：頻率字典
    輸出：概率字典
    '''
    resdict = dic.copy()
    if pi:
        sum_freq = sum(dic.values())
        for k in resdict.keys():
            resdict[k] = resdict[k]/sum_freq
        return resdict
        
    
    for k in resdict.keys():
        count = 0
        for kk in dic[k].keys():
            count += (dic[k][kk])
        for kk in dic[k].keys():
            resdict[k][kk] = resdict[k][kk]/count
    return resdict
            

def write2file(dirpath, pi, transition, emission):
    '''
    存儲參數模型
    輸入：目標文件夾, 初始概率字典, 詞性轉移概率字典, 放射概率字典
    '''
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
   
    with open('./'+dirpath+'/pi.json','w', encoding='utf-8-sig') as f:
        json.dump(pi,f,indent=2,ensure_ascii=False)

    with open('./'+dirpath+'/transition.json','w', encoding='utf-8-sig') as f:
        json.dump(transition,f,indent=2,ensure_ascii=False)

    with open('./'+dirpath+'/emission.json','w', encoding='utf-8-sig') as f:
        json.dump(emission,f,indent=2,ensure_ascii=False)
        
def model_param_proccessing():
    print("========== 模型參數生成 ==========")
    MIN_COUNT = 1 # 最小保留詞的頻率
    
    print ('載入訓練數據...')
    try:
        #詞列表, 詞性列表
        words_list, postags_list = read_from_train("./dataset/proccessed/train/ner_tag_com.txt")
        # 詞頻字典
        vocab = cal_vocab(words_list) 
        # 詞性集合
        pos   = cal_postag_set(postags_list) 
        #根据最小词频过滤词汇表
        vocab = [w[0] for w in vocab.items() if w[1] >= MIN_COUNT]
    except:
        print ('載入失敗...')
        sys.exit(0)

    
    print ('載入成功，開始訓練...')
    try:
        # 初始概率
        pi = cal_pi(postags_list)
        # 轉移概率
        transition = cal_transition(pos, postags_list)
        #放射概率
        emission = cal_emission(pos, postags_list, words_list, vocab)
    except:
        print ('訓練出錯...')
        sys.exit(0)
    
    
    print ('訓練完成，保存參數模型...')
    try:
        # 保存參數模型
        write2file('model', pi, transition, emission)
        print ('保存成功...')
    except:
        print ('保存失敗...')
        sys.exit(0)
    print("========== 模型參數生成完成 ==========")
    print()
    
    
    
if __name__ == "__main__":
    model_param_proccessing()
    