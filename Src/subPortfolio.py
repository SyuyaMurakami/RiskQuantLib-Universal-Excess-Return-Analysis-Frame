#!/usr/bin/python
# coding = utf-8

import numpy as np
import pandas as pd

#->subPortfolio@import
from RiskQuantLib.InstrumentList.SecurityList.StockList.stockList import stockList

#->subPortfolio
def initHold(self):
    self.holdings = stockList()
    self.weight = 0.0
    self.rtn = 0.0
    return self

def addHolding(self, holdingObj):
    securitySeries = self.holdings.all+[holdingObj]
    self.holdings.setAll(securitySeries)

def addHoldingSeries(self, holdingList):
    if hasattr(holdingList, 'all') and type(getattr(holdingList,'all',np.nan))==type([]):
        securitySeries = self.holdings.all + holdingList.all
    else:
        securitySeries = self.holdings.all + holdingList
    self.holdings.setAll(securitySeries)

def calRTN(self):
    self.weight = np.nansum(self.holdings['weight'])
    self.rtn = np.nansum([w*r for w,r in zip(self.holdings['weight'],self.holdings['rtn'])])/self.weight if (not np.isnan(self.weight)) and self.weight!=0.0 else np.nanmean(self.holdings['rtn'])

#->subPortfolioList@add
def addSubPortfolio(self,codeString,nameString,instrumentTypeString = 'SubPortfolio'):
    tmpList = self.all+[self.elementClass(codeString,nameString,instrumentTypeString).initHold()]
    self.setAll(tmpList)

#->subPortfolioList@addSeries
def addSubPortfolioSeries(self,subPortfolioCodeSeries,subPortfolioNameSeries,instrumentTypeString = 'SubPortfolio'):
    subPortfolioSeries = [self.elementClass(i,j,instrumentTypeString).initHold() for i,j in zip(subPortfolioCodeSeries,subPortfolioNameSeries)]
    tmpList = self.all + subPortfolioSeries
    self.setAll(tmpList)
