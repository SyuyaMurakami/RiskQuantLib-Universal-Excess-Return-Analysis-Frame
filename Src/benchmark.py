#!/usr/bin/python
# coding = utf-8

import numpy as np
import pandas as pd

#->benchmark@import
from RiskQuantLib.InstrumentList.SubPortfolioList.subPortfolioList import subPortfolioList, subPortfolio
from RiskQuantLib.InstrumentList.SecurityList.StockList.stockList import stockList

#->benchmark
def initHold(self):
    self.subPortfolio = subPortfolioList()
    self.holdings = stockList()
    self.weight = 0.0
    self.rtn = 0.0
    return self

def addHolding(self, element):
    self.holdings.setAll(self.holdings.all + [element])

def addHoldingSeries(self, elementList):
    if hasattr(elementList,'all') and type(getattr(elementList,'all',np.nan))==type([]):
        self.holdings.setAll(self.holdings.all + elementList.all)
    else:
        self.holdings.setAll(self.holdings.all + elementList)

# classify benchmark holdings to sub-portfolio
def addSubPortfolioByAttrForEveryBenchmark(self, attrName: str):
    tmpList = self.holdings.groupBy(attrName=attrName, inplace=True)
    tmpSubPortfolioList = subPortfolioList()
    tmpSubPortfolioList.addSubPortfolioSeries(tmpList[attrName], tmpList[attrName])
    [subPortfolioIT.addHoldingSeries(holdings.all) for subPortfolioIT, holdings in zip(tmpSubPortfolioList, tmpList)]
    tmpSubPortfolioList.sort(['code'],inplace=True)
    self.subPortfolio.setAll(self.subPortfolio.all + tmpSubPortfolioList.all)

def addSubPortfolio(self, subPT: subPortfolio):
    self.subPortfolio.setAll(self.subPortfolio.all + [subPT])

def addSubPortfolioSeries(self, subPortfolioListObj):
    if hasattr(subPortfolioListObj,'all') and type(getattr(subPortfolioListObj,'all',np.nan))==type([]):
        self.subPortfolio.setAll(self.subPortfolio.all + subPortfolioListObj.all)
    else:
        self.subPortfolio.setAll(self.subPortfolio.all + subPortfolioListObj)

def calRTN(self):
    self.subPortfolio.execFunc('calRTN')
    self.weight = self.holdings.sum('weight')
    self.rtn = np.nansum([w*r for w,r in zip(self.holdings['weight'],self.holdings['rtn'])])/self.weight if (not np.isnan(self.weight)) and self.weight!=0.0 else np.nanmean(self.holdings['rtn'])

#->benchmarkList
def addBenchmarkFromHolding(self, holdingList):
    if hasattr(holdingList,'all') and type(getattr(holdingList,'all',np.nan))==type([]):
        tmpObj = holdingList.groupBy('belongTo')
    else:
        tmpObj = self.new()
        tmpObj.setAll(holdingList)
        tmpObj = tmpObj.groupBy('belongTo')
    securitySeries = [self.elementClass(i, i).initHold() for i in tmpObj['belongTo']]
    [port.addHoldingSeries(holding) for port, holding in zip(securitySeries, tmpObj)]
    self.setAll(self.all + securitySeries)

def addSubPortfolioByAttr(self,attrName : str):
    self.execFunc('addSubPortfolioByAttrForEveryBenchmark',attrName)
