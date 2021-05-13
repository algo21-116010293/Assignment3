#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: minjue
"""

import pandas as pd
import datetime
import math
import matplotlib.pyplot as plt

vix_d = pd.read_csv('/path/vix_dict-pf(1).csv',index_col=False)
vix_d = vix_d[['date','vix_ls']]
index20100531 = vix_d[vix_d['date'] == '2010-05-31'].index[0]
vix_dict = vix_d.loc[index20100531:,]
vix_dict.index = range(len(vix_dict))
vix_dict['date'] = vix_dict.apply(lambda x: datetime.datetime.strptime(x['date'],'%Y-%m-%d'),axis = 1)

years = []
for j in range(12):
    years.append(str(j + 10).rjust(2, '0'))

expr = """
vix = pd.read_excel('/path/vix_fut.xlsx',sheet_name = years[%(ind)d])
vix = vix.loc[1:,]
vix%(y)s = vix.rename(columns = {'Unnamed: 0':'date'})
vix%(y)s.index = range(len(vix%(y)s))

"""

for i in range(len(years)):
    y = str(i+10)
    exec(expr %{'ind':i,'y':y,'y':y,'y':y})

start_value = 1
wgt1 = 0.05
wgt2 = 0.95
        
output_df = pd.DataFrame(columns = ['date','w1','fut1','price1','rr1',
                                    'w2','fut2','price2','rr2','value'])
output_df['date'] = vix_dict['date']
    
def findYear(fut):    # UXM10 Index
    y_str = fut.split(' ')[0][3:]
    if len(y_str) == 2:
        y = y_str
    else:
        y = '2'+y_str
    return y         # 10,11,...,21
'''
根据日期选择交易的期权(近期和远期)
'''
exp = pd.read_excel('/path/exp_date.xlsx')
exp_day = exp[['Type','NoticeDay']]
exp_day['NoticeDay'] = exp_day.apply(lambda x: datetime.datetime.strptime(x['NoticeDay'],'%Y-%m-%d'),axis = 1)
exp_day['Type'] = exp_day.apply(lambda x: x['Type'].split(' ')[0]+' Index', axis = 1)
month_dict = {'1':'F','2':'G','3':'H','4':'J','5':'K','6':'M',
              '7':'N','8':'Q','9':'U','10':'V','11':'X','12':'Z'}

def findFut(day):
    y = day.year
    m = day.month
    y_str = str(y)[2:]  # 10,11,...,19,20,21
    if y_str[0] == '1':
        year = y_str
    else:
        if y_str[1] == '0':
            if m<= 4:
                year = y_str
            else:
                year = y_str[1]
        else:
            year = y_str[1]
    name = 'UX'+month_dict[str(m)]+year+' Index'
    return name

def checkEnddayPrice(fut,day):
    y_str = findYear(fut)
    lc = locals()
    exec("price = vix%s[vix%s['date'] == day][fut].values[0]"%(y_str,y_str))
    price = lc['price']
    if math.isnan(price):
        print(fut,day)
        return True
    else:
        return False

fut_list = exp_day['Type'].tolist()
for i in range(1,len(output_df)):
    #i = j+1
    d = output_df['date'][i]
    spot_fut = findFut(d)
    exp_index = exp_day[exp_day['Type'] == spot_fut].index[0]
    exp_date = exp_day['NoticeDay'][exp_index]
    fut_i = fut_list.index(spot_fut)
    
    if d < exp_date:
        output_df['fut1'][i] = spot_fut
        output_df['fut2'][i] = fut_list[fut_i+1]
    else:
        output_df['fut1'][i] = fut_list[fut_i+1]
        output_df['fut2'][i] = fut_list[fut_i+2]


# 到期日无价格，换仓日期提前一天
change_fut_index = []
for i in range(len(output_df)-1):
    if output_df['fut1'][i] != output_df['fut1'][i+1]:
        change_fut_index.append(i+1)        

for i in change_fut_index[1:]:
    day = output_df['date'][i]
    original_fut1 = output_df['fut1'][i-1]
    original_fut2 = output_df['fut2'][i-1]
    fut1 = output_df['fut1'][i]
    fut2 = output_df['fut2'][i]
    if checkEnddayPrice(original_fut1,day) or checkEnddayPrice(original_fut2,day):
        output_df['fut1'][i-1] = fut1
        output_df['fut2'][i-1] = fut2

'''
找对应的price
'''
for i in range(1,len(output_df)):
    t = output_df['date'][i]
    
    f1 = output_df['fut1'][i]
    y_str1 = findYear(f1)
    exec("output_df['price1'][i] = vix%s[vix%s['date'] == t][f1].values[0]" %(y_str1,y_str1))
    
    f2 = output_df['fut2'][i]
    y_str2 = findYear(f2)
    exec("output_df['price2'][i] = vix%s[vix%s['date'] == t][f2].values[0]" %(y_str2,y_str2))
    
mask = output_df[['price1','price2']].isnull().any(axis = 1)
output_df = output_df[~mask]
output_df.index = range(len(output_df))


output_df['rr1'] = (output_df['price1']-output_df['price1'].shift())/output_df['price1'].shift()
output_df['rr2'] = (output_df['price2']-output_df['price2'].shift())/output_df['price2'].shift()


'''
根据信号调仓
'''
vix_dict = vix_dict[~mask]
vix_dict.index = range(len(vix_dict))
n = len(vix_dict)
change_index = [0]
change_date = [vix_dict['date'][0]]
for i in range(2,len(vix_dict)):
    if vix_dict['vix_ls'][i-1]!= vix_dict['vix_ls'][i-2]:
        change_index.append(i)
        change_date.append(vix_dict['date'][i])
change_index.append(n-1)
change_date.append(vix_dict['date'][n-1])

'''
换标的日的return rate要重新算
'''
change_fut_index = []
for i in range(len(output_df)-1):
    if output_df['fut1'][i] != output_df['fut1'][i+1]:
        change_fut_index.append(i+1)

def changeFutRR(index):
    change_day = output_df['date'][index]
    lc=locals()
    
    last_fut1 = output_df['fut1'][index-1]
    y_str1 = findYear(last_fut1)
    exec("trade_price1 = vix%s[vix%s['date'] == change_day][last_fut1].values[0]"%(y_str1,y_str1))
    trade_price1 = lc['trade_price1']
    output_df['rr1'][index] = (trade_price1-output_df['price1'][index-1])/output_df['price1'][index-1]
    
    last_fut2 = output_df['fut2'][index-1]
    y_str2 = findYear(last_fut2)
    exec("trade_price2 = vix%s[vix%s['date'] == change_day][last_fut2].values[0]"%(y_str2,y_str2))
    trade_price2 = lc['trade_price2']
    output_df['rr2'][index] = (trade_price2-output_df['price2'][index-1])/output_df['price2'][index-1]
    

for i in change_fut_index:
    changeFutRR(i)
    

output_df['w1'][0] = start_value*wgt1
output_df['w2'][0] = start_value*wgt2


op_copy = output_df.copy()


def calWeight(start_index,end_index):
    if start_index == 0:
        check_index = 0
    else: 
        check_index = start_index-1
    for i in range(start_index+1,end_index):
        if vix_dict['vix_ls'][check_index] == 1:
            op_copy['w1'][i] = op_copy['w1'][i-1]*(1+op_copy['rr1'][i])
            op_copy['w2'][i] = op_copy['w2'][i-1]*(1+op_copy['rr2'][i])
            op_copy['value'][i] = op_copy['w1'][i]+op_copy['w2'][i]
        else:
            op_copy['w1'][i] = op_copy['w1'][i-1]*(1-op_copy['rr1'][i])
            op_copy['w2'][i] = op_copy['w2'][i-1]*(1-op_copy['rr2'][i])
            op_copy['value'][i] = op_copy['w1'][i]+op_copy['w2'][i]

for j in range(len(change_index)-1):
    start_i = change_index[j]
    end_i = change_index[j+1]
    calWeight(start_i, end_i)
    op_copy['w1'][end_i] = op_copy['value'][end_i-1]*wgt1
    op_copy['w2'][end_i] = op_copy['value'][end_i-1]*wgt2
    op_copy['value'][end_i] = op_copy['w1'][end_i]+op_copy['w2'][end_i]


plt.plot(op_copy['value'])
plt.show()
