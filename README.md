# Trading Strategy of VIX Future
This repo focuses the trading strategy of futures of VIX Index.

## Content
* Introduction to VIX Index and its futures
* Strategy
* Data
* Backtest
* Result
* Improvement
* Further Analysis
* Reference

## Introduction to VIX Index and its futures
The Cboe Volatility Index (VIX) is a real-time index that represents the market's expectations for volatility over the coming 30 days. Since it is related to volatility, it can reflect the market sentiment especially the fear of the market participants.

The futures of VIX start in each month and have a maturity of nearly a month.

## Strategy
First, we assign a signal to the VIX. That is, if the VIX is larger than the avarage of past 60 days' VIX plus 10, which means we assign it a `buy` signal, which means we long the near-term future while shorting the next-term future; otherwise, assign it a `sell` signal, which means short the near-term future while long the next-term future.

Then, we trade the futures according to the signals, keeping that strategy until the signal changes. Also, the near-term and next-term future contracts need to be changed if the near-term futures are expired. 

At each adjustment day, the weights in both future contracts are 0.50. The initial wealth is 1.0.

>For example, the signal between 2010.6.10 to 2010.6.21 is `buy`, from 2010.6.22 to 2010.6.30 is `sell`, we buy the contract of 2010.06 and short contract of >2010.07 from 2010.6.10 to 2010.6.21; from 2010.6.22, we change the strategy to short the contract of 2010.06 and long contract of 2010.07. However, the contract of >2010.06 expires on 2010.6.25, then the strategy change to short the contract of 2010.07 and long contract of 2010.08.

## Data
The VIX Index data([VIX Index](https://github.com/algo21-116010293/Assignment3/blob/main/data/vix_index.xlsx)) is downloaded from Wind and the VIX Future data is downloaded from Bloomberg, including its price([VIX FUT](https://github.com/algo21-116010293/Assignment3/blob/main/data/vix_fut.xlsx)) and expiration date([FUT Exp date](https://github.com/algo21-116010293/Assignment3/blob/main/data/exp_date.xlsx)).

## Backtest
The time interval of back testing is from 2010-06-01 to 2021-04-09.

Here, we use the return from `mark to market` to be the indicator.

As a result, we get a table like 
*Plot: The Result table of Back Testing*  
![back testing result]()

To visulize,
*Plot: The daily Return of Back Testing witg*  
![daily return]()

From the result, we can see that thaerthere is a sudden drop at the end of Feb 2018, which leads the return to be negative. In real time, we will receive a margin call. Therefore, this strategy is not proper and we need to modify it so that at least the return will not be negative. 
