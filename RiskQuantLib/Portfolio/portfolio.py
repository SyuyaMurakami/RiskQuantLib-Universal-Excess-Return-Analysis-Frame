#!/usr/bin/python
# coding = utf-8
import numpy as np
from RiskQuantLib.Set.Portfolio.portfolio import setPortfolio
from RiskQuantLib.Operation.listBaseOperation import listBase
from RiskQuantLib.SubPortfolioList.subPortfolioList import subPortfolioList,subPortfolio
from RiskQuantLib.Security.base import base as securityBase
class portfolio(setPortfolio,listBase):

    elementClass = securityBase

    def __init__(self, codeString = '' , nameString = '' , securityTypeString = 'Portfolio'):
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
        tmpSubPortfolioList.sort(['code'], inplace=True)
        self.subPortfolio.setAll(self.subPortfolio.all + tmpSubPortfolioList.all)

    def addSubPortfolioByBenchmark(self, linkedAttrName = ''):
        if linkedAttrName == '':
            codeList = [i['code'] for i in self.benchmark.subPortfolio]
            tmpHoldingList = [[j for j in self.all if j.code in i] for i in codeList]
        else:
            tmpHoldingList = [[j for j in self.all if getattr(j,linkedAttrName,np.nan) == i.code] for i in self.benchmark.subPortfolio]
        tmpSubPortfolioList = subPortfolioList()
        tmpSubPortfolioList.addSubPortfolioSeries(self.benchmark.subPortfolio['code'],self.benchmark.subPortfolio['name'])
        [port.setAll(hold) for port,hold in zip(tmpSubPortfolioList,tmpHoldingList)]
        self.subPortfolio.setAll(self.subPortfolio.all + tmpSubPortfolioList.all)

    def addSubPortfolio(self, subPT: subPortfolio):
        self.subPortfolio.setAll(self.subPortfolio.all + [subPT])

    def addSubPortfolioSeries(self, subPortfolioListObj):
        if hasattr(subPortfolioListObj,'all') and type(getattr(subPortfolioListObj,'all',np.nan))==type([]):
            self.subPortfolio.setAll(self.subPortfolio.all + subPortfolioListObj.all)
        else:
            self.subPortfolio.setAll(self.subPortfolio.all + subPortfolioListObj)

    def registerExcessRtnBreakDown(self, attrName):
        if type(attrName)==type(''):
            attrName = [attrName]
        elif type(attrName)==type([]):
            pass
        else:
            return
        if not hasattr(self,'excessRTN'):
            self.calExcessRTN()
        breakDownValue = [getattr(self,i,np.nan) for i in attrName]
        self.excessRtnBreakDown = dict(zip(attrName,breakDownValue))
        residual = self.excessRTN - np.nansum([self.excessRtnBreakDown[i] for i in self.excessRtnBreakDown.keys() if i!='residual'])
        self.excessRtnBreakDown['residual'] = residual

    def calRTN(self):
        self.subPortfolio.execFunc('calRTN')
        self.weight = self.sum('weight')
        self.rtn = np.nansum([w*r for w,r in zip(self['weight'],self['rtn'])])/self.weight if (not np.isnan(self.weight)) and self.weight!=0.0 else np.nanmean(self['rtn'])

    def calExcessRTN(self):
        self.benchmark.calRTN()
        self.calRTN()
        self.excessRTN = self.rtn - self.benchmark.rtn
        self.logLinkingMultiplier = (np.log(1+self.rtn) - np.log(1+self.benchmark.rtn))/(self.rtn - self.benchmark.rtn)

    def calAllocationRTN(self):
        self.allocationRTN = np.nansum([(subP.weight-benchmarkP.weight)*benchmarkP.rtn for subP,benchmarkP in zip(self.subPortfolio,self.benchmark.subPortfolio)])

    def calSelectionRTN(self):
        self.selectionRTN = np.nansum([(subP.rtn-benchmarkP.rtn)*benchmarkP.weight for subP,benchmarkP in zip(self.subPortfolio,self.benchmark.subPortfolio)])

    def calInteractionRTN(self):
        self.interactionRTN = np.nansum([subP.weight*subP.rtn - benchmarkP.weight*subP.rtn-subP.weight*benchmarkP.rtn+benchmarkP.weight*benchmarkP.rtn for subP,benchmarkP in zip(self.subPortfolio,self.benchmark.subPortfolio)])

    def calSubPortfolioExcessRTN(self,subPortfolioCodeList):
        [setattr(self,subPortfolioCode+'ExcessRTN',getattr(self.subPortfolio[subPortfolioCode],'rtn',np.nan) - getattr(self.benchmark.subPortfolio[subPortfolioCode],'rtn',np.nan)) for subPortfolioCode in subPortfolioCodeList]

    def calBrinsonBreakDown(self):
        self.calBreakDown(['allocationRTN', 'selectionRTN', 'interactionRTN'],['calAllocationRTN','calSelectionRTN','calInteractionRTN'])

    def calSubPortfolioBreakDown(self,subPortfolioCodeList):
        self.calBreakDown([i + 'ExcessRTN' for i in subPortfolioCodeList],['calSubPortfolioExcessRTN'],subPortfolioCodeList)

    def calBreakDown(self,attrName, targetFunctionName, *args):
        self.calExcessRTN()
        if type(targetFunctionName)==type(''):
            targetFunctionName = [targetFunctionName]
        elif type(targetFunctionName)==type([]):
            pass
        else:
            return
        [getattr(self,i,lambda *args:None)(*args) for i in targetFunctionName]
        self.registerExcessRtnBreakDown(attrName)