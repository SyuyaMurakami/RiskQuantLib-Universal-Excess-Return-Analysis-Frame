#!/usr/bin/python
#coding = utf-8
import numpy as np

class setBaseList:

    def setIssuer(self,codeSeries,issuerSeries):
        issuerDict = dict(zip(codeSeries,issuerSeries))
        [i.setIssuer(issuerDict[i.code]) if i.code in issuerDict.keys() else i.setIssuer('') for i in self.all]

    def setHistoricalCost(self,codeSeries,costSeries):
        costDict = dict(zip(codeSeries,costSeries))
        [i.setHistoricalCost(costDict[i.code]) if i.code in costDict.keys() else i.setHistoricalCost(np.nan) for i in self.all]

    def setHoldingAmount(self,codeSeries,holdingAmountSeries):
        holdingAmountDict = dict(zip(codeSeries,holdingAmountSeries))
        [i.setHoldingAmount(holdingAmountDict[i.code]) if i.code in holdingAmountDict.keys() else i.setHoldingAmount(np.nan) for i in self.all]


    def setWeight(self,codeSeries,weightSeries):
        weightDict = dict(zip(codeSeries,weightSeries))
        [i.setWeight(weightDict[i.code]) if i.code in weightDict.keys() else i.setWeight(np.nan) for i in self.all]
    def setRtn(self,codeSeries,rtnSeries):
        rtnDict = dict(zip(codeSeries,rtnSeries))
        [i.setRtn(rtnDict[i.code]) if i.code in rtnDict.keys() else i.setRtn(np.nan) for i in self.all]
    def setTradingDate(self,codeSeries,tradingDateSeries):
        tradingDateDict = dict(zip(codeSeries,tradingDateSeries))
        [i.setTradingDate(tradingDateDict[i.code]) if i.code in tradingDateDict.keys() else i.setTradingDate(np.nan) for i in self.all]
    def setBelongTo(self,codeSeries,belongToSeries):
        belongToDict = dict(zip(codeSeries,belongToSeries))
        [i.setBelongTo(belongToDict[i.code]) if i.code in belongToDict.keys() else i.setBelongTo(np.nan) for i in self.all]
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>