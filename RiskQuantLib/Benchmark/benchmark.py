#!/usr/bin/python
# coding = utf-8
import numpy as np

from RiskQuantLib.Set.Benchmark.benchmark import setBenchmark
from RiskQuantLib.Operation.listBaseOperation import listBase
from RiskQuantLib.SubPortfolioList.subPortfolioList import subPortfolioList,subPortfolio
from RiskQuantLib.Security.base import base as securityBase
class benchmark(setBenchmark,listBase):
    def __nullFunction__(self):
        pass
    elementClass = securityBase
    def __init__(self, codeString = '',nameString = '',securityTypeString = 'Benchmark'):
        self.code = codeString
        self.name = nameString
        self.securityType = securityTypeString
        self.subPortfolio = subPortfolioList()
        self.all = []
        self.weight = 0.0
        self.rtn = 0.0

    def addHolding(self, element):
        self.setAll(self.all + [element])

    def addHoldingSeries(self, elementList):
        if hasattr(elementList,'all') and type(getattr(elementList,'all',np.nan))==type([]):
            self.setAll(self.all + elementList.all)
        else:
            self.setAll(self.all + elementList)

    # classify benchmark holdings to sub-portfolio
    def addSubPortfolioByAttr(self, attrName: str):
        tmpList = self.groupBy(attrName=attrName, inplace=True)
        tmpSubPortfolioList = subPortfolioList()
        tmpSubPortfolioList.addSubPortfolioSeries(tmpList[attrName], tmpList[attrName])
        [subPortfolioIT.addHoldingSeries(holdings.all) for subPortfolioIT, holdings in zip(tmpSubPortfolioList, tmpList)]
        tmpSubPortfolioList.sort(['code'],inplace=True)
        self.subPortfolio.setAll(self.subPortfolio.all + tmpSubPortfolioList.all)

    def addSubPortfolio(self, subPT: subPortfolio):
        self.subPortfolio.setAll(self.subPortfolio.all + [subPT])

    def addSubPortfolioSeries(self, subPortfolioListObj):
        if hasattr(subPortfolioListObj,'all') and type(getattr(subPortfolioListObj,'all',np.nan))==type([]):
            self.subPortfolio.setAll(self.subPortfolio.all + subPortfolioListObj.all)
        else:
            self.subPortfolio.setAll(self.subPortfolio.all + subPortfolioListObj)

    def calRTN(self):
        self.subPortfolio.execFunc('calRTN')
        self.weight = self.sum('weight')
        self.rtn = np.nansum([w*r for w,r in zip(self['weight'],self['rtn'])])/self.weight if (not np.isnan(self.weight)) and self.weight!=0.0 else np.nanmean(self['rtn'])