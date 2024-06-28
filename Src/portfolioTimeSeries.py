#!/usr/bin/python
# coding = utf-8

import numpy as np
import pandas as pd
from RiskQuantLib.InstrumentList.PortfolioList.portfolioList import portfolioList
from RiskQuantLib.Operation.operation import operation
from RiskQuantLib.Auto.InstrumentList.PortfolioList.portfolioList import portfolioListAuto
from Src.benchmarkTimeSeries import benchmarkTimeSeries

class portfolioTimeSeries(operation,portfolioListAuto):

    elementClass = portfolioList

    def __init__(self):
        self.all = []
        self.listType = 'Portfolio Time Series'

    def addPortfolioFromHolding(self, holdingList):
        if hasattr(holdingList,'all') and type(getattr(holdingList,'all',np.nan))==type([]):
            tmpObj = holdingList.groupBy('tradingDate')
        else:
            tmpObj = self.new()
            tmpObj.setAll(holdingList)
            tmpObj = tmpObj.groupBy('tradingDate')
        securitySeries = [portfolioList() for i in tmpObj['belongTo']]
        [port.addPortfolioFromHolding(holding) for port, holding in zip(securitySeries, tmpObj)]
        [setattr(port,'tradingDate',holding.tradingDate) for port, holding in zip(securitySeries, tmpObj)]
        self.setAll(self.all + securitySeries)

    def reformToPortfolio(self):
        tmpObj = self.new()
        allPortfolio = {(port,date.tradingDate) for date in self.all for port in date}
        [i[0].setTradingDate(i[1]) for i in allPortfolio]
        tmpObj.setAll([i[0] for i in allPortfolio])
        self.portfolio = tmpObj.groupBy('code')
        self.portfolio.execFunc('sort','tradingDate',False,True)

    def linkTimeSeries(self):
        accuRtn = np.array([np.nanprod(np.array(port['rtn'])+1) for port in self.portfolio])
        benchAccuRtn = np.array([np.nanprod(np.array([j.rtn for j in port['benchmark']])+1) for port in self.portfolio])
        excessAccuRtn = accuRtn - benchAccuRtn
        accuLogLinkingMultiplier = (np.log(accuRtn)-np.log(benchAccuRtn))/excessAccuRtn
        linkedExcessRtnBreakDown = [[date.logLinkingMultiplier*np.array(list(date.excessRtnBreakDown.values())) for date in port] for port in self.portfolio]
        linkedExcessRtnBreakDown = [np.row_stack(i) for i in linkedExcessRtnBreakDown]
        excessAccuRtnBreakDown = [np.nansum(i,axis=0)/accuLogLinkingMultiplier[index] for index,i in enumerate(linkedExcessRtnBreakDown)]
        [setattr(port, 'accuRtn', accuRtn[index]-1) for index, port in enumerate(self.portfolio)]
        [setattr(port, 'benchmarkAccuRtn', benchAccuRtn[index]-1) for index, port in enumerate(self.portfolio)]
        [setattr(port,'excessAccuRtn',excessAccuRtn[index]) for index,port in enumerate(self.portfolio)]
        [setattr(port, 'excessAccuRtnBreakDown', dict(zip(port[0].excessRtnBreakDown.keys(),excessAccuRtnBreakDown[index]))) for index, port in enumerate(self.portfolio)]

    def setBenchmark(self, codeSeries,benchmarkCodeSeries,benchmarkTimeSeriesObj:benchmarkTimeSeries):
        codeBenchDict = dict(zip(codeSeries,benchmarkCodeSeries))
        benchmarkOnLatestDate = [benchmarkTimeSeriesObj.filter(lambda x:x.tradingDate<=date.tradingDate) for date in self]
        [i.sort('tradingDate',inplace=True) for i in benchmarkOnLatestDate]
        benchmarkOnLatestDate = [i[-1] if len(i)>0 else benchmarkTimeSeries.elementClass().new() for i in benchmarkOnLatestDate]
        benchmarkOnLatestDate = [benchmark[list(codeBenchDict.values())] for benchmark in benchmarkOnLatestDate]
        benchmarkOnLatestDateList = [benchmarkTimeSeries.elementClass().new() for i in benchmarkOnLatestDate]
        [benchmarkOnLatestDateList[index].setAll(j) for index,j in enumerate(benchmarkOnLatestDate)]
        [date.setBenchmark(codeBenchDict.keys(),[benchmark[codeBenchDict[obj]] for obj in codeBenchDict.keys()]) for date,benchmark in zip(self.all,benchmarkOnLatestDateList)]

    def addSubPortfolioByBenchmark(self, linkedAttrName = ''):
        self.execFunc('execFunc','addSubPortfolioByBenchmarkForEveryPortfolio', linkedAttrName)

    def calBrinsonBreakDown(self):
        self.execFunc('calBrinsonBreakDown')
        self.reformToPortfolio()
        self.linkTimeSeries()

    def calSubPortfolioBreakDown(self,subPortfolioCodeList):
        self.execFunc('calSubPortfolioBreakDown',subPortfolioCodeList)
        self.reformToPortfolio()
        self.linkTimeSeries()


    def calBreakDown(self,attrName,targetFunctionName):
        self.execFunc('calBreakDown',attrName,targetFunctionName)
        self.reformToPortfolio()
        self.linkTimeSeries()

#->module
from Src.portfolioTimeSeries import portfolioTimeSeries
