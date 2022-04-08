#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.Benchmark.benchmark import benchmark
from RiskQuantLib.Operation.listBaseOperation import listBase
from RiskQuantLib.Set.BenchmarkList.benchmarkList import setBenchmarkList
class benchmarkList(listBase,setBenchmarkList):
    def __nullFunction__(self):
        pass
    elementClass = benchmark
    def __init__(self):
        self.all = []
        self.listType = 'Benchmark List'
    def addBenchmark(self, securityCode,securityName,securityTypeString = "Benchmark"):
        securitySeries = self.all+[benchmark(securityCode,securityName,securityTypeString)]
        self.setAll(securitySeries)
    def addBenchmarkSeries(self, securityCodeSeries,securityNameSeries,securityTypeString = "Benchmark"):
        securitySeries = [benchmark(i,j,securityTypeString) for i,j in zip(securityCodeSeries,securityNameSeries)]
        self.setAll(self.all + securitySeries)
    def addBenchmarkFromHolding(self, holdingList):
        if hasattr(holdingList,'all') and type(getattr(holdingList,'all',np.nan))==type([]):
            tmpObj = holdingList.groupBy('belongTo')
        else:
            tmpObj = self.new()
            tmpObj.setAll(holdingList)
            tmpObj = tmpObj.groupBy('belongTo')
        securitySeries = [benchmark(i, i) for i in tmpObj['belongTo']]
        [port.addHoldingSeries(holding) for port, holding in zip(securitySeries, tmpObj)]
        self.setAll(self.all + securitySeries)
    def addSubPortfolioByAttr(self,attrName : str):
        self.execFunc('addSubPortfolioByAttr',attrName)