#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 00:00:30 2019

@author: willc
"""
ner = []
stack = []

from model import write2file
from dataset import read_from_train
import os, sys

def train_handle(inputfile, outputfile, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(inputfile,'r', encoding='utf-8-sig') as inp, open('./'+output_path+'/'+outputfile+'.txt','w', encoding='utf-8-sig') as outp:
        for string in inp.readlines():
            i=0
            substring = ""
            tag = ""
            temp = []
            res = []
            stack = []
            
            while i<len(string):
                #print(string[i])
                #print("i: ",i," stack: ",stack)
                
                
                if string[i] != '[' and string[i] != ']' and string[i] != ' ':
                    substring = substring + string[i]
                    if i==(len(string)-1):
                        if substring != '':
                            stack.append(substring)
                            while len(stack)>0:
                                temp.append(stack.pop()+'/0')
                            res.append(temp[::-1])
                            temp=[]
                
                elif string[i] == ' ':
                    if substring != "":
                        stack.append(substring)
                        substring = ""
                
                elif string[i] == '[':
                    
                    a = '[' in stack
                    
                    if (a) or len(stack) == 0 :
                        stack.append('[')
                        
                    elif len(stack)>0:
                        while len(stack)>0:
                            temp.append(stack.pop()+'/0')
                            
                        res.append(temp[::-1])
                        
                        temp=[]
                        stack.append('[')
                        #print(stack)
                    
                    #print(stack)
                        
                elif string[i] == ']':
                    if substring != "":
                        stack.append(substring)
                        substring = ""
                    if string[i+1] == 'n':
                        tag = string[i+1]+string[i+2]
                        i+=2
                    else:
                        tag = string[i+1]+string[i+2]+string[i+3]
                        i+=3
                    while len(stack)>0:
                        pop = stack.pop()
                        
                        if pop != '[':
                            temp.append(pop+"/"+tag)
                            #print(temp)
            
                        else:
            
                            a = ('[' in stack)
                            if (a):
                                for q in temp[::-1]:
                                    stack.append(q)
                                temp=[]
            
                                
                            break
                    if len(temp) != 0:# and len(inline)==0:
                        res.append(temp[::-1])
                        #print(temp)
                    temp=[]
                    tag=""
                
             
                    
                        
                
                i+=1
            
            for sent in res:
                for word in sent:
                    outp.write(word+' ')
            outp.write("\n")

def delete_line(inputfile, outputfile, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(inputfile,'r', encoding='utf-8-sig') as inp, open('./'+output_path+'/'+outputfile+'.txt','w', encoding='utf-8-sig') as outp:
        for string in inp.readlines():
            string = string.rstrip()
            ls_split = string.split(' ')[-1].split('/')
            if string == '/0':
                pass
            
            else:
                if len(ls_split) == 1:
                    string = string+'/0'
                outp.write(string+'\n')

def handle_taging_ner(inputfile, outputfile, output_path, tag_level):
    MIDDLE = 'M' if tag_level == 'three' else 'E'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(inputfile,'r', encoding='utf-8-sig') as inp, open('./'+output_path+'/'+outputfile+'.txt','w', encoding='utf-8-sig') as outp:
        for string in inp.readlines():
            tag=""
            string = string.rstrip()
            line = string.split(' ')
            i = 0
            while i<len(line):
                if line[i]=='':
                    i+=1
                    continue
                word = line[i].split('/')[0]
                tag = line[i].split('/')[-1]
                if tag=='tes' or tag=='tre' or tag=='sym' or tag=='dis' or tag=="nt" or tag=='nr':

                    if i == len(line) - 1:
                        if line[i-1].split('/')[-1] != line[i].split('/')[-1]:
                            outp.write(word + "/B_" + tag + " ")
                        else:
                            outp.write(word + "/E_" + tag + " ")
                    elif line[i-1].split('/')[-1] != line[i].split('/')[-1]:
                        if len(line[i].split('/')) == 3:
                            outp.write(word+"/"+line[i].split('/')[1]+"/B_"+tag+" ")
                        else:
                            outp.write(word+"/B_"+tag+" ")
                    elif line[i-1].split('/')[-1] == line[i].split('/')[-1] and line[i].split('/')[-1] != line[i+1].split('/')[-1]:
                        if len(line[i].split('/')) == 3:
                            outp.write(word+"/"+line[i].split('/')[1]+"/E_"+tag+" ")
                        else:
                            outp.write(word+"/E_"+tag+" ")
                    elif line[i-1].split('/')[-1] == line[i].split('/')[-1]:
                        if len(line[i].split('/')) == 3:
                            outp.write(word+"/"+line[i].split('/')[1]+"/"+MIDDLE+"_"+tag+" ")
                        else:
                            outp.write(word+"/"+MIDDLE+"_"+tag+" ")

                    
                else:
                    outp.write(line[i]+' ')
                i+=1
            outp.write('\n')

def handle_taging_bod(inputfile, outputfile, output_path, tag_level):
    MIDDLE = 'M' if tag_level == 'three' else 'E'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(inputfile,'r', encoding='utf-8-sig') as inp, open('./'+output_path+'/'+outputfile+'.txt','w', encoding='utf-8-sig') as outp:
        for string in inp.readlines():
            string = string.rstrip()
            line = string.split(' ')
            i = 0
            while i < len(line):
                if line[i]=='':
                    i+=1
                    continue
                word = line[i].split('/')[0]
                #print(line[i])
                tag = line[i].split('/')[1]
                if tag=='bod':
                    if i==0:
                        outp.write(word+"/B_"+tag+" ")
                    elif i == len(line) - 1:
                        if line[i-1].split('/')[-1] != line[i].split('/')[-1]:
                            outp.write(word + "/B_" + tag + " ")
                        else:
                            outp.write(word + "/E_" + tag + " ")
                    elif line[i-1].split('/')[1] != line[i].split('/')[1]:
                        if len(line[i].split('/')) == 3:
                            outp.write(word+"/B_"+tag+"/"+line[i].split('/')[-1]+" ")
                        else:
                            outp.write(word+"/B_"+tag+" ")
                    elif line[i-1].split('/')[1] == line[i].split('/')[1] and line[i].split('/')[1] != line[i+1].split('/')[1]:
                        if len(line[i].split('/')) == 3:
                            outp.write(word+"/E_"+tag+"/"+line[i].split('/')[-1]+" ")
                        else:
                            outp.write(word+"/E_"+tag+" ")
                    elif line[i-1].split('/')[1] == line[i].split('/')[1]:
                        if len(line[i].split('/')) == 3:
                            outp.write(word+"/"+MIDDLE+"_"+tag+"/"+line[i].split('/')[-1]+" ")
                        else:
                            outp.write(word+"/"+MIDDLE+"_"+tag+" ")
                    
                else:
                    outp.write(line[i]+' ')
                i+=1
            outp.write('\n')


def train_pre_preproccess(tag_level):
    train_handle("./dataset/original/train_ner.txt", "handle", './dataset/proccessed/train')
    delete_line("./dataset/proccessed/train/handle.txt", "handle_line", './dataset/proccessed/train')
    handle_taging_ner("./dataset/proccessed/train/handle_line.txt", "ner_tag_first", './dataset/proccessed/train', tag_level)
    handle_taging_bod("./dataset/proccessed/train/ner_tag_first.txt", "ner_tag_com", "./dataset/proccessed/train", tag_level)

def test_target_pre_preproccess(tag_level):
    train_handle("./dataset/original/test_ner1.txt", "handle", './dataset/proccessed/test')
    delete_line("./dataset/proccessed/test/handle.txt", "handle_line", './dataset/proccessed/test')
    handle_taging_ner("./dataset/proccessed/test/handle_line.txt", "ner_tag_first", './dataset/proccessed/test', tag_level)
    handle_taging_bod("./dataset/proccessed/test/ner_tag_first.txt", "ner_tag_com", "./dataset/proccessed/test", tag_level)

def validation_target_pre_preproccess(tag_level):
    train_handle("./dataset/original/val_ner.txt", "handle", './dataset/proccessed/validation')
    delete_line("./dataset/proccessed/validation/handle.txt", "handle_line", './dataset/proccessed/validation')
    handle_taging_ner("./dataset/proccessed/validation/handle_line.txt", "ner_tag_first", './dataset/proccessed/validation', tag_level)
    handle_taging_bod("./dataset/proccessed/validation/ner_tag_first.txt", "ner_tag_com", "./dataset/proccessed/validation", tag_level)


def target2list(word_list, tag_list):
    out = []
    combine = zip(word_list, tag_list)
    for word_tag in combine:
        out.append([word_tag[0], word_tag[1]])
    return out

def write2json(filepath, despath, filename):
    word_list, tag_list = read_from_train(filepath)
    target_data = target2list(word_list, tag_list)
    write2file(target_data, filename, despath)

def data_preproccessing(tag_level="three"):
    print("==========  數據預處理 ==========")
    print("轉換訓練集格式...")
    try:
        train_pre_preproccess(tag_level)
        print("轉換訓練集格式完成...")
    except Exception as e:
        print("轉換訓練集格式失敗, 原因： ", e)
        sys.exit(0)

    print("轉換驗證集格式...")
    try:
        validation_target_pre_preproccess(tag_level)
        print("轉換驗證集格式完成...")
    except Exception as e:
        print("轉換驗證集格式失敗, 原因： ", e)
        sys.exit(0)

    print("轉換測試集格式...")
    try:
        test_target_pre_preproccess(tag_level)
        print("轉換測試集格式完成...")
    except Exception as e:
        print("轉換測試集格式失敗, 原因： ", e)
        sys.exit(0)

    print("將轉換後的驗證集合測試集輸出成json...")
    try:
        write2json('./dataset/proccessed/validation/ner_tag_com.txt', './result_file/validation', 'target')
        write2json('./dataset/proccessed/test/ner_tag_com.txt', './result_file/test', 'target')
        print("轉換完成...")
    except Exception as e:
        print("轉換失敗, 原因： ", e)
        sys.exit(0)

    print("==========  數據預處理完成 ==========")
    print()
