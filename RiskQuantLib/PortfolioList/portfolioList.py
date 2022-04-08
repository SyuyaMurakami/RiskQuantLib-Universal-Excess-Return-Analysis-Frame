#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Portfolio.portfolio import portfolio
from RiskQuantLib.Operation.listBaseOperation import listBase
from RiskQuantLib.Set.PortfolioList.portfolioList import setPortfolioList
class portfolioList(listBase,setPortfolioList):

    elementClass = portfolio

    def __init__(self):
        self.all = []
        self.listType = 'Portfolio List'

    def addPortfolio(self, securityCode,securityName,securityTypeString = "Portfolio"):
        securitySeries = self.all+[portfolio(securityCode,securityName,securityTypeString)]
        self.setAll(securitySeries)

    def addPortfolioSeries(self, securityCodeSeries,securityNameSeries,securityTypeString = "Portfolio"):
        securitySeries = [portfolio(i,j,securityTypeString) for i,j in zip(securityCodeSeries,securityNameSeries)]
        self.setAll(self.all + securitySeries)

    def addPortfolioFromHolding(self, holdingList):
        if hasattr(holdingList,'all') and type(getattr(holdingList,'all',np.nan))==type([]):
            tmpObj = holdingList.groupBy('belongTo')
        else:
            tmpObj = self.new()
            tmpObj.setAll(holdingList)
            tmpObj = tmpObj.groupBy('belongTo')
        securitySeries = [portfolio(i, i) for i in tmpObj['belongTo']]
        [port.addHoldingSeries(holding) for port,holding in zip(securitySeries,tmpObj)]
        self.setAll(self.all + securitySeries)

    def addSubPortfolioByBenchmark(self, linkedAttrName = ''):
        self.execFunc('addSubPortfolioByBenchmark',linkedAttrName)

    def calBrinsonBreakDown(self):
        self.execFunc('calBrinsonBreakDown')

    def calSubPortfolioBreakDown(self,subPortfolioCodeList):
        self.execFunc('calSubPortfolioBreakDown',subPortfolioCodeList)

    def calBreakDown(self, attrName, targetFunctionName):
        self.execFunc('calBreakDown', attrName, targetFunctionName)