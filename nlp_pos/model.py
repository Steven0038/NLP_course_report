  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:36:14 2019

@author: willc
"""

from viterbi import viterbi
from collections import defaultdict
import json
import re
import sys
import os
import math

def load_model(dirname):

    with open('./'+ dirname +'/pi.json', encoding='utf-8-sig') as f:
        pi = json.load(f)
    with open('./'+ dirname +'/transition.json', encoding='utf-8-sig') as f:
        transition = json.load(f)
    with open('./'+ dirname +'/emission.json', encoding='utf-8-sig') as f:
        emission = json.load(f)
    return pi, transition, emission

def tagging(obs, pi, transition, emission):
    pred_path = []
    for sent in obs:
        path = viterbi(sent, pi, transition, emission)
        pred_path.append(path)
    return pred_path

def output_pred(obs, pred_path):
    ouput = []
    for sent in range(len(obs)):
        #ouput.append([[obs[sent], pred_path[sent]] for (obs[sent], pred_path[sent]) in list(zip(obs[sent], pred_path[sent]))])
        temp = [[obs[sent], pred_path[sent]] for (obs[sent], pred_path[sent]) in list(zip(obs[sent], pred_path[sent]))]
        for res in temp:
            ouput.append(res)
    return ouput


def tag_and_write2file(filename, outputname, sepnum=50, outputpath="./result_file", test=False):
    file_type = "測試" if test else "驗證"

    print("========== 將" + file_type + "集標註並輸出成文件 ==========")

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    # 載入模型

    pi, transition, emission = load_model('model')
    #read_list = []
    with open(filename, 'r', encoding='utf-8-sig') as fr:
        # train_data = fr.read()
        temp = []
        for line in fr:
            read_list = []
            line = line.rstrip()
            ln = line.split(" ")
            for w in ln:
                if w != '。':
                    temp.append(w)
                elif w == '。':
                    temp.append('。')
                    if len(temp) > sepnum:
                        f = math.floor(len(temp)/sepnum)
                        m = len(temp)%sepnum
                        i=0
                        while i<f:
                            read_list.append(temp[sepnum * i:sepnum * (i+1)])
                            i+=1
                        if m != 0:
                            read_list.append(temp[sepnum * (i-1): (sepnum * (i-1))+m])
                        temp = []
                    else:
                        read_list.append(temp)
                        temp = []
            if len(temp) != 0:
                read_list.append(temp)
                temp = []

            # HMM, 維特比 pos 標註
            pos_list = []
            for sent in read_list:
                pos = viterbi(sent, pi, transition, emission)
                pos_list.append(pos)

            # 追加寫回文本中
            with open(outputpath + '/' + outputname + '.txt', 'a', encoding='utf-8-sig') as outp:
                for line in range(len(read_list)):
                    for word in range(len(read_list[line])):
                        #outp.write(word + ' ')
                        # 判斷是否為英文字串
                        x = re.match('^[a-zA-Z]+$', read_list[line][word])
                        if read_list[line][word] == "$$_":
                            # 如果為 &&_ 則不標註
                            outp.write(read_list[line][word] + ' ')
                        elif x != None:
                            # 如果為英文字串，將其標為 nx
                            outp.write(read_list[line][word] + '/' + 'nx' + ' ')
                        else:
                            outp.write(read_list[line][word] + "/" + pos_list[line][word] + ' ')
                outp.write('\n')

    print("========== 將" + file_type + "集輸出完成 ==========")
    print()

def read_from_test(filename, sepnum=50):

    read_list = []
    with open(filename, 'r', encoding='utf-8-sig') as fr:
        # train_data = fr.read()
        temp = []
        for line in fr:
            line = line.rstrip()
            ln = line.split(" ")
            for w in ln:
                if w != '。':
                    temp.append(w)
                elif w == '。':
                    temp.append('。')
                    if len(temp) > sepnum:
                        f = math.floor(len(temp) / sepnum)
                        m = len(temp) % sepnum
                        i = 0
                        while i < f:
                            read_list.append(temp[sepnum * i:sepnum * (i + 1)])
                            i += 1
                        if m != 0:
                            read_list.append(temp[sepnum * (i - 1): (sepnum * (i - 1)) + m])
                        temp = []
                    else:
                        read_list.append(temp)
                        temp = []
            if len(temp) != 0:
                read_list.append(temp)
                temp = []

    return read_list


def handle_dollar_sign(tag_list):
    '''
    將 $$_ 對應的標註設為空
    '''
    for n in range(len(tag_list)):
        if tag_list[n][0] == '$$_':
            tag_list[n][1] = ""

def write2file(output, filename, dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open('./'+ dirname +'/'+ filename +'.json', 'w', encoding='utf-8-sig') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
def start_tagging(filename, outpath, sepnum=50, test=False, handle_space=False):

    file_type = "測試" if test else "驗證"

    print("========== " + file_type + "集標注 ==========")

    # 載入參數模型
    print("載入參數模型...")
    try:
        pi, transition, emission = load_model('model')
        print("載入模型完成...")
    except:
        print ('載入模型失敗...')
        sys.exit(0)

    # 讀取測試集
    print("讀取測試集...")
    try:
        obser_val = read_from_test(filename, sepnum)
        print("讀取完成...")
    except:
        print ('讀入測試集失敗...')
        sys.exit(0)

    # 進行 HMM - Viterbi 標註
    print("進行 HMM - Viterbi 標註...")
    pred_path = tagging(obser_val, pi, transition, emission)
    print ("標注完成...")


    # 輸出標注結果
    print("導出標注結果...")
    try:
        tagged_result = output_pred(obser_val, pred_path)
        if handle_space:
            handle_dollar_sign(tagged_result)
        write2file(tagged_result, "tagged", outpath)
        print("導出成功")
    except:
        print ('導出失敗')
        sys.exit(0)

    print("========== " + file_type + "集標注完成 ==========")
    print()

if __name__ == "__main__":
    read_from_test('./dataset/original/test_cws1.txt')


