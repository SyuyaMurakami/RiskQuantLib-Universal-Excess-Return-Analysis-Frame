#!/usr/bin/python
#coding = utf-8

import numpy as np
from QuantLib import Instrument
from RiskQuantLib.Set.Security.base import setBase

class base(Instrument,setBase):
    """
    This is the security basic class. Any security should inherit from this class.
    """
    def __init__(self,codeString,nameString,securityTypeString = 'Security'):
        self.code = codeString
        self.name = nameString
        self.securityType = securityTypeString
        self.weight = 0.0
        self.rtn = 0.0

    def __getitem__(self, item):
        return getattr(self,item,np.nan)

    def __str__(self):
        return self.code

    def iniPricingModule(self,*args):
        Instrument.__init__(self,*args)

    def calRTN(self):
        pass






