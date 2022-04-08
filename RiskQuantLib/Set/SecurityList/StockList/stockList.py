#!/usr/bin/python
#coding = utf-8

import numpy as np
from RiskQuantLib.Set.SecurityList.base import setBaseList


class setStockList(setBaseList):
    def __nullFunction__(self):
        pass

    # build module, contents below will be automatically built and replaced, self-defined functions shouldn't be written here
    #-<Begin>
    def setIndustry(self,codeSeries,industrySeries):
        industryDict = dict(zip(codeSeries,industrySeries))
        [i.setIndustry(industryDict[i.code]) if i.code in industryDict.keys() else i.setIndustry(np.nan) for i in self.all]
    #-<End>