  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:36:14 2019

@author: willc
"""

from viterbi import viterbi
import json
import sys, os, math

def load_model(dirname):

    with open('./'+ dirname +'/pi.json', encoding='utf-8-sig') as f:
        pi = json.load(f)
    with open('./'+ dirname +'/transition.json', encoding='utf-8-sig') as f:
        transition = json.load(f)
    with open('./'+ dirname +'/emission.json', encoding='utf-8-sig') as f:
        emission = json.load(f)
    return pi, transition, emission


def cut(sent, pos_list):
    '''
    將標註好的結果套用回原本的句子裡
    :param sent:
    :param pos_list:
    :return:
    '''
    seglist = list()
    word = list()
    for index in range(len(pos_list)):
        if pos_list[index] == 'S':
            word.append(sent[index])
            seglist.append(word)
            word = []
        elif pos_list[index] in ['B', 'M']:
            word.append(sent[index])
        elif pos_list[index] == 'E':
            word.append(sent[index])
            seglist.append(word)
            word = []
    seglist = [''.join(tmp) for tmp in seglist]
    return seglist

def start_tagging(filename, outname, outpath, sepnum=50, test=False):
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    file_type = "測試" if test else "驗證"

    print("========== " + file_type + "集標注 ==========")
    print("載入模型參數...")
    pi, transition, emission = load_model('model')

    print("載入模型參數...")
    print("讀取" + file_type + "集進行HMM+Viterbi標註...")
    with open(filename, 'r', encoding='utf-8-sig') as fr:
        for line in fr:
            sent_list = []
            sent_temp=""
            line = line.rstrip()
            for car in line:
                if car != '。':
                    sent_temp = sent_temp + car
                elif car == '。':
                    sent_temp = sent_temp + car
                    if len(sent_temp) > sepnum:
                        f = math.floor(len(sent_temp) / sepnum)
                        m = len(sent_temp) % sepnum
                        i = 0
                        while i<f:
                            sent_list.append(sent_temp[sepnum * i:sepnum * (i+1)])
                            i+=1
                        if m != 0:
                            sent_list.append(sent_temp[sepnum * (i): (sepnum * (i))+m])
                        sent_temp = ""
                    else:
                        sent_list.append(sent_temp)
                        sent_temp = ''


            if sent_temp != '':
                sent_list.append(sent_temp)


            seg = []
            # HMM, 維特比分詞
            for sent in sent_list:
                pos_list = viterbi(sent, pi, transition, emission)

                # 將標註好的結果套用回原本的句子裡
                seglist = cut(sent, pos_list)
                seg.append(seglist)

            # 追加寫回文本中
            with open(outpath + '/' + outname + '.txt', 'a', encoding='utf-8-sig') as outp:
                for line in seg:
                    for word in line:
                        outp.write(word + ' ')
                outp.write('\n')
    print("========== " + file_type + "集標注完成 ==========")
    print()


if __name__ == '__main__':
    pi, transition, emission = load_model('model')
    start_tagging('test_cws1.txt', sepnum=100)

