#!/usr/bin/python
# -*- coding:utf-8 -*-
#author: lianjun.yao
#desc: use to db ops
#---------------------
#2015-08-07 created
#---------------------
import sys,os
import ConfigParser
#iniAdd = "./src/config.ini"
iniAdd = "./DLL/config.ini"
class Config():
    def __init__(self,version = 'GEN'):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(iniAdd)
        self.version = version
        
    def setVersion(self,version):
        self.version = version
        
    def getValue(self,sections,option):
        self.cf.read(iniAdd)
        return self.cf.get(sections, option)
        
    def getName(self,sections):
        #print self.cf.sections()
        self.cf.read(iniAdd)
        return self.cf.options(sections)
    
    def getDic(self,sections):
        self.cf.read(iniAdd)
        sectionlist = self.getName(sections)
        dic = {}
        for i in sectionlist:
            dic[i] = self.cf.get(sections,i)
        return dic
    
    def writeInI(self,sections,option,value):  
        self.cf.read(iniAdd)
        self.cf.set(sections, option,value)
        fp = open(iniAdd,"w")
        self.cf.write(fp)
    
    def getSimuDic(self):
        self.cf.read(iniAdd)
        sections = self.version+ "-Simu"
        return self.getDic(sections)
    
    
    def getVarValue(self,option):    
        self.cf.read(iniAdd)
        sections = self.version +"-VAR"
        return self.getValue(sections, option)        
    
    def getConfig(self,option):
        self.cf.read(iniAdd)
        sections = 'CONFIG'
        return self.getValue(sections, option)                

if __name__ == "__main__":        
    #sections = "F5_list"
    #get(sections)
    #option = ".grsimu_setWaneDir_1"
    #value = 0
    #setIni(sections, option, value)
    #print get(sections)
    #print getDic(sections)
    sections1 = "IP_Temp"
    sections2 = "VAR_Temp"
    list1 = ["1afadfa","2fsasfaf","3adsfdsafas","4dsafdsfasdfsaf"]
    list2 = ["4afadfa","3fsasfaf","2adsfdsafas","1dsafdsfasdfsaf"]    
    ini = Config('SC1')
    ini.writeInI(sections1, sections1, list1)
    ini.writeInI(sections2, sections2, list2)
    var1 = ini.getValue(sections2, sections2)
    print var1,type(var1)