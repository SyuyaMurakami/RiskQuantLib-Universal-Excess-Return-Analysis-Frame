#!/usr/bin/python
# coding = utf-8
import numpy as np
from RiskQuantLib.Set.SubPortfolio.subPortfolio import setSubPortfolio
from RiskQuantLib.Operation.listBaseOperation import listBase
from RiskQuantLib.Security.base import base as securityBase
class subPortfolio(setSubPortfolio,listBase):
    def __nullFunction__(self):
        pass
    elementClass = securityBase
    def __init__(self, codeString = '', nameString = '',securityTypeString = 'Sub-Portfolio'):
        self.code = codeString
        self.name = nameString
        self.securityType = securityTypeString
        self.all = []
        self.weight = 0.0
        self.rtn = 0.0

    def addHolding(self, holdingObj):
        securitySeries = self.all+[holdingObj]
        self.setAll(securitySeries)

    def addHoldingSeries(self, holdingList):
        if hasattr(holdingList, 'all') and type(getattr(holdingList,'all',np.nan))==type([]):
            securitySeries = self.all + holdingList.all
        else:
            securitySeries = self.all + holdingList
        self.setAll(securitySeries)

    def calRTN(self):
        [i.calRTN() for i in self.all]
        self.weight = np.nansum(self['weight'])
        self.rtn = np.nansum([w*r for w,r in zip(self['weight'],self['rtn'])])/self.weight if (not np.isnan(self.weight)) and self.weight!=0.0 else np.nanmean(self['rtn'])