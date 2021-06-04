#!/usr/bin/env python
# coding: utf-8

'''График зависимости трафика от времени (точечный график)'''
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime
import matplotlib.patches as patches

large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'xtick.labelsize': small,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
coef = 0.008
df = pd.read_csv("dump.csv",low_memory=False)
x = [datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S") for s in df["ts"][:17449]]
y = [b*coef for b in df["ibyt"][:17449]]
datenums=md.date2num(x)

plt.figure(figsize=(16, 10), dpi= 80, facecolor='w', edgecolor='k')
plt.xticks( rotation=14)
ax = plt.gca()
ax.set(xlabel='Time', ylabel='Traffic(in Kb)')
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
ax.xaxis.set_major_locator(md.MinuteLocator(interval=10)) 
plt.scatter(datenums,y,s=20,c='tab:green',label='Kb of traffic')
plt.title("Traffic over time", fontsize=22)
plt.legend(fontsize=12)    
#plt.show()
plt.savefig("stats.pdf",bbox_inches='tight')

