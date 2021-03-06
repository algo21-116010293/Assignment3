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
![back testing result](https://github.com/algo21-116010293/Assignment3/blob/main/result/result_tab.png)

To visulize,
*Plot: The daily Return of Back Testing with weight 0.5&0.5*  
![daily return](https://github.com/algo21-116010293/Assignment3/blob/main/result/w0.5.png)

From the result, we can see that there is a period that the portfolio reaches high return at more than 15 times than the initial wealth. However, there is a sudden drop at the end of Feb 2018, which leads the return to be negative. In real time, we will receive a margin call. Therefore, this strategy is not proper and we need to modify it so that at least the return will not be negative. 

## Improvement
### 1. Change the Weight of Contracts 
Since the future contracts of near-term bear more risk, we put less weight on it, say 0.05 on near-term contract, 0.95 on next-term contract. We get the result as below, 

*Plot: The daily Return of Back Testing with Weight 0.05&0.95*  
![daily return with weight 0.05](https://github.com/algo21-116010293/Assignment3/blob/main/result/w0.05.png)

It shows that at the end of Feb 2018, the great loss still exist but will not lead the account to be negative. 

### 2. Long Only
Since the loss mainly comes from short contracts, we try to long only. The result is

*Plot: The daily Return of Back Testing by Longing Only*  
![daily return by longing](https://github.com/algo21-116010293/Assignment3/blob/main/result/long.png)

The result shows that the loss at the same time is very little. However, the return of this strategy is also limited, the largest of which is only 1.4 times than the initial.

## Further Analysis
From the above, we guess that if we want to obtain high profit, the sharp loss may be not avoidable, which means we need to try to smooth it instead of getting rid of it. Further analysis can focus on the method of producing signal. 

## Reference
The idea of this repo is from a blog [Trading of Derivatives on VIX Index](http://blog.sina.com.cn/s/blog_8ffb0d960102wxlw.html), especially the part of Spread Strategy. However, this repo adds more on that. 


