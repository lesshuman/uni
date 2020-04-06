#!/usr/bin/env python
# coding: utf-8

# In[53]:


'''
Вариант 11:
Протарифицировать  абонента  с  номером  911926375  с  коэффициентом  k: 1руб/минута исходящие звонки, 1руб/минута входящие, смс -первые 5шт бесплатно, далее 1руб/шт
X = T * k
X–итоговая стоимость всех звонков абонента,
T–общая длительность звонков (сумма длительностей всех записей по абоненту),
k–множитель тарифного плана
Y = N * k
Y–итоговая стоимость всех СМС абонента,
N–общее количество СМС (сумма числа всех СМС в записях по абоненту в файле),
k–множитель тарифного плана

timestamp -время звонка
sms_number -количество отправленных смс для абонента msisdn_origin
'''
import pandas as pd
from math import ceil

df = pd.read_csv("data.csv")
S = 0
k = {"in":1,"out":1,"sms":{"free":5,"rate":1}}
l = len(df.index)
for i in range(0,l):
    if df["msisdn_origin"][i] == 911926375:
        S+=ceil(df["call_duration"][i])*k["out"]
        S+=(df["sms_number"][i] - k["sms"]["free"])*k["sms"]["rate"]
    if df["msisdn_dest"][i] == 911926375:
        S+=ceil(df["call_duration"][i])*k["in"]
print("Итоговый счет: {} рублей".format(S))
    


# In[ ]:




