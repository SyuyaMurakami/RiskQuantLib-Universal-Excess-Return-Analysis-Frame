#!/usr/bin/python
# coding = utf-8

import numpy as np
import pandas as pd

#->portfolio@import
from RiskQuantLib.InstrumentList.SubPortfolioList.subPortfolioList import subPortfolioList, subPortfolio
from RiskQuantLib.InstrumentList.SecurityList.StockList.stockList import stockList

#->portfolio
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
def addSubPortfolioByAttr(self, attrName: str):
    tmpList = self.holdings.groupBy(attrName=attrName, inplace=True)
    tmpSubPortfolioList = subPortfolioList()
    tmpSubPortfolioList.addSubPortfolioSeries(tmpList[attrName], tmpList[attrName])
    [subPortfolioIT.addHoldingSeries(holdings.all) for subPortfolioIT, holdings in zip(tmpSubPortfolioList, tmpList)]
    tmpSubPortfolioList.sort(['code'], inplace=True)
    self.subPortfolio.setAll(self.subPortfolio.all + tmpSubPortfolioList.all)

def addSubPortfolioByBenchmarkForEveryPortfolio(self, linkedAttrName = ''):
    if linkedAttrName == '':
        codeList = [i['code'] for i in self.benchmark.subPortfolio]
        tmpHoldingList = [[j for j in self.holdings.all if j.code in i] for i in codeList]
    else:
        tmpHoldingList = [[j for j in self.holdings.all if getattr(j,linkedAttrName,np.nan) == i.code] for i in self.benchmark.subPortfolio]
    tmpSubPortfolioList = subPortfolioList()
    tmpSubPortfolioList.addSubPortfolioSeries(self.benchmark.subPortfolio['code'],self.benchmark.subPortfolio['name'])
    [port.holdings.setAll(hold) for port,hold in zip(tmpSubPortfolioList,tmpHoldingList)]
    self.subPortfolio.setAll(self.subPortfolio.all + tmpSubPortfolioList.all)

def addSubPortfolio(self, subPT: subPortfolio):
    self.subPortfolio.setAll(self.subPortfolio.all + [subPT])

def addSubPortfolioSeries(self, subPortfolioListObj):
    if hasattr(subPortfolioListObj,'all') and type(getattr(subPortfolioListObj,'all',np.nan))==type([]):
        self.subPortfolio.setAll(self.subPortfolio.all + subPortfolioListObj.all)
    else:
        self.subPortfolio.setAll(self.subPortfolio.all + subPortfolioListObj)

def registerExcessRtnBreakDown(self, attrName):
    if type(attrName)==type(''):
        attrName = [attrName]
    elif type(attrName)==type([]):
        pass
    else:
        return
    if not hasattr(self,'excessRTN'):
        self.calExcessRTN()
    breakDownValue = [getattr(self,i,np.nan) for i in attrName]
    self.excessRtnBreakDown = dict(zip(attrName,breakDownValue))
    residual = self.excessRTN - np.nansum([self.excessRtnBreakDown[i] for i in self.excessRtnBreakDown.keys() if i!='residual'])
    self.excessRtnBreakDown['residual'] = residual

def calRTN(self):
    self.subPortfolio.execFunc('calRTN')
    self.weight = self.holdings.sum('weight')
    self.rtn = np.nansum([w*r for w,r in zip(self.holdings['weight'],self.holdings['rtn'])])/self.weight if (not np.isnan(self.weight)) and self.weight!=0.0 else np.nanmean(self.holdings['rtn'])

def calExcessRTN(self):
    self.benchmark.calRTN()
    self.calRTN()
    self.excessRTN = self.rtn - self.benchmark.rtn
    self.logLinkingMultiplier = (np.log(1+self.rtn) - np.log(1+self.benchmark.rtn))/(self.rtn - self.benchmark.rtn)

def calAllocationRTN(self):
    self.allocationRTN = np.nansum([(subP.weight-benchmarkP.weight)*benchmarkP.rtn for subP,benchmarkP in zip(self.subPortfolio,self.benchmark.subPortfolio)])

def calSelectionRTN(self):
    self.selectionRTN = np.nansum([(subP.rtn-benchmarkP.rtn)*benchmarkP.weight for subP,benchmarkP in zip(self.subPortfolio,self.benchmark.subPortfolio)])

def calInteractionRTN(self):
    self.interactionRTN = np.nansum([subP.weight*subP.rtn - benchmarkP.weight*subP.rtn-subP.weight*benchmarkP.rtn+benchmarkP.weight*benchmarkP.rtn for subP,benchmarkP in zip(self.subPortfolio,self.benchmark.subPortfolio)])

def calSubPortfolioExcessRTN(self,subPortfolioCodeList):
    [setattr(self,subPortfolioCode+'ExcessRTN',getattr(self.subPortfolio[subPortfolioCode],'rtn',np.nan) - getattr(self.benchmark.subPortfolio[subPortfolioCode],'rtn',np.nan)) for subPortfolioCode in subPortfolioCodeList]

def calBrinsonBreakDownForEveryPortfolio(self):
    self.calBreakDownForEveryPortfolio(['allocationRTN', 'selectionRTN', 'interactionRTN'],['calAllocationRTN','calSelectionRTN','calInteractionRTN'])

def calSubPortfolioBreakDownForEveryPortfolio(self,subPortfolioCodeList):
    self.calBreakDownForEveryPortfolio([i + 'ExcessRTN' for i in subPortfolioCodeList],['calSubPortfolioExcessRTN'],subPortfolioCodeList)

def calBreakDownForEveryPortfolio(self,attrName, targetFunctionName, *args):
    self.calExcessRTN()
    if type(targetFunctionName)==type(''):
        targetFunctionName = [targetFunctionName]
    elif type(targetFunctionName)==type([]):
        pass
    else:
        return
    [getattr(self,i,lambda *args:None)(*args) for i in targetFunctionName]
    self.registerExcessRtnBreakDown(attrName)

#->portfolioList
def addPortfolioFromHolding(self, holdingList):
    if hasattr(holdingList,'all') and type(getattr(holdingList,'all',np.nan))==type([]):
        tmpObj = holdingList.groupBy('belongTo')
    else:
        tmpObj = self.new()
        tmpObj.setAll(holdingList)
        tmpObj = tmpObj.groupBy('belongTo')
    securitySeries = [self.elementClass(i, i).initHold() for i in tmpObj['belongTo']]
    [port.addHoldingSeries(holding) for port,holding in zip(securitySeries,tmpObj)]
    self.setAll(self.all + securitySeries)

def addSubPortfolioByBenchmark(self, linkedAttrName = ''):
    self.execFunc('addSubPortfolioByBenchmarkForEveryPortfolio',linkedAttrName)

def calBrinsonBreakDown(self):
    self.execFunc('calBrinsonBreakDownForEveryPortfolio')

def calSubPortfolioBreakDown(self,subPortfolioCodeList):
    self.execFunc('calSubPortfolioBreakDownForEveryPortfolio',subPortfolioCodeList)

def calBreakDown(self, attrName, targetFunctionName):
    self.execFunc('calBreakDownForEveryPortfolio', attrName, targetFunctionName)
