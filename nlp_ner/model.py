  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:36:14 2019

@author: willc
"""

from viterbi import viterbi
import json
import sys, os, math, re

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
        temp = [[obs[sent], pred_path[sent]] for (obs[sent], pred_path[sent]) in list(zip(obs[sent], pred_path[sent]))]
        for res in temp:
            ouput.append(res)
    return ouput

def tag_and_write2file(filename, outputname, sepnum=50, outputpath="./result_file", test=False):
    file_type = "測試" if test else "驗證"

    print("========== 將" + file_type + "集標註並輸出成文件 ==========")

    # 檢查是否有存在目標文件夾，若無則創建
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
            ner_list = []
            for sent in read_list:
                ner = viterbi(sent, pi, transition, emission)
                ner_list.append(ner)
            # print(len(ner_list))
            # print(len(read_list))

            # 追加寫回文本中
            with open(outputpath + '/' + outputname + '.txt', 'a', encoding='utf-8-sig') as outp:
                for line in range(len(read_list)):
                    for word in range(len(read_list[line])) :
                        # outp.write(read_list[line][word] + "/" + ner_list[line][word] + ' ')
                        ner_split = ner_list[line][word].split('/')
                        #print(ner_split)
                        if word == len(read_list[line])-1:
                            if ner_list[line][word] == '0':
                                outp.write(read_list[line][word] + ' ')

                                break
                            elif len(ner_split) == 1:
                                S = ner_list[line][word][0]
                                # print(S)
                                NER = ner_list[line][word][2:]
                                #print(NER)
                                if S == "B":
                                    outp.write("[" + read_list[line][word] + "]" + NER + ' ')
                                else:
                                    outp.write(read_list[line][word] + "]" + NER + ' ')
                            elif len(ner_split) == 2:
                                S1 = ner_split[0][0]
                                S2 = ner_split[1][0]
                                NER1 = ner_split[0][2:]
                                NER2 = ner_split[1][2:]
                                if S1 == 'B':
                                    outp.write("[" + read_list[line][word] + "]" + NER1 + ']' + NER2 + ' ')
                                else:
                                    outp.write(read_list[line][word] + "]" + NER1 + ']' + NER2 + ' ')
                        elif ner_list[line][word] == '0':
                            outp.write(read_list[line][word] + ' ')
                        elif len(ner_split) == 1:
                            S = ner_list[line][word][0]
                            NER = ner_list[line][word][2:]
                            # print(NER)
                            if S == "B":
                                ner_split_next = ner_list[line][word + 1].split('/')
                                if len(ner_split_next) == 1:
                                    if (ner_list[line][word + 1][0] == 'M' or ner_list[line][word + 1][0] == "E") and (ner_list[line][word + 1][2:] == NER):
                                        outp.write("[" + read_list[line][word] + ' ')
                                    else:
                                        outp.write("[" + read_list[line][word] + "]" + NER + ' ')
                                elif len(ner_split_next) == 2:
                                    if (ner_split_next[1][0] == 'M' or ner_split_next[1][0] == "E") and (ner_split_next[1][2:] == NER):
                                        outp.write("[" + read_list[line][word]+' ')
                                    else:
                                        outp.write("[" + read_list[line][word] + "]" + NER + ' ')
                            elif S == "M":
                                outp.write(read_list[line][word] + ' ')
                            elif S == "E":
                                outp.write(read_list[line][word] + ']' + NER + ' ')
                        elif len(ner_split) == 2:
                            S1 = ner_split[0][0]
                            S2 = ner_split[1][0]
                            NER1 = ner_split[0][2:]
                            NER2 = ner_split[1][2:]


                            if S1 == "B" and S2 == "B" :  # [[key]bod ...]ner
                                ner_split_next = ner_list[line][word + 1].split('/')
                                if len(ner_split_next) == 1:
                                    if ner_list[line][word + 1][0] != 'M' and ner_list[line][word + 1][0] != 'E':
                                        outp.write("[[" + read_list[line][word] + "]"+ NER1 + ']'+ NER2 + ' ')
                                    else:
                                        outp.write("[[" + read_list[line][word] + "]" + NER1 + ' ')
                                elif len(ner_split_next) == 2:
                                    if ner_split_next[0][0] != 'M' and ner_split_next[0][0] != 'E':
                                        outp.write("[[" + read_list[line][word] + "]" + NER1 + ']' + NER2 + ' ')
                                    else:
                                        outp.write("[[" + read_list[line][word] +  ' ')

                            elif S1 == "B" and S2 == "M":  # [...[key]bod ...]ner:
                                ner_split_next = ner_list[line][word + 1].split('/')
                                if len(ner_split_next) == 1:
                                    if ner_list[line][word + 1][0] != 'M' and ner_list[line][word + 1][0] != 'E':
                                        outp.write("[" + read_list[line][word] + "]"+ NER1 + ']'+ NER2 + ' ')
                                    else:
                                        outp.write("[" + read_list[line][word] + "]" + NER1 + ' ')
                                elif len(ner_split_next) == 2:
                                    if ner_split_next[0][0] != 'M' and ner_split_next[0][0] != 'E':
                                        outp.write("[" + read_list[line][word] + "]"+ NER1 + ']'+ NER2 + ' ')
                                    else:
                                        outp.write("[" + read_list[line][word] + ' ')

                            elif S1 == "B" and S2 == "E":  # [...[key]bod]ner:
                                ner_split_next = ner_list[line][word + 1].split('/')
                                outp.write("[" + read_list[line][word] + "]" + NER1 + ']' + NER2 + ' ')

                            elif S1 == "M" and S2 == "B":
                                # 沒有這種情況ㄅ
                                pass
                            elif S1 == "M" and S2 == "M":  # [...[key key2 key3]bod]ner
                                outp.write(read_list[line][word] + ' ')
                            elif S1 == "M" and S2 == "E":
                                # 沒有這種情況ㄅ
                                pass
                            elif S1 == "E" and S2 == "B":
                                # 沒有這種情況ㄅ
                                pass
                            elif S1 == "E" and S2 == "M": # [...[key key2 key3]bod...]ner
                                outp.write(read_list[line][word] + ']' + NER1 + ' ')
                            elif S1 == "E" and S2 == "E": # [...[key key2 key3]bod]ner
                                outp.write(read_list[line][word] + ']' + NER1 + "]" + NER2 + ' ')
                        # else:
                        #     outp.write(read_list[line][word] + "/" + ner_list[line][word] + ' ')
                outp.write('\n')

    print("========== 將" + file_type + "集輸出完成 ==========")
    print()


def read_from_file(filename, sepnum=50):
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

    return read_list

def write2file(output, filename, dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open('./'+ dirname +'/'+ filename +'.json', 'w', encoding='utf-8-sig') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
def start_tagging(filename, outpath,test=False, sepnum=50):

    file_type = "測試" if test else "驗證"

    print("========== "+file_type+"集標注 ==========")

    # 載入參數模型
    print("載入模型參數...")
    try:
        pi, transition, emission = load_model('model')
        print("載入參數完成...")
    except:
        print ('載入參數失敗...')
        sys.exit(0)

    # 讀取測試集
    print("讀取"+file_type+"集...")
    try:
        obser_val = read_from_file(filename, sepnum)
        print("讀取完成...")
    except:
        print ('讀入'+file_type+'集失敗...')
        sys.exit(0)

    # 進行 HMM - Viterbi 標註
    print("進行 HMM - Viterbi 標註...")
    try:
        pred_path = tagging(obser_val, pi, transition, emission)
        print ("標注完成...")
    except:
        print ('OOPS 發生錯誤了！')
        sys.exit(0)

    # 輸出標注結果
    print("導出標注結果...")
    try:
        tagged_result = output_pred(obser_val, pred_path)
        write2file(tagged_result, "tagged", outpath)
        print("導出成功")
    except:
        print ('導出失敗')
        sys.exit(0)

    print("========== "+file_type+"集標注完成 ==========")
    print()


if __name__ == '__main__':
    pass
    # start_tagging()
    # tag_and_write2file('dataset/original/test_cws1.txt', 'test', sepnum=50, outputpath="./result_file/new", test=False)
