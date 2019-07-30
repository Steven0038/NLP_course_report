#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 12:03:25 2019

@author: willc
"""

import warnings
from helper.pre_proccess import data_preproccessing
from dataset import model_param_proccessing
from model import start_tagging, tag_and_write2file
from evaluate import evaluate
from ner_evaluate import ner_evaluate


if __name__ == "__main__":
    # 數據預處理, 使用 B M E 三層標註
    data_preproccessing(tag_level='three')

    # 生成、輸出參數模型
    model_param_proccessing()

    # 以隱馬爾可夫 + 維特比算法進行標註
    # 驗證集
    start_tagging('./dataset/original/val_cws.txt', './result_file/validation', test=False, sepnum=40)
    # 測試集
    start_tagging('./dataset/original/test_cws1.txt', './result_file/test', test=True, sepnum=80)

    # 標註並輸出成文件
    # 驗證集
    tag_and_write2file('dataset/original/val_cws.txt', 'tagged', sepnum=40, outputpath="./result_file/validation", test=False)
    # 測試集
    tag_and_write2file('dataset/original/test_cws1.txt', 'tagged', sepnum=80, outputpath="./result_file/test", test=True)

    # 結果評估
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # 驗證集
        evaluate('./result_file/validation', test=False)
        # 測試集
        evaluate('./result_file/test', test=True)

    # 助教的模型評估
    # 驗證集
    ner_evaluate('dataset/original/val_ner.txt', './result_file/validation/tagged.txt', test=False)
    # 測試集
    ner_evaluate('dataset/original/test_ner1.txt', './result_file/test/tagged.txt', test=True)



