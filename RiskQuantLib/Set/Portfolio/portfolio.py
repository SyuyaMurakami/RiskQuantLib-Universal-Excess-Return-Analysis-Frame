#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
class setPortfolio():
    def __nullFunction__(self):
        pass
    def setBenchmark(self,BenchmarkObj):
        self.benchmark = BenchmarkObj
    def setTradingDate(self, tradingDate):
        from RiskQuantLib.Property.Date.date import date
        if not hasattr(self, '__tradingDate'):
            self.__tradingDate = date(tradingDate)
            self.tradingDate = self.__tradingDate.value
        else:
            self.__tradingDate.setValue(tradingDate)
            self.tradingDate = self.__tradingDate.value
    def setBelongTo(self, belongToString):
        self.belongTo = belongToString
    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    #-<End>