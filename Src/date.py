#!/usr/bin/python
# coding = utf-8

#->date@import
import pandas as pd

#->date@init
def __init__(self, value : str):
    self.value = pd.Timestamp(value)
    self.belongToObject = None
    self.belongToAttrName = ''

#->date
def setValue(self,value : str):
    self.value = pd.Timestamp(value)


