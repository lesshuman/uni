#!/usr/bin/env python
# coding: utf-8
'''
Вариант 11
Протарифицировать абонента с IP-адресом 17.248.150.51 с коэффициентом k: 0,5руб/Мб*
* Фактически, 0.5руб/Кбит, т.к. общий трафик абонента меньше 1Мб
** Расчеты выполнены, исходя из предположения, что Мб в задании означают единицы измерения мегабит.
'''
import pandas as pd
df = pd.read_csv("dump.csv",low_memory=False)
#ibyt ~ bytes field
#sa - source addr
#da - dest addr
l = len(df.index)
coef = 0.008 # bytes to kilobits
S = 0
k = 0.5
for i in range(0,l):
    if df["sa"][i] == "17.248.150.51" or df["da"][i] == "17.248.150.51" :
        S += df["ibyt"][i]
final=k*S*coef
print("Итоговый счет: {} рублей".format(final))



