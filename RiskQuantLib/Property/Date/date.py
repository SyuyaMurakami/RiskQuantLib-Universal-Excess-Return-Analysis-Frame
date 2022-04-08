#!/usr/bin/python
# coding = utf-8
import pandas as pd

from RiskQuantLib.Property.base import base
class date(base):
    def __nullFunction__(self):
        pass
    def __init__(self, value : str):
        super(date,self).__init__(pd.Timestamp(value))
    def setValue(self,value : str):
        self.value = pd.Timestamp(value)