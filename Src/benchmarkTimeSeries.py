#!/usr/bin/python
# coding = utf-8

import numpy as np
import pandas as pd
from RiskQuantLib.InstrumentList.BenchmarkList.benchmarkList import benchmarkList
from RiskQuantLib.Operation.operation import operation
from RiskQuantLib.Auto.InstrumentList.BenchmarkList.benchmarkList import benchmarkListAuto

class benchmarkTimeSeries(operation,benchmarkListAuto):

    elementClass = benchmarkList

    def __init__(self):
        self.all = []
        self.listType = 'Benchmark Time Series'

    def addBenchmarkFromHolding(self, holdingList):
        if hasattr(holdingList,'all') and type(getattr(holdingList,'all',np.nan))==type([]):
            tmpObj = holdingList.groupBy('tradingDate')
        else:
            tmpObj = self.new()
            tmpObj.setAll(holdingList)
            tmpObj = tmpObj.groupBy('tradingDate')
        securitySeries = [benchmarkList() for _ in tmpObj['belongTo']]
        [port.addBenchmarkFromHolding(holding) for port, holding in zip(securitySeries, tmpObj)]
        [setattr(port,'tradingDate',holding.tradingDate) for port, holding in zip(securitySeries, tmpObj)]
        self.setAll(self.all + securitySeries)

    def addSubPortfolioByAttr(self,attrName : str):
        self.execFunc('addSubPortfolioByAttr',attrName)

#->module
from Src.benchmarkTimeSeries import benchmarkTimeSeries