# -*- coding: utf-8 -*- 
from sys import path  #增加新的PATH
path.append(r"..\\")
import re
from FUC import *

def getState(ip,ini):    
    try:
        snamelist = []
        datalist = []
        namelist = ['Power','Generator_Speed','Wind_Speed','Turbine_Operation_Mode','BPLEVEL','YPLEVEL']        
        for i in namelist:
            data  = ''
            data = ini.getVarValue(i) 
            snamelist.append(data)
        for var in snamelist:
            rdata = ''
            rdata = ads.read(ip,var)
            datalist.append(rdata)
        return datalist
    except Exception,e:
        print e
        return datalist
    

    
if __name__ == '__main__' :
    ip ='172.16.43.189.1.1:801'
    ini = config.Config('SC1')
    print getSClist(ip)