#!/usr/bin/python
# coding = utf-8
import os
import smtpd
import sys

import numpy as np
import pandas as pd

from RiskQuantLib.module import *
path = sys.path[0]

# 多期brinson归因

# 读取业绩基准持仓源文件，并将其转换为对象化的列表
df_benchmark_holding = pd.read_excel(path+os.sep+'Data'+os.sep+'benchmark.xlsx')
benchmark_holding = stockList().fromDF(df_benchmark_holding)

# 初始化一个业绩基准时间序列分析对象，传入业绩基准的持仓，选择分析维度为行业
benchmark_list = benchmarkTimeSeries()
benchmark_list.addBenchmarkFromHolding(benchmark_holding)
benchmark_list.addSubPortfolioByAttr('industry')# 这里选择分析维度为行业，理论上可以选择任何属性，但如果是Brinson归因，则必须选择行业

# 读取投资组合持仓数据，转换为对象化列表
df_fund_holding = pd.read_excel(path+os.sep+'Data'+os.sep+'holding.xlsx')
df_fund_to_benchmark = pd.read_excel(path+os.sep+'Data'+os.sep+'portfolio_to_benchmark.xlsx')
fund_holding = stockList().fromDF(df_fund_holding)

# 初始化一个投资组合时间序列分析对象，传入投资组合的持仓，设置投资组合的基准，选择分析维度同业绩基准相同
fund_list = portfolioTimeSeries()
fund_list.addPortfolioFromHolding(fund_holding)
fund_list.setBenchmark(df_fund_to_benchmark['fund'],df_fund_to_benchmark['index'],benchmark_list)
fund_list.addSubPortfolioByBenchmark('industry')

# 多期行业归因
fund_list.calSubPortfolioBreakDown(['金融','冶金','机械制造','能源','电子'])# 选择你要归因到的行业类型，这些行业必须是源文件中industry列出现过的

# 输出结果
result = pd.DataFrame(fund_list.portfolio['excessAccuRtnBreakDown'],index = fund_list.portfolio['code'])
result['accuRtn'] = fund_list.portfolio['accuRtn']
result['benchmarkAccuRtn'] = fund_list.portfolio['benchmarkAccuRtn']
result['excessAccuRtn'] = fund_list.portfolio['excessAccuRtn']
result[['accuRtn','benchmarkAccuRtn','excessAccuRtn']+result.columns.to_list()[:-3]].to_excel(path+os.sep+'Result'+os.sep+'行业归因.xlsx')

print("Finished")