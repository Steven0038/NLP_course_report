#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: willc
"""

from dataset import train, split2combine
from model import start_tagging
from evaluate import evaluate

if __name__ == "__main__":

    # 訓練、生成模型參數
    train('./dataset/original/train_cws.txt', 'model')

    # 將分詞後的文件還原成原文件
    # 驗證集
    split2combine('./dataset/original/val_cws.txt', 'val_uncut', './dataset/uncut', test=False)
    # 測試集
    split2combine('./dataset/original/test_cws1.txt', 'test_uncut', './dataset/uncut', test=True)

    # 以隱馬爾可夫 + 維特比算法進行標註
    # 驗證集
    start_tagging('./dataset/uncut/val_uncut.txt', 'tagged', 'result_file/validation', sepnum=50, test=False)
    # 測試集
    start_tagging('./dataset/uncut/test_uncut.txt', 'tagged', 'result_file/test', sepnum=50, test=True)

    # 模型評估
    # 驗證集
    evaluate('./result_file/validation/tagged.txt', './dataset/original/val_cws.txt', test=False)
    # 測試集
    evaluate('./result_file/test/tagged.txt', './dataset/original/test_cws1.txt', test=True)