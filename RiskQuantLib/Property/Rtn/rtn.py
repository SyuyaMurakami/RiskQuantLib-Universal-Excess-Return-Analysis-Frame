#!/usr/bin/python
# coding = utf-8
import numpy as np

from RiskQuantLib.Property.base import base
class rtn(base):
    def __nullFunction__(self):
        pass
    def __init__(self, value):
        super(rtn,self).__init__(value)
        self.form = 'Normal'

    def changeToLog(self):
        if self.form == 'Normal':
            self.value = np.log(self.value+1)
            self.form = 'Log'

    def changeToNormal(self):
        if self.form == 'Log':
            self.value = np.exp(self.value)-1
            self.form = 'Normal'
