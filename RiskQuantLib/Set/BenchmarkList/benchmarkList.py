#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
class setBenchmarkList():
    def __nullFunction__(self):
        pass
    def setTradingDate(self,codeSeries,tradingDateSeries):
        tradingDateDict = dict(zip(codeSeries,tradingDateSeries))
        [i.setTradingDate(tradingDateDict[i.code]) if i.code in tradingDateDict.keys() else i.setTradingDate(np.nan) for i in self.all]
    def setBelongTo(self,codeSeries,belongToSeries):
        belongToDict = dict(zip(codeSeries,belongToSeries))
        [i.setBelongTo(belongToDict[i.code]) if i.code in belongToDict.keys() else i.setBelongTo(np.nan) for i in self.all]
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>