#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: minjue
"""

import pandas as pd
import matplotlib.pyplot as plt

vix_d = pd.read_csv('/path/vix_dict-pf(1).csv',index_col=False)
vix_d = vix_d[['date','vix_ls']]
index20100531 = vix_d[vix_d['date'] == '2010-05-31'].index[0]
vix_dict = vix_d.loc[index20100531:,]
vix_dict.index = range(len(vix_dict))
vix_dict['date'] = vix_dict.apply(lambda x: datetime.datetime.strptime(x['date'],'%Y-%m-%d'),axis = 1)

long_index = [0,1]
for i in range(2,len(vix_dict)):
    if vix_dict['vix_ls'][i] == 0:
        if vix_dict['vix_ls'][i-2] == 1:
            long_index.append(i)
    else:
        if vix_dict['vix_ls'][i-1] == 1:
            long_index.append(i)
long_days = vix_dict['date'][long_index]

change_day_index = []
for i in range(1,len(long_index)):
    if long_index[i-1] != long_index[i]-1:
        change_day_index.append(long_index[i])



short_index = [i for i in range(len(vix_dict)) if i not in long_index]
short_days = vix_dict['date'][short_index]

long_copy = output_df.copy()


for i in range(len(long_copy)):
    if long_copy['date'][i] in list(short_days):
        long_copy['rr1'][i] = 0
        long_copy['rr2'][i] = 0

    
def calLongWgt(start_index,end_index):
    for i in range(start_index+1,end_index+1):
        long_copy['w1'][i] = long_copy['w1'][i-1]*(1+long_copy['rr1'][i])
        long_copy['w2'][i] = long_copy['w2'][i-1]*(1+long_copy['rr2'][i])
        long_copy['value'][i] = long_copy['w1'][i] + long_copy['w2'][i]

for i in range(0,len(change_index)-1,2):
    start_i = change_index[i]   # change_index[0,2,4,6,...22] = 0,201,299,...,2685
    end_i = change_index[i+1]   # change_index[1,3,5,7,...23] = 13,207,345,...,2690
    calLongWgt(start_i, end_i)
    next_open_index = change_index[i+2]
    for j in range(end_i+1,next_open_index):
        long_copy['w1'][j] = long_copy['w1'][end_i]
        long_copy['w2'][j] = long_copy['w2'][end_i]
        long_copy['value'][j] = long_copy['w1'][j]+long_copy['w2'][j]
    long_copy['w1'][next_open_index] = long_copy['value'][end_i]*wgt1
    long_copy['w2'][next_open_index] = long_copy['value'][end_i]*wgt2
    long_copy['value'][next_open_index] = long_copy['w1'][next_open_index]+long_copy['w2'][next_open_index]
    
plt.plot(long_copy['value'])
plt.show()    
