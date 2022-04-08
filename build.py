#!/usr/bin/python
# coding = utf-8
import os
import sys
import time
from RiskQuantLib.Build.build import buildAttr as BA
from RiskQuantLib.Build.build import buildInstrument as BI
path = sys.path[0]
BI(path + os.sep + "Build_Instrument.xlsx")
time.sleep(2)
BA(path + os.sep + "Build_Attr.xlsx")