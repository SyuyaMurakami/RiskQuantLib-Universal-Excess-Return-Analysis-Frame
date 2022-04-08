#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from RiskQuantLib.SubPortfolio.subPortfolio import subPortfolio
from RiskQuantLib.Operation.listBaseOperation import listBase
from RiskQuantLib.Set.SubPortfolioList.subPortfolioList import setSubPortfolioList
class subPortfolioList(listBase,setSubPortfolioList):
    def __nullFunction__(self):
        pass
    elementClass = subPortfolio
    def __init__(self):
        self.all = []
        self.listType = 'Sub-Portfolio List'
    def addSubPortfolio(self, securityCode,securityName,securityTypeString = "Sub-Portfolio"):
        securitySeries = self.all+[subPortfolio(securityCode,securityName,securityTypeString)]
        self.setAll(securitySeries)
    def addSubPortfolioSeries(self, securityCodeSeries,securityNameSeries,securityTypeString = "Sub-Portfolio"):
        securitySeries = [subPortfolio(i,j,securityTypeString) for i,j in zip(securityCodeSeries,securityNameSeries)]
        self.setAll(self.all + securitySeries)