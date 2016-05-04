# -*- coding: utf-8 -*-
from sys import path  #增加新的PATH
path.append(r".\\DLL")
import re,os
import ads,config
ini =  config.Config()
MAX_IP_COUNT = ini.getConfig('MAX_IP_COUNT')
MAX_VAR_COUNT = ini.getConfig('MAX_VAR_COUNT')

#用于确认连接情况及PLC程序版本
def check_conection(ip,versionType):    
    strVersion = ""
    ratedPower =0
    state = False
    ini.setVersion(versionType)
    buildNo = ini.getVarValue('buildNo')
    strVersion = ads.read(ip, buildNo)
    if  strVersion != None:
        state = True
    return state,strVersion
        
#用于从临时文件读取历史数据
def loadCombox():
    try:
        iplist = []
        varlist = []
        mode = True
        with open(".\DLL\Temp.txt","r") as f:
            for i in f.readlines():
                line = str(i).replace('\n','')              
                if line != "var:":
                    if mode:
                        iplist.append(line)
                    else:
                        varlist.append(line)
                else:
                    mode = False
    except Exception,e:
        print e
    return iplist,varlist   


def saveCombox(ipcombox,varcombox):

    i = 0
    with open(".\DLL\Temp.txt","w") as f:
        for ip in ipcombox:
            f.write(ip)
            f.write('\n')
            i += 1
            if i > MAX_IP_COUNT :
                break
        f.write("var:\n") 
        i = 0
        for var in varcombox:           
            f.write(var)
            f.write('\n')     
            i += 1
            if i > MAX_VAR_COUNT :
                break         

def saveBatchCombox(varlist):
    i = 0 
    with open('.\DLL\Temp_var.txt','w') as f:
        for var in varlist:
            f.write(var)
            f.write('\n')
            i += 1
            if i > MAX_VAR_COUNT :
                break                 
            
            
def loadBatchCombox():
    try:
        PATH = ".\DLL\Temp_var.txt"
        varlist = []
        if not os.path.exists(PATH):           
            return varlist
        with open(".\DLL\Temp_var.txt","r") as f:
            for line in f.readlines():
                if line != "":
                    line = str(line).replace('\n','')           
                    varlist.append(line)

    except Exception,e:
        print e
    return varlist   

def loadVersionType():
    versionTypeList = []
    try:
        strVersionType = str(ini.getConfig('versiontype')).strip()
        versionTypeList = strVersionType.split(',')
    except Exception,e:
        print e
    return versionTypeList
        