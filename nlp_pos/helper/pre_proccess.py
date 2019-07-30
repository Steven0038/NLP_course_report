#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 16:50:30 2019

@author: willc
"""

import json, os, sys

def write2file(output, filename, dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(dirname +'/'+ filename +'.json', 'w', encoding='utf-8-sig') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def proccess_data(filename):
    output = []
    with open(filename, 'r', encoding='utf-8-sig') as fr:
        for line in fr:
            line = line.rstrip().split(' ')
            for l in line:
                output.append(l.rsplit('/', 1))
    return output


def handle_no_tag_word(tagged_result):
    for tag_word in tagged_result:
        if len(tag_word) == 1:
            tag_word.append("")


def test_target_pre_proccess():
    proccess_test_data = proccess_data('./dataset/original/test_pos1.txt')
    handle_no_tag_word(proccess_test_data)
    write2file(proccess_test_data, 'target', './result_file/test')

def validation_target_pre_proccess():
    proccess_valid_data = proccess_data('./dataset/original/val_pos.txt')
    handle_no_tag_word(proccess_valid_data)
    write2file(proccess_valid_data, 'target', './result_file/validation')

def data_preproccessing():
    print("==========  數據預處理 ==========")
    print("轉換訓練集格式...")
    try:
        test_target_pre_proccess()
        print("轉換訓練集格式完成...")
    except Exception as e:
        print("轉換訓練集格式失敗, 原因： ", e)
        sys.exit(0)

    print("轉換驗證集格式...")
    try:
        validation_target_pre_proccess()
        print("轉換驗證集格式完成...")
    except Exception as e:
        print("轉換訓練集格式失敗, 原因： ", e)
        sys.exit(0)
    print("==========  數據預處理完成 ==========")
    print()
if __name__ == "__main__":
    data_preproccessing()