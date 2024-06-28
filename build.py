#!/usr/bin/python
# coding = utf-8
import os,sys,argparse
from RiskQuantLib import autoBuildProject,buildProject
path = sys.path[0] if not getattr(sys, "frozen", False) else os.path.dirname(sys.executable)
parser = argparse.ArgumentParser()
parser.add_argument("-a","--auto", help="use auto build model to build project dynamically", action="store_true")
parser.add_argument("-t", "--targetPath", type=str, help="the RiskQuantLib project you want to build")
parser.add_argument("-r", "--renderFromPath", type=str, help="the directory of source code where the template code exists")
parser.add_argument("-c", "--channel", type=str, help="if given a channel name, render action in this channel will not delete the result of render in other channel unless it is overwritten by current render")
parser.add_argument("-d", "--debug", help="use debug mode, break point in Src will start to effect", action="store_true")
args = parser.parse_args()
targetPath = args.targetPath if args.targetPath else path
renderFromPath = args.renderFromPath if args.renderFromPath else targetPath+os.sep+"Src"
bindType = args.channel if args.channel else "renderedSourceCode"
autoBuildProject(targetPath,renderFromPath,bindType,args.debug) if args.auto else buildProject(targetPath,renderFromPath,bindType,args.debug)