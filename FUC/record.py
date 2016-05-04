# -*- coding: utf8 -*- 

from sys import path  #增加新的PATH
path.append(r"..\\")
import os,time,threading
PATH = './DLL'

#报告名
def filename():
    return time.strftime("%Y%m%d_%H-%M-%S", time.localtime()) 

def writeVariableList(verlist):
    try:
        VARLIST_TXT_PATH = PATH + "/ADS_VariableList.txt"
        with open(VARLIST_TXT_PATH,'w') as f:
            for i in verlist:
                f.write("%s\n"%i)   
    except Exception, e:
        print e
        
            
def startRecord(IP,port = '801',internal = 10, times = 300000):
    try:
        #变更：无需写文件
        #writeVariableList(verlist)     
        #好像并没有什么用
        #cmd_path = 'cmd /k cd /d %s' %PATH 

        print "recorder open"
        os.popen('cd "%s" & cmd /k AdsRecorder.exe  %s.1.1:%s ADS_VariableList.txt ../Recording/%s.txt /interval %s /record %s ' %(PATH, IP,port, filename(), internal, times)).read()          
        
        return True
    except Exception,e:
        print e
        return False
    
def stopRecord():
    try:
        cmd_path = 'cmd /k cd /d %s' %PATH       
            
        os.popen('cd "%s" & cmd /k del *.ctrl'%(PATH)).read()          
        print "recorder stop"
    except Exception,e:
        print e
        return False        
    
class RecordThread(threading.Thread):

    def __init__(self,threadname,ip,port = '801',internal = 10, times = 300000,win = None):
        self.ip = ip
        self.port = port
        self.internal = internal
        self.times = times
        threading.Thread.__init__(self,name=threadname)
        self.win = win
    def run(self):
        startRecord(self.ip,self.port,self.internal , self.times)
        if self.win != None:
            self.win.pushButton_startRecorder.setEnabled(True)
        print 'record thread is dead'
        return 


    
    
if __name__ == '__main__' :
    ver = ['.grsimu_setWindSpeed_1','.grGenSpeedForProcess']
    t1 = RecordThread('t1',ver,'testcase2')
    t1.start()
    print "fun1 start"
    #startRecord(ver,'runtest1')
    count = 10
    while count > 1:
        count = count -1
        time.sleep(1)
        print count
    stopRecord()