# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
import os,sys,time
from FUC import config,ads
reload(sys)   
sys.setdefaultencoding('gbk') 


class SCshow(QThread) :
    """"""
    sinOut1 = pyqtSignal(list)
    sinOut2 = pyqtSignal()

    #----------------------------------------------------------------------
    def __init__(self,parent=None):
        super(SCshow, self).__init__(parent)
    
    def update(self,ip,version):
        self.version = version
        cf = config.Config(version)
        try:
            self.scarrayname = cf.getVarValue('listofactivesc')    
        except Exception,e:
            print e
            return 

        self.ip = ip
        self.listening = True
        self.start()

    def run(self):
        disconnectCount  = 0
        oldlist = []
        while self.listening :    
            ret = self.getSClist(self.ip,self.version)
            if ret == []:
                disconnectCount += 1
                if disconnectCount > 3:
                    self.listening =  False
                    self.sinOut2.emit()
            if ret != oldlist:
                self.sinOut1.emit(ret)
            time.sleep(1)
            oldlist = ret
            
    def stop(self):
        self.listening = False

    def getSClist(self,ip,version):
        varlist = []
        arrayList = []
        NUMOFLIST = 34        
        try:
            time.sleep(0.5)
            for i in xrange(1,NUMOFLIST):
                sname = ""
                var = ""
                #if version == "GEN":
                    #sname = self.scarrayname + str(i)
                #elif version == "SC1":           
                    #sname = self.scarrayname + "["+str(i)+"]"  
                sname = self.scarrayname%i
                var = ads.read(ip, sname)
                if  var == None:
                    del arrayList[:]
                    return []
                if var == '' or var[0] == "x" :
                    break
                varlist.append(var)        
                for i in varlist:
                    valuelist = i.split('     ')
                    if version == "SC1"  and valuelist != []: 
                        valuelist.insert(1,'')                
                    for v in range(len(valuelist)):
                        valuelist[v] = valuelist[v].strip()
                        if v == 0 or v == 2:
                            valuelist[v] = valuelist[v].replace('_','')                
                arrayList.append(valuelist)
        except Exception,e:
            print e
        return arrayList
    
