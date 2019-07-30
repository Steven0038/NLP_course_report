#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 22:46:25 2019

@author: willc
"""
import json
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def load_file(dirname, filename):
    with open('./'+ dirname +'/'+ filename +'.json', encoding='utf-8-sig') as f:
        return json.load(f)


def accuracy(predict, target):
    count = 0
    for n in range(len(predict)):
        if predict[n] == target[n]: 
            count += 1
    print('準確率: {:.2f}%'.format(100*(count/len(predict))))
 
 
def confusion_matrix_plot_matplotlib(y_truth, y_predict, filename, cmap=plt.cm.Blues):
    """
    Matplotlib 繪製混淆矩陣
    parameters
    ----------
    y_truth: 真实的y的值, 1d array
    y_predict: 预测的y的值, 1d array
    cmap: 画混淆矩阵图的配色风格, 使用cm.Blues
    """
    cm = confusion_matrix(y_truth, y_predict)
    plt.matshow(cm, cmap=cmap)  # 混淆矩阵图
    plt.colorbar()  # 颜色标签
 
    for x in range(len(cm)):  # 数据标签
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(y, x), horizontalalignment='center', verticalalignment='center', fontsize=4)
 
    plt.ylabel('target')  # 坐标轴标签
    plt.xlabel('predict')  # 坐标轴标签
    plt.savefig('confusion_matrix_'+ filename, type='png', dpi=300)
    plt.show()  # 显示作图结果

def evaluate(filepath, test=False):

    file_type = "測試" if test else "驗證"

    print("========== " + file_type + "集模型結果評估 ==========")

    pred = load_file(filepath, 'tagged')
    pred = [i[1] for i in pred]
    target = load_file(filepath, 'target')
    target = [i[1] for i in target]

    
    accuracy(pred, target)
    score = classification_report(target, pred)
    print(score)
    
    confusion_matrix_plot_matplotlib(target, pred, file_type)

    print("========== " + file_type + "集模型結果評估完成 ==========")
    print()


        
