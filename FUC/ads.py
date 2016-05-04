# -*- coding: utf-8 -*-
#editer: yao
#date:2014/04/27
#version: 1.0
import ads,config
import os,time
ini =  config.Config()
method = int(ini.getConfig('adsMathed'))
if method == 1:
    adsMethod =True
else:
    from ctypes import *
    import platform
    adsMethod = False
    windowsType = platform.architecture()
    WinBit = windowsType[0]
    print WinBit

    if WinBit == '32bit':
	DLLDIR ='./Dll/x32/TESTDLL.dll' 
    else:
	DLLDIR ='./Dll/x64/TESTDLL.dll' 
from PyQt4.QtGui import QMessageBox


PATH = './/DLL'
def readDLL(ip,name):
    try:
        dll = cdll.LoadLibrary(DLLDIR)
        dll.AdsSingleRead.restype = c_char_p               
        name = name.strip()
        ret = dll.AdsSingleRead(ip,name)  
        dll = None
        if ret == ";":
            QMessageBox.warning(self, 'WORNING', "There is no connect")  
            return None
        else:
            dataAndType = ret.split(';')
            datatype = dataAndType[1]
            recdata = dataAndType[0]
            #print datatype,recdata
            data = turnTypeDLL(recdata,datatype)
            return data
    except:
        return None
    
def getTypeDLL(ip,name):
    try:
        dll = cdll.LoadLibrary(DLLDIR)
        dll.AdsSingleRead.restype = c_char_p               
        name = name.strip()        
        ret = dll.AdsSingleRead(ip,name)  
	dll = None
        if ret == ";":            
            return None
        else:
            dataAndType = ret.split(';')
            datatype = dataAndType[1]
            return datatype
    except:
        return None    
    
def turnTypeDLL(name,datatype):
    if datatype[0] == "I" or datatype[0] == "U" or datatype[0] == "T" or datatype[0] == "B":
        name = int(name)
    elif datatype[0] == "F" or datatype[0] == "D":
        name = float(name)
        name = round(name,3)
    elif datatype[0] == "B":
        name = bool(name)
    elif datatype[0] == "S":
        name = str(name)
    else: 
        QMessageBox.warning(self, 'WORNING', "The type is not available")          
    return name

def writeDLL(ip,name,value):
    try:
        dll = cdll.LoadLibrary(DLLDIR)
        dll.AdsSingleRead.restype = c_char_p                 
        name = name.strip()
        ret = dll.AdsSingleWrite(ip,name,str(value)) 
        dll = None
        if ret == "-1":
            QMessageBox.warning(self, 'WORNING', "There is no connect")  
            return None
        return True
    except:
        return None
    
    
    
#获得对应变量类型     
def adsGetType(ip,name):
    try:

        #cmd_path = 'cmd /k cd /d %s' %PATH        
        
        info = os.popen('cd "%s" & cmd /k Envision.Tools.TcAds.VariableCmd.exe /t %s %s' %(PATH,ip,name)).read()          
        info =info.replace('\n','\t')
        data = info.split('\t')               
        return data[2]
    except Exception,e:
        print e
        return False
    
#读取或要写入的值转换为变量对应的类型
def adsTurnType(ip,name,data):    
    try:
        vartype = adsGetType(ip,name)
        #print vartype
        if vartype[-3:] == "INT":       #int型
            data = int(data)
        elif vartype[-4:] == "REAL":    #real对应float型
            
            data = float(data)
            #data = '%.3f'%data   #小数位最多3位
        elif vartype == "BOOL":         #Bool型
            data = bool(int(data))
            #print "it is a bool"
        else:  
            data = str(data)            #字符串或者其他
        return data
    except Exception,e:
        print e,"turn type",name
        return data
    
#ads通道读取
def adsRead(ip,name):
    try:
        #cmd_path = 'cmd /k cd /d %s' %PATH        
        info = os.popen('cd "%s" & cmd /k Envision.Tools.TcAds.VariableCmd.exe /r %s %s' %(PATH,ip,name)).read()

        #print 'INFO',info,cmd_path,name
        info =info.replace('\n','\t')
        data = info.split('\t')
        #print data
        #print 'DATA',len(data),data    
        ver = data[2]
        return adsTurnType(ip,name,ver)   #读取数据后要修改数据类型
    except Exception,e:
        print e,";the connection is time out",name
        return None
    
#ads通道写入变量
def adsWrite(ip,name,var,sign = "/nocheck /nomsgbox"):
    try:
        adsTurnType(ip,name,var)   #写入前先转换数据类型
        #print name,var,sign
        #cmd_path = 'cmd /k cd /d %s' %PATH
        Tab ='     '
        info = os.popen('cd "%s" & cmd /k Envision.Tools.TcAds.VariableCmd.exe %s /w %s %s %s' %(PATH,sign,ip,name,var)).read()
        time.sleep(0.01)
        return True
    except Exception,e:
        print name
        print e,";the connection is time out",name
        return None
        
 
def read(ip,name):
    
    if not adsMethod:     
        return readDLL(ip, name)
    else:
        
        return adsRead(ip,name)
        
def write(ip,name,value):
    if not adsMethod:
        return writeDLL(ip, name, value)
    else:
        return adsWrite(ip, name, value)
        
def getType(ip,name):
    if not adsMethod:
        return getTypeDLL(ip, name)
    else:
        return adsGetType(ip, name)
            
if __name__ == "__main__":            
    print "start"
    strname = ".gsControlCodeBuildNo"
    uintname = ".aqsimuCANCON_txPDO3_WORD3"
    usintname = ".gistate"
    intname = ".aqsimuCAN_ABB_CVT_txPDO2_WORD4"
    realname = ".grsimu_TempGearBearingDE"
    boolname = ".gbsimu_FreezeWindSpeed"  
    gar = '.SCADA.GEARBOX.PAR.Ctrl_PAR_bEnablePowerReduByGearbox'
    ip = "172.16.43.189.1.1:801"
    
    print read(ip,gar)
    #value = 123.32
    #write(ip, realname, value)
    #print read(ip,realname)