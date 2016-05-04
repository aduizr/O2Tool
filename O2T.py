# -*- coding: utf-8 -*-

"""
Module implementing O2Tool.
"""
from PyQt4.QtGui import   * #QDialog, QApplication, QMainWindow, 
from PyQt4.QtCore import *  #pyqtSignature

import sys,os,time
from Ui_O2T import Ui_O2Tool
from FUC import *
from scTable import SCstate
from scHistory import SChistory
RECORDERPATH = "Recording"




class O2Tool(QMainWindow, Ui_O2Tool):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        with open('./DLL/ADS_VariableList.txt','r') as f:
            varlist = f.read()
        if varlist != "":
            self.textEdit_var_recorder.setText(varlist)
        self.QIP = ""
        self.port = ''
        self.AmsNetID = ""
        self.connectState = False
        self.varlistchanged = True
        self.batchVarListChanged= True
        self.listening = False
        self.limitEnable = False
        self.versionType = ""
        self.scID = 0
        self.sc = ''
        self.ratedpower = 0
        self.iplist = set
        self.varlist = set
        self.batchVarList = set        
        self.iplist,self.varlist = connect.loadCombox()
        self.batchVarList = connect.loadBatchCombox()        
        if self.iplist != []:
            self.comboBox_ip.addItems(self.iplist)
        if self.varlist!= []:
            self.comboBox_name.addItems(self.varlist)
        self.comboBox_ip.setCurrentIndex(0)
        self.comboBox_name.setCurrentIndex(0)          
        if self.batchVarList != []:
            self.comboBox_batchVar1.addItems(self.batchVarList)
            self.comboBox_batchVar1.setCurrentIndex(-1)
            self.comboBox_batchVar2.addItems(self.batchVarList)
            self.comboBox_batchVar2.setCurrentIndex(-1)
            self.comboBox_batchVar3.addItems(self.batchVarList)
            self.comboBox_batchVar3.setCurrentIndex(-1)
            self.comboBox_batchVar4.addItems(self.batchVarList)
            self.comboBox_batchVar4.setCurrentIndex(-1)
            self.comboBox_batchVar5.addItems(self.batchVarList)
            self.comboBox_batchVar5.setCurrentIndex(-1)
            self.comboBox_batchVar6.addItems(self.batchVarList)
            self.comboBox_batchVar6.setCurrentIndex(-1)
            self.comboBox_batchVar7.addItems(self.batchVarList)
            self.comboBox_batchVar7.setCurrentIndex(-1)
            self.comboBox_batchVar8.addItems(self.batchVarList)
            self.comboBox_batchVar8.setCurrentIndex(-1)
            self.comboBox_batchVar9.addItems(self.batchVarList)
            self.comboBox_batchVar9.setCurrentIndex(-1)
            self.comboBox_batchVar10.addItems(self.batchVarList)
            self.comboBox_batchVar10.setCurrentIndex(-1)
            self.comboBox_batchVar11.addItems(self.batchVarList)
            self.comboBox_batchVar11.setCurrentIndex(-1)
            self.comboBox_batchVar12.addItems(self.batchVarList)
            self.comboBox_batchVar12.setCurrentIndex(-1) 
        versionTypeList = connect.loadVersionType()
        if versionTypeList!= []:
            self.comboBox_version.addItems(versionTypeList)
        self.dockwindow = SCstate()
        self.dockwindow.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea,self.dockwindow)
        self.dockwindow.hide() 
        self.dialog_SChistory = SChistory()
        self.dialog_SChistory.hide()
        #self.dialog_SChistory.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.connectfunction()

    def connectfunction(self):
        self.connect(self.dockwindow,SIGNAL('output(QString)'),self.getSCcode) 
        self.connect(self.dialog_SChistory,SIGNAL('output(QString)'),self.getSCcode) 
        self.connect(self.dockwindow,SIGNAL('output(int)'),self.normalwindow)
        self.connect(self.lineEdit_port, SIGNAL("returnPressed()"), self.on_pushButton_adsConnect_clicked) 
        self.connect(self.lineEdit_set, SIGNAL("returnPressed()"), self.on_pushButton_adsWrite_clicked) 
        self.connect(self.lineEdit_windspeed, SIGNAL("returnPressed()"), self.on_pushButton_setWindspeed_clicked) 
        self.connect(self.lineEdit_Scada, SIGNAL("returnPressed()"), self.on_pushButton_setScada_clicked) 
        self.connect(self.lineEdit_Radius, SIGNAL("returnPressed()"), self.on_pushButton_setRadius_clicked)
        self.connect(self.lineEdit_SCcode, SIGNAL("returnPressed()"), self.on_pushButton_loadSC_clicked)
        self.connect(self.lineEdit_SCsetType, SIGNAL("returnPressed()"), self.on_pushButton_setSCmode_clicked)
        self.connect(self.lineEdit_SCsetdelay, SIGNAL("returnPressed()"), self.on_pushButton_setSCdelay_clicked)
        self.connect(self.lineEdit_SCresetDelay, SIGNAL("returnPressed()"), self.on_pushButton_setSCredelay_clicked)
        self.connect(self.lineEdit_SCrepeatTimes, SIGNAL("returnPressed()"), self.on_pushButton_setSCrepeat_clicked)
        self.connect(self.lineEdit_SCbplevel, SIGNAL("returnPressed()"), self.on_pushButton_setSCbplevel_clicked)
        self.connect(self.comboBox_ip,SIGNAL("returnPressed"),self.on_pushButton_adsConnect_clicked)
        self.connect(self.comboBox_name,SIGNAL("returnPressed"),self.on_pushButton_adsLoad_clicked)
        #self.connect(self.comboBox_ip.lineEdit,SIGNAL("returnPressed"),self.on_pushButton_adsConnect_clicked)
    


    def normalwindow(self,state):
        try: 
            if state == 1:
                self.resize(1100,500)         
            elif state == 0:
                self.resize(630,500)                
        except Exception,e:
            print e

    @pyqtSignature("")
    def on_pushButton_SClist_clicked(self):  
        if self.dockwindow.listening:
            self.dockwindow.close()
            self.resize(630,500)
        else:            
            self.dockwindow.show()
            self.resize(1100,500)            
            self.dockwindow.startThread()
            

    def closeEvent(self,event):
        if self.dockwindow.listening:
            self.dockwindow.close()
        self.dialog_SChistory.close()
        print "save"
        saveCombox(self.iplist, self.varlist)   
        self.close()
        
    def changeEvent(self,event):
        if event.type() == QEvent.WindowStateChange and self.dockwindow.listening:
            if self.isMinimized():
                self.dockwindow.hide()            
            else:
                print "show"
                self.dockwindow.show()                


#======================================#    
#================ADS工具===============#          
    @pyqtSignature("")
    def on_pushButton_adsConnect_clicked(self):
        """
        make sure the tool connecting to the plc
        """
        if self.connectState:  
            self.connectState = False
            self.updateEnable()            
        else:            
            version = ''
            self.QIP = self.comboBox_ip.currentText()
            self.sIP = str(self.QIP).strip()
            self.port = str(self.lineEdit_port.text()).strip()
            self.AmsNetID =self.sIP  + ".1.1:"+ self.port
            self.versionType = str(self.comboBox_version.currentText())
            try:
                self.connectState,version = connect.check_conection(self.AmsNetID,self.versionType)
                #self.connectState,version,self.ratedpower,self.versionType  =True, "1232","12312321","sc1"
                if self.connectState and not version == "" :
                    #print self.iplist
                    self.comboBox_version.setEnabled(False)
                    self.updateEnable()
                    if self.sIP in self.iplist:
                        self.iplist.remove(self.sIP)
                        net = self.comboBox_ip.findText(self.QIP)
                        self.comboBox_ip.removeItem(net)   
                    self.comboBox_ip.insertItem(-1,self.QIP)
                    self.comboBox_ip.setCurrentIndex(0)
                    self.iplist.insert(0,self.sIP)                       
                    self.label_version.setText(version)
                    self.lineEdit_ip_recorder.setText(self.QIP) 
                    self.lineEdit_ip_batchRead.setText(self.AmsNetID)
                    self.lineEdit_ip_batch.setText(self.AmsNetID)
                    self.ini = config.Config(self.versionType)
                    ratedpower = self.ini.getVarValue('ratedpower')
                    self.ratedpower = ads.read(self.AmsNetID, ratedpower)
                    self.setWindowTitle('O2Tool  ' + str(self.AmsNetID) + '   ' + str(self.ratedpower))
                    self.dockwindow.getip(self.AmsNetID,self.versionType)
                    if self.versionType == 'SC1' or self.versionType == 'NGP':     
                        self.pushButton_bp150.setText( "BP_198")
                        self.pushButton_bp199.setText( "BP_200")
                    else:
                        self.pushButton_bp150.setText( "BP_150")
                        self.pushButton_bp199.setText( "BP_199") 
                    self.getSCvar()
                else:
                    if self.dockwindow.listening:
                        self.dockwindow.close()
                    self.connectState = False                    
                    self.updateEnable()   
                    QMessageBox.warning(self, 'WORNING',"There is no connection")
            except Exception, e : 
                self.connectState = False
                self.updateEnable() 
                QMessageBox.warning(self, 'WORNING', str(e))
  
                
    def getSCcode(self,sc):
        if sc != "":
            self.lineEdit_SCcode.setText(sc)
            self.tabWidget.setCurrentIndex(1)
            self.on_pushButton_loadSC_clicked()
    
    @pyqtSignature("")
    def on_pushButton_adsLoad_clicked(self):
        """
        ADS load variable.
        """        
        try:
            var = self.comboBox_name.currentText()
            strVar = str(var).strip()
            data = ads.read(self.AmsNetID,strVar)
            datatype = ads.getType(self.AmsNetID,strVar)
            if data == None: 
                strVar = "."+strVar
                data = ads.read(self.AmsNetID,strVar)
                datatype = ads.getType(self.AmsNetID,strVar)
                if data ==None:
                    word =  "Can not connet the varlue: "+strVar   
                    QMessageBox.warning(self, 'WORNING', str(word))
                    return 
            if strVar in self.varlist:
                self.varlist.remove(strVar)
                net = self.comboBox_name.findText(strVar)                    
                self.comboBox_name.removeItem(net)   
            self.comboBox_name.insertItem(-1,strVar)
            self.comboBox_name.setCurrentIndex(0)    
            self.varlist.insert(0,strVar)
            self.lineEdit_value.setText(str(data))
            self.lineEdit_type.setText(datatype)
            self.lineEdit_set.setFocus()
            if datatype == 'BOOL':
                self.pushButton_adsTrigger.setEnabled(True)
            else:
                self.pushButton_adsTrigger.setEnabled(False)
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))
            

        
        
    @pyqtSignature("")
    def on_pushButton_adsTrigger_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            strVar =  str(self.comboBox_name.currentText()).strip()
            #datatype = ads.getType(self.AmsNetID,strVar)
            ads.write(self.AmsNetID,strVar,0)
            time.sleep(0.05)
            ads.write(self.AmsNetID,strVar,1)
            time.sleep(0.05)
            ads.write(self.AmsNetID,strVar,0)
            time.sleep(0.05)
            self.on_pushButton_adsLoad_clicked()

            

        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))     
          
        
    @pyqtSignature("")
    def on_pushButton_adsWrite_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            strVar =  str(self.comboBox_name.currentText()).strip()
            data = str(self.lineEdit_set.text())
            ads.write(self.AmsNetID,strVar,data)
            self.on_pushButton_adsLoad_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))          
  
#======================================#    
#================常用工具===============#        
    @pyqtSignature("")
    def on_pushButton_loadWindspeed_clicked(self):
        try:
            option = "simuWindSpeed_1"
            var = self.ini.getVarValue(option)
            data = ads.read(self.AmsNetID,var)
            if data != None:
                self.lineEdit_windspeed.setText(str(data))
            else:
                QMessageBox.warning(self, 'WORNING', "Can not read the WindSpeed")
             
        except Exception,e:
            print e
    
    @pyqtSignature("")
    def on_pushButton_setWindspeed_clicked(self):
        option1 = "simuWindSpeed_1"
        option2 = "simuWindSpeed_2"
        var1 = self.ini.getVarValue(option1)
        var2 = self.ini.getVarValue(option2)
        data = str(self.lineEdit_windspeed.text())
        if data != None:
            ads.write(self.AmsNetID,var1,data)
            ads.write(self.AmsNetID,var2,data)
            self.on_pushButton_loadWindspeed_clicked()
        else:
            QMessageBox.warning(self, 'WORNING', "Can not set the WindSpeed")

    @pyqtSignature("")
    def on_pushButton_loadScada_clicked(self):
        option = "PowerLimitFromSCADA"
        var = self.ini.getVarValue(option)
        data = ads.read(self.AmsNetID,var)
        if data != None:
            self.lineEdit_Scada.setText(str(data))
        else:
            QMessageBox.warning(self, 'WORNING', "Can not read the Value")

    @pyqtSignature("")
    def on_pushButton_setScada_clicked(self):
        option = "PowerLimitFromSCADA"
        var = self.ini.getVarValue(option)
        data = str(self.lineEdit_Scada.text())
        if data != None:
            ads.write(self.AmsNetID,var,data)
            self.on_pushButton_loadScada_clicked()
        else:
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")
     

    @pyqtSignature("")
    def on_pushButton_resetScada_clicked(self):
        option = "PowerLimitFromSCADA"
        var = self.ini.getVarValue(option)        
        ads.write(self.AmsNetID,var,self.ratedpower)
        self.on_pushButton_loadScada_clicked()
     

    @pyqtSignature("")
    def on_pushButton_loadRadius_clicked(self):
        option = "RotorRadius"
        var = self.ini.getVarValue(option)
        data = ads.read(self.AmsNetID,var)
        if data != None:
            self.lineEdit_Radius.setText(str(data))
        else:
            QMessageBox.warning(self, 'WORNING', "Can not read the Value")
   
    @pyqtSignature("")
    def on_pushButton_setRadius_clicked(self):
        option = "RotorRadius"
        var = self.ini.getVarValue(option)
        data = str(self.lineEdit_Radius.text())
        if data != None:
            ads.write(self.AmsNetID,var,data)
            self.on_pushButton_loadRadius_clicked()
        else:
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")

    
    @pyqtSignature("")
    def on_pushButton_loadgearbox_clicked(self):
        option = "GB_Limit"
        var = self.ini.getVarValue(option)
        data = ads.read(self.AmsNetID,var)
        if data != None:
            self.lineEdit_Gearbox.setText(str(data))
        else:
            QMessageBox.warning(self, 'WORNING', "Can not read the Value")     
            
            
    @pyqtSignature("")
    def on_pushButton_enableGearbox_clicked(self):
        option = "GB_Limit"
        var = self.ini.getVarValue(option)
        data = "1"
        if data != None:
            ads.write(self.AmsNetID,var,data)
            self.on_pushButton_loadgearbox_clicked()
        else:
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")
    
    @pyqtSignature("")
    def on_pushButton_disableGearbox_clicked(self):
        option = "GB_Limit"
        var = self.ini.getVarValue(option)
        data = "0"
        if data != None:
            ads.write(self.AmsNetID,var,data)
            self.on_pushButton_loadgearbox_clicked()
        else:
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")
  
  
#======================================#    
#================常用功能===============#      
    @pyqtSignature("")
    def on_pushButton_enablesimu_clicked(self):
        """
        激活仿真器
        """
        try:

            simudic = {}
            simudic = self.ini.getSimuDic()
            
            for i in simudic:
                ads.write(self.AmsNetID,i,simudic[i])
                #print i,simudic[i]
            self.on_pushButton_ResetSaftyChain_clicked() 
            path =self.ini.getConfig('disableSClistDir') 
            txtname = self.ini.getConfig('disableSClist')   
            txtPath = path + txtname
            with open(txtPath , 'w') as f:
                f.write('')
            self.dialog_SChistory.update()

        except Exception,e:
            print e


    @pyqtSignature("")
    def on_pushButton_limitPower_clicked(self):
        option = "PowerLimitFromSCADA"
        var = self.ini.getVarValue(option)
        option = 'setLimitedPower'
        value = self.ini.getConfig(option)
        if self.versionType == 'NGP':
            limitdata = float(value)/float(self.ratedpower)       
        else:
            limitdata = int(value)
        data = ads.read(self.AmsNetID,var)
        print limitdata
        if data != None:
            if  not self.limitEnable:
                ads.write(self.AmsNetID,var,limitdata)
                self.limitEnable = True
                self.pushButton_limitPower.setText(u"SCADA限功率：开")
            else:
                if self.versionType == 'NGP':
                    data = 1
                else:
                    data = self.ratedpower
                ads.write(self.AmsNetID,var,data)
                self.pushButton_limitPower.setText(u"SCADA限功率：关")
                self.limitEnable = False
        else:
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")

#======================================#    
#================刹车功能===============#  
    @pyqtSignature("")
    def on_pushButton_bp50_clicked(self):
        
        try:
            activeScada = 'activeScada'
            scada =self.ini.getVarValue(activeScada)            
            ads.write(self.AmsNetID,scada,1)                  
            option = "BP_50"
            var = self.ini.getVarValue(option)  
            if self.versionType == 'NGP':
                ads.write(self.AmsNetID,var, 1)
                time.sleep(1.5)
                ads.write(self.AmsNetID,var, 0)
                bpAck = self.ini.getVarValue(option + 'ACK')
                data = ads.read(self.AmsNetID, bpAck)
                if data == 0:
                    self.on_pushButton_ResetSaftyChain_clicked()
            else:                
                data = read(self.AmsNetID,var)                     
                if data:
                    data = 0  
                else:
                    data = 1
                ads.write(self.AmsNetID,var, data) 
            self.pushButton_bp50.setText(option + ":"+str(data))
        except Exception,e:    
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")        

    @pyqtSignature("")
    def on_pushButton_bp51_clicked(self):
        try:
            activeScada = 'activeScada'
            scada =self.ini.getVarValue(activeScada)            
            ads.write(self.AmsNetID,scada,1)              
            option = "BP_51"
            var = self.ini.getVarValue(option)            
            if self.versionType == 'NGP':
                ads.write(self.AmsNetID,var, 1)
                time.sleep(1.5)
                ads.write(self.AmsNetID,var, 0)
                bpAck = self.ini.getVarValue(option + 'ACK')
                data = ads.read(self.AmsNetID, bpAck)
                if data == 0:
                    self.on_pushButton_ResetSaftyChain_clicked()
            else:                
                data = read(self.AmsNetID,var)                     
                if data:
                    data = 0  
                else:
                    data = 1
                ads.write(self.AmsNetID,var, data) 

            self.pushButton_bp51.setText(option + ":"+str(data))
        except Exception,e:    
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")
            

    @pyqtSignature("")
    def on_pushButton_bp100_clicked(self):       
        try:
            activeScada = 'activeScada'
            scada =self.ini.getVarValue(activeScada)            
            ads.write(self.AmsNetID,scada,1)                        
            option = "BP_100"
            var = self.ini.getVarValue(option)  
            if self.versionType == 'NGP':
                ads.write(self.AmsNetID,var, 1)
                time.sleep(1.5)
                ads.write(self.AmsNetID,var, 0)
                bpAck = self.ini.getVarValue(option + 'ACK')
                data = ads.read(self.AmsNetID, bpAck)
                if data == 0:
                    self.on_pushButton_ResetSaftyChain_clicked()
            else:                
                data = read(self.AmsNetID,var)                     
                if data:
                    data = 0  
                else:
                    data = 1
                ads.write(self.AmsNetID,var, data) 
            self.pushButton_bp100.setText(option + ":"+str(data))
        except Exception,e:    
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")
            
            
    @pyqtSignature("")
    def on_pushButton_bp150_clicked(self):        
        try:
            option = "BP_150"
            var = self.ini.getVarValue(option)            
            activeScada = 'activeScada'
            scada =self.ini.getVarValue(activeScada)            
            ads.write(self.AmsNetID,scada,1)            
            if self.versionType == 'NGP':
                ads.write(self.AmsNetID,var, 1)
                time.sleep(1.5)
                ads.write(self.AmsNetID,var, 0)
                bpAck = self.ini.getVarValue(option + 'ACK')
                data = ads.read(self.AmsNetID, bpAck)
                if data == 0:
                    self.on_pushButton_ResetSaftyChain_clicked()
            else:                
                data = read(self.AmsNetID,var)                     
                if data:
                    data = 0  
                else:
                    data = 1
                ads.write(self.AmsNetID,var, data) 
            bplevel = self.pushButton_bp150.text()
            self.pushButton_bp150.setText(bplevel[:6] + ":"+str(data))
        except Exception,e:    
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")
        

    
    @pyqtSignature("")
    def on_pushButton_bp199_clicked(self):
        try:
            option = "BP_199"
            activeScada = 'activeScada'
            scada =self.ini.getVarValue(activeScada)            
            ads.write(self.AmsNetID,scada,1)
            var = self.ini.getVarValue(option)  
            if self.versionType == 'NGP':
                ads.write(self.AmsNetID,var, 1)
                time.sleep(1.5)
                ads.write(self.AmsNetID,var, 0)
                bpAck = self.ini.getVarValue(option + 'ACK')
                data = ads.read(self.AmsNetID, bpAck)
                if data == 0:
                    self.on_pushButton_ResetSaftyChain_clicked()
            else:                
                data = read(self.AmsNetID,var)                     
                if data:
                    data = 0  
                else:
                    data = 1
                ads.write(self.AmsNetID,var, data) 
            bplevel = self.pushButton_bp199.text()
            self.pushButton_bp199.setText(bplevel[:6] + ":"+str(data))        
        except Exception,e:    
            QMessageBox.warning(self, 'WORNING', "Can not set the Value")
#======================================#    
#================SC配置===============#      


        
    @pyqtSignature("")
    def on_pushButton_loadSC_clicked(self):        
        
        try:
            var = str(self.lineEdit_SCcode.text()).strip().upper()
            if var == "":
                QMessageBox.warning(self, 'WORNING', u"请输入SC编号")     
                return 
            if var[0] != 'S':
                var = "SC" + var   
            self.sc = var
            self.lineEdit_SCcode.setText(self.sc)
            scgci = self.scGci%self.sc
            self.scID = str(ads.read(self.AmsNetID,scgci))
            self.lineEdit_SCid.setText(self.scID)
            rescResetType =  str(ads.read(self.AmsNetID,self.scResetType%self.scID))
            rescSetDelay = str(ads.read(self.AmsNetID,self.scSetDelay%self.scID))
            rescReSetDelay = str(ads.read(self.AmsNetID,self.scReSetDelay%self.scID))
            rescRepeatRate = str(ads.read(self.AmsNetID,self.scRepeatRate%self.scID))
            
            
            if self.versionType == 'NGP':
                if rescResetType == '1':
                    rescResetType = 'A'
                elif rescResetType == '0' :
                    rescResetType = 'M'
                disableScWord = u"启用SC："
                rescDisable = str(ads.read(self.AmsNetID,self.scDisable%self.scID))
            else:
                rescDisable = str(ads.read(self.AmsNetID,self.scDisable%self.sc))
                disableScWord = u"禁用SC："
            rescBplevel = str(ads.read(self.AmsNetID,self.scBplevel%self.scID))
            rescYplevel = str(ads.read(self.AmsNetID,self.scYplevel%self.scID))
            self.lineEdit_SCsetType.setText(rescResetType)
            self.lineEdit_SCsetdelay.setText(rescSetDelay)
            self.lineEdit_SCresetDelay.setText(rescReSetDelay)
            self.lineEdit_SCrepeatTimes.setText(rescRepeatRate)
            self.lineEdit_SCbplevel.setText(rescBplevel)
            self.lineEdit_SCyplevel.setText(rescYplevel)
            self.pushButton_disableSC.setText(disableScWord + rescDisable)
        except Exception,e:
            print e

    @pyqtSignature("")
    def on_pushButton_setSCdelay_clicked(self):
        try:
            scSetDelay = self.scSetDelay%self.scID
            data = str(self.lineEdit_SCsetdelay.text())
            ads.write(self.AmsNetID,scSetDelay,data)
            self.on_pushButton_loadSC_clicked()
            change = 'setSCdelay: '+ data
            self.scChangeList(self.sc, change)  
            self.dialog_SChistory.update()
        except Exception,e:
            print e
            
    @pyqtSignature("")
    def on_pushButton_disableSC_clicked(self):
        try:
            if self.versionType == 'NGP':
                disableScWord = u"启用SC："
                SCdisable = self.scDisable%self.scID
            else:
                disableScWord = u"禁用SC："
                SCdisable = self.scDisable%self.sc
            data = ads.read(self.AmsNetID,SCdisable)
            if data:
                data = '0'
            else:
                data = '1'
            ads.write(self.AmsNetID,SCdisable,data)
            if self.versionType == 'NGP':
                self.on_pushButton_ResetSaftyChain_clicked()
            self.pushButton_disableSC.setText(disableScWord + data)
            change = disableScWord + data
            self.scChangeList(self.sc, change)
            self.dialog_SChistory.update()
        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e))  

            
    @pyqtSignature("")        
    def on_pushButton_disableSClist_clicked(self):
        try:
            path =self.ini.getConfig('disableSClistDir') 
            txtname = self.ini.getConfig('disableSClist') 
            txtPath = path + txtname            
            if not os.path.isfile(txtPath): 
                f = open(txtPath,'w')
                f.close() 
            if  self.dialog_SChistory.isHidden() :
                self.dialog_SChistory.update()
                self.dialog_SChistory.activateWindow()
                self.dialog_SChistory.show()            
            else:
                self.dialog_SChistory.hide()
        
        except Exception,e:
            print e
                    
    @pyqtSignature("")
    def on_pushButton_setSCmode_clicked(self):
        try:
            scResetType = self.scResetType%self.scID
            data = str(self.lineEdit_SCsetType.text()).strip().upper()
            #NGP复位方式的字符位为 autoResetEnable 为1 则是自动复位 反之则为手动复位
            if self.versionType == 'NGP':
                if data == 'M':
                    rescResetType = '0'
                elif data == 'A' :
                    rescResetType = '1'            
            ads.write(self.AmsNetID,scResetType,data)
            self.on_pushButton_loadSC_clicked()
            change = 'SCmode: '+ data
            self.scChangeList(self.sc, change)       
            self.dialog_SChistory.update()
        except Exception,e:
            print e
    

    @pyqtSignature("")
    def on_pushButton_setSCredelay_clicked(self):
        try:
            scReSetDelay = self.scReSetDelay%self.scID
            data = str(self.lineEdit_SCresetDelay.text())
            ads.write(self.AmsNetID,scReSetDelay,data)
            self.on_pushButton_loadSC_clicked()
            change = 'setResetDelay: '+ data
            self.scChangeList(self.sc, change)       
            self.dialog_SChistory.update()
        except Exception,e:
            print e

    
    @pyqtSignature("")
    def on_pushButton_setSCrepeat_clicked(self):
        try:
            scRepeatRate = self.scRepeatRate%self.scID
            data = str(self.lineEdit_SCrepeatTimes.text())
            ads.write(self.AmsNetID,scRepeatRate,data)
            self.on_pushButton_loadSC_clicked()
            change = 'setSCrepeat: '+ data
            self.scChangeList(self.sc, change)    
            self.dialog_SChistory.update()
        except Exception,e:
            print e        
   
    @pyqtSignature("")
    def on_pushButton_setSCbplevel_clicked(self):
        try:
            scBplevel = self.scBplevel%self.scID
            data = str(self.lineEdit_SCbplevel.text())
            ads.write(self.AmsNetID,scBplevel,data)
            self.on_pushButton_loadSC_clicked()
            change = 'bplevel: '+ data
            self.scChangeList(self.sc, change)
            self.dialog_SChistory.update()
        except Exception,e:
            print e        
            
    @pyqtSignature("")
    def on_pushButton_setSCyplevel_clicked(self):
        try:
            scYplevel = self.scYplevel%self.scID
            data = str(self.lineEdit_SCyplevel.text())
            ads.write(self.AmsNetID,scYplevel,data)
            self.on_pushButton_loadSC_clicked()
            change = 'yplevel: '+ data
            self.scChangeList(self.sc, change)   
            self.dialog_SChistory.update()
        except Exception,e:
            print e            
  

    
    @pyqtSignature("")
    def on_pushButton_highwind_clicked(self):        
        try:
            if self.versionType != 'NGP':
                option = "BP_50"
                var = self.ini.getVarValue(option) 
                ads.write(self.AmsNetID,var, 1)    
                ads.write(self.AmsNetID,var, 0)          
            option1 = "simuWindSpeed_1"
            option2 = "simuWindSpeed_2"
            var1 = self.ini.getVarValue(option1)
            var2 = self.ini.getVarValue(option2)  
            data = self.ini.getConfig('highwind')  
            if data != None:
                ads.write(self.AmsNetID,var1,data)
                ads.write(self.AmsNetID,var2,data)
                self.on_pushButton_loadWindspeed_clicked()
            else:
                QMessageBox.warning(self, 'WORNING', "Can not read the WindSpeed")  

        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e))  
    
    @pyqtSignature("")
    def on_pushButton_highwindStop_clicked(self):        
        try:   
            
            option1 = "simuWindSpeed_1"
            option2 = "simuWindSpeed_2"
            var1 = self.ini.getVarValue(option1)
            var2 = self.ini.getVarValue(option2)  
            data = self.ini.getConfig('highwindstop')  
            if data != None:
                ads.write(self.AmsNetID,var1,data)
                ads.write(self.AmsNetID,var2,data)
            else:
                QMessageBox.warning(self, 'WORNING', "Can not read the WindSpeed")      
        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e))    
        
    @pyqtSignature("")
    def on_pushButton_lowwind_clicked(self):
        try:
            self.on_pushButton_ResetSaftyChain_clicked()
            if self.versionType != 'NGP':
                option = "BP_50"
                var = self.ini.getVarValue(option) 
                ads.write(self.AmsNetID,var, 1)    
                ads.write(self.AmsNetID,var, 0)    
            option1 = "simuWindSpeed_1"
            option2 = "simuWindSpeed_2"
            var1 = self.ini.getVarValue(option1)
            var2 = self.ini.getVarValue(option2)  
            data = self.ini.getConfig('lowwind')  
            if data != None:
                ads.write(self.AmsNetID,var1,data)
                ads.write(self.AmsNetID,var2,data)
                self.on_pushButton_loadWindspeed_clicked()
            else:
                QMessageBox.warning(self, 'WORNING', "Can not read the WindSpeed")  
        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e))  

    @pyqtSignature("")
    def on_pushButton_lowwindStop_clicked(self):        
        try:   
            
            option1 = "simuWindSpeed_1"
            option2 = "simuWindSpeed_2"
            var1 = self.ini.getVarValue(option1)
            var2 = self.ini.getVarValue(option2)  
            data = self.ini.getConfig('lowwindstop')  
            if data != None:
                ads.write(self.AmsNetID,var1,data)
                ads.write(self.AmsNetID,var2,data)
            else:
                QMessageBox.warning(self, 'WORNING', "Can not read the WindSpeed")          
        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e)) 
            
    def on_pushButton_traclogDone_clicked(self):        
        try:               
            option = "traceLoggerDone"
            var = self.ini.getVarValue(option)
            if var != None:
                data = str(ads.read(self.AmsNetID,var))
                self.pushButton_traclogDone.setText('Tracelog:' + data)   
        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e)) 

    
    @pyqtSignature("")
    def on_pushButton_ResetSaftyChain_clicked(self):
        try:
            option = "SafetyChain_RESET"
            var = self.ini.getVarValue(option) 
            ads.write(self.AmsNetID,var, 0)
            time.sleep(0.2)
            ads.write(self.AmsNetID,var, 1)
            if self.versionType == 'NGP':
                time.sleep(1.5)
            ads.write(self.AmsNetID,var, 0)          
        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e)) 
    
    @pyqtSignature("int")
    def on_checkBox_turbineOP_stateChanged(self):
        try:
            if self.checkBox_turbineOP.checkState():
                self.stateThread = threading.Thread(target = self.refreshTurbineOP)
                self.listening = True
                self.stateThread.setDaemon(1) 
                self.stateThread.start()
                print 'start the thread to listion the turbine operation'
                
            else:            
                print self.stateThread.isAlive()
                self.listening = False
                if self.stateThread.isAlive():
                    self.stateThread = None
                    print 'kill the thread to listion the turbine operation'
        except Exception,e:
            print e
            
    def refreshTurbineOP(self):
        while (self.listening):
            statelist = getstate.getState(self.AmsNetID,self.ini)
            self.label_power.setText(u'功率:'+ str(statelist[0]))
            self.label_genspeed.setText(u'转速:'+str(statelist[1]))
            self.label_windspeed.setText(u'风速:'+ str(statelist[2]))
            self.label_turbineOP.setText(u'风机状态:'+ str(statelist[3]))
            self.label_bplevel.setText(u'刹车等级:'+ str(statelist[4]))
            self.label_yplevel.setText(u'偏航等级:'+ str(statelist[5]))
            time.sleep(1)
        




    
    #======================================#    
    #=============数据记录工具==============#

    @pyqtSignature("")
    def on_pushButton_startRecorder_clicked(self):
        """
        Start Recorder
        """
        if not self.varlistchanged :  
            try:
                internal = int(self.lineEdit_ter_recorder.text())
                keeptime = int(self.lineEdit_long_recorder.text())*1000
                times = int(keeptime/internal)
                self.pushButton_stopRecorder.setEnabled(True)
                self.pushButton_startRecorder.setEnabled(False)
                self.recorderThread  = record.RecordThread("recorder",self.QIP,self.port,internal,times,self)                
                self.recorderThread.start()                
            except Exception,e:
                print e
                self.pushButton_startRecorder.setEnabled(True)
                       
    
    @pyqtSignature("")
    def on_pushButton_stopRecorder_clicked(self):
        """
        Stop Recorder
        """
        try:
            record.stopRecord()
            while self.recorderThread.isAlive():
                continue
            if not self.varlistchanged :
                self.pushButton_startRecorder.setEnabled(True) 
        except Exception,e:
            print e
            
    @pyqtSignature("")
    def on_textEdit_var_recorder_textChanged(self):
        #用于防止变量修改后不保存就开始启动录数据
        self.pushButton_startRecorder.setEnabled(False)
        self.varlistchanged = True

    
    @pyqtSignature("")
    def on_pushButton_savevar_clicked(self):
        newVarList = self.textEdit_var_recorder.toPlainText()
        if newVarList != "":
            try:
                if not os.path.exists(RECORDERPATH):
                    os.makedirs(RECORDERPATH)                   
                PATH = './DLL/ADS_VariableList.txt'            
                with open(PATH,'w') as f:
                    f.write(newVarList)
            except Exception,e:
                print e
        self.varlistchanged = False
        if self.connectState :                  
            self.pushButton_startRecorder.setEnabled(True)
            
    @pyqtSignature("")
    def on_pushButton_openFileDir_clicked(self):   

        if not os.path.exists(RECORDERPATH):
            os.makedirs(RECORDERPATH)        
        os.startfile(RECORDERPATH)
        
        
#批量读
    def readFunction(self,datain,dataout):
        try:  
            varname = datain.currentText()
            strVar = str(varname).strip()
            if strVar == '':
                dataout.setText('')  
                return 
            data = ads.read(self.AmsNetID,strVar)
            datatype = ads.getType(self.AmsNetID,strVar)
            if data == None: 
                strVar = "."+strVar
                data = ads.read(self.AmsNetID,strVar)
                if data ==None:
                    word =  "Can not connet the varlue: "+strVar   
                    QMessageBox.warning(self, 'WORNING', str(word))                     
                    return 
            if strVar in self.batchVarList:
                self.batchVarList.remove(strVar)
                net = datain.findText(strVar)                    
                datain.removeItem(net)   
            datain.insertItem(-1,strVar)
            datain.setCurrentIndex(0)    
            self.batchVarList.insert(0,strVar)
            dataout.setText(str(data))
            dataout.setFocus()
            connect.saveBatchCombox(self.batchVarList)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))     

    def writeFunction(self,lineedit_var,lineedit_data):
        try:
            strVar =  str(lineedit_var.currentText()).strip()
            if strVar == '':
                return 0
            data = str(lineedit_data.text())
            ads.write(self.AmsNetID,strVar,data)  
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))       
            
    @pyqtSignature("")
    def on_pushButton_batchRead1_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar1,self.lineEdit_batchValue_1)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))  
            
    @pyqtSignature("")
    def on_pushButton_batchRead2_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar2,self.lineEdit_batchValue_2)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e)) 
            
            
    @pyqtSignature("")
    def on_pushButton_batchRead3_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar3,self.lineEdit_batchValue_3)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))   
            
    @pyqtSignature("")
    def on_pushButton_batchRead4_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar4,self.lineEdit_batchValue_4)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))        
           
    @pyqtSignature("")
    def on_pushButton_batchRead5_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar5,self.lineEdit_batchValue_5)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()             
            QMessageBox.warning(self, 'WORNING', str(e)) 
            
    @pyqtSignature("")
    def on_pushButton_batchRead6_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar6,self.lineEdit_batchValue_6)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e)) 
            
    @pyqtSignature("")
    def on_pushButton_batchRead7_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar7,self.lineEdit_batchValue_7)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e)) 
            
    @pyqtSignature("")
    def on_pushButton_batchRead8_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar8,self.lineEdit_batchValue_8)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))         
            
    @pyqtSignature("")
    def on_pushButton_batchRead9_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar9,self.lineEdit_batchValue_9)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))   
            
    @pyqtSignature("")
    def on_pushButton_batchRead10_clicked(self):        
        try:
            self.readFunction(self.comboBox_batchVar10,self.lineEdit_batchValue_10)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))       
            
    @pyqtSignature("")
    def on_pushButton_batchRead11_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar11,self.lineEdit_batchValue_11)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e)) 
            
    @pyqtSignature("")
    def on_pushButton_batchRead12_clicked(self):
        try:
            self.readFunction(self.comboBox_batchVar12,self.lineEdit_batchValue_12)            
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))     
            
    @pyqtSignature("")
    def on_pushButton_batchWrite1_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar1,self.lineEdit_batchValue_1) 
            self.on_pushButton_batchRead1_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable()            
            QMessageBox.warning(self, 'WORNING', str(e))     

    @pyqtSignature("")
    def on_pushButton_batchWrite2_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar2,self.lineEdit_batchValue_2)
            self.on_pushButton_batchRead2_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite3_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar3,self.lineEdit_batchValue_3)
            self.on_pushButton_batchRead3_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite4_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar4,self.lineEdit_batchValue_4)
            self.on_pushButton_batchRead4_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite5_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar5,self.lineEdit_batchValue_5)
            self.on_pushButton_batchRead5_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite6_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar6,self.lineEdit_batchValue_6)
            self.on_pushButton_batchRead6_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite7_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar7,self.lineEdit_batchValue_7)
            self.on_pushButton_batchRead7_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite8_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar8,self.lineEdit_batchValue_8)
            self.on_pushButton_batchRead8_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite9_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar9,self.lineEdit_batchValue_9)
            self.on_pushButton_batchRead9_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite10_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar10,self.lineEdit_batchValue_10)
            self.on_pushButton_batchRead10_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite11_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar11,self.lineEdit_batchValue_11)
            self.on_pushButton_batchRead11_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
            
    @pyqtSignature("")
    def on_pushButton_batchWrite12_clicked(self):
        try:
            self.writeFunction(self.comboBox_batchVar12,self.lineEdit_batchValue_12)
            self.on_pushButton_batchRead12_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 

    @pyqtSignature("")
    def on_pushButton_batchWriteAll_clicked(self):
        try:
            self.on_pushButton_batchWrite1_clicked()
            self.on_pushButton_batchWrite2_clicked()
            self.on_pushButton_batchWrite3_clicked()
            self.on_pushButton_batchWrite4_clicked()
            self.on_pushButton_batchWrite5_clicked()
            self.on_pushButton_batchWrite6_clicked()
            self.on_pushButton_batchWrite7_clicked()
            self.on_pushButton_batchWrite8_clicked()
            self.on_pushButton_batchWrite9_clicked()
            self.on_pushButton_batchWrite10_clicked()
            self.on_pushButton_batchWrite11_clicked()
            self.on_pushButton_batchWrite12_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable() 
    
    @pyqtSignature("")
    def on_pushButton_batchReadAll_clicked(self):
        try:
            self.on_pushButton_batchRead1_clicked()
            self.on_pushButton_batchRead2_clicked()
            self.on_pushButton_batchRead3_clicked()
            self.on_pushButton_batchRead4_clicked()
            self.on_pushButton_batchRead5_clicked()
            self.on_pushButton_batchRead6_clicked()
            self.on_pushButton_batchRead7_clicked()
            self.on_pushButton_batchRead8_clicked()
            self.on_pushButton_batchRead9_clicked()
            self.on_pushButton_batchRead10_clicked()
            self.on_pushButton_batchRead11_clicked()
            self.on_pushButton_batchRead12_clicked()
        except Exception,e:
            self.connectState = False
            self.updateEnable()             
            
    @pyqtSignature("")
    def on_pushButton_batchConnect_clicked(self):
        self.on_pushButton_adsConnect_clicked()

    @pyqtSignature("")
    def on_pushButton_batchWrite_clicked(self):
        datalist = []
        try:
            errdatalist = []
            self.label_finished.setText("")
            data = str(self.textEdit_var_batchWrite.toPlainText()).strip()
            if data == '':
                self.label_finished.setText(u"请按照格式输入变量列表")
                return 
            linelist = data.split('\n')
            for line in linelist:
                line = line.strip()
                if line != '':            
                    datalist = line.split('=')            
                    ads.write(self.AmsNetID,datalist[0],datalist[1])
                    data = ads.read(self.AmsNetID,datalist[0])  
                    datatype = type(data)
                    if data - datatype(datalist[1]) > 0.01:
                        errdatalist.append(datalist[0])
            if len(errdatalist) > 0:
                data = ','.join(errdatalist) + ' can not write!'
                QMessageBox.warning(self, 'WORNING', data) 
            else:
                self.label_finished.setText("Done")
        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e)) 
            
    @pyqtSignature("")
    def on_pushButton_batchCheck_clicked(self):        
        dataArray = []
        wrongdata = False
        try:
            self.label_finished.setText("")
            data = str(self.textEdit_var_batchWrite.toPlainText()).strip()
            if data == '':
                self.label_finished.setText(u"请按照格式输入变量列表")
                self.batchVarListChanged = True
                return
            self.textEdit_var_batchWrite.clear()
            linelist = data.split('\n')
            for line in linelist:
                line = line.replace("#####",'').strip()
                datalist = []
                if line != '':            
                    datalist = line.split('=')
                    var = datalist[0].strip()
                    if ads.read(self.AmsNetID,var) == None or len(datalist) < 2:
                        line = '#####' + line +'#####'
                        self.textEdit_var_batchWrite.append(line)   
                        wrongdata = True
                    else:
                        line =  datalist[0].strip() + ' ' + '=' + " " +datalist[1].strip() 
                        self.textEdit_var_batchWrite.append(line)   
                        self.textEdit_var_batchWrite.wordWrapMode()
            if wrongdata:
                self.label_finished.setText(u"请按照格式输入变量列表")
                self.batchVarListChanged = True
            else:
                self.label_finished.setText(u"已检查")
                self.batchVarListChanged = False            
            self.updateEnable()
        except Exception,e:
            QMessageBox.warning(self, 'WORNING', str(e)) 
    
    @pyqtSignature("")
    def on_textEdit_var_batchWrite_textChanged(self):
        self.label_finished.setText(u"变量已改变")
        self.batchVarListChanged = True
        self.updateEnable()   
    
    @pyqtSignature("")
    def on_pushButton_batchClean_clicked(self):   
        self.textEdit_var_batchWrite.clear()
        ip = "172.16.43.189.1.1:801"
        a = read(ip,'.gsControlCodeBuildNo')
        print a
        
    #用于批量使能按键激活
    def updateEnable(self):
        if self.connectState:
            self.pushButton_adsConnect.setText('DisConnect')
            self.pushButton_batchConnect.setText('DisConnect')

        else:
            self.pushButton_adsConnect.setText('Connect')
            self.pushButton_batchConnect.setText('Connect')
        self.comboBox_version.setEnabled(not self.connectState)
        self.comboBox_name.setEnabled(self.connectState)
        self.lineEdit_set.setEnabled(self.connectState)
        self.comboBox_ip.setEnabled(not self.connectState)
        self.pushButton_loadRadius.setEnabled(self.connectState)
        self.pushButton_loadgearbox.setEnabled(self.connectState)
        self.pushButton_setRadius.setEnabled(self.connectState)
        self.pushButton_enableGearbox.setEnabled(self.connectState)
        self.pushButton_disableGearbox.setEnabled(self.connectState)
        self.pushButton_loadWindspeed.setEnabled(self.connectState)
        self.pushButton_resetScada.setEnabled(self.connectState)
        self.pushButton_setWindspeed.setEnabled(self.connectState)
        self.pushButton_loadScada.setEnabled(self.connectState)
        self.pushButton_setScada.setEnabled(self.connectState)
        self.pushButton_adsLoad.setEnabled(self.connectState)
        self.pushButton_adsTrigger.setEnabled(self.connectState)
        self.pushButton_adsWrite.setEnabled(self.connectState)
        self.pushButton_disableSC.setEnabled(self.connectState)
        self.pushButton_disableSClist.setEnabled(self.connectState)
        self.pushButton_loadSC.setEnabled(self.connectState)
        self.pushButton_setSCmode.setEnabled(self.connectState)
        self.pushButton_setSCdelay.setEnabled(self.connectState)
        self.pushButton_setSCredelay.setEnabled(self.connectState)
        self.pushButton_setSCrepeat.setEnabled(self.connectState)
        self.pushButton_bp150.setEnabled(self.connectState)
        self.pushButton_bp50.setEnabled(self.connectState)
        self.pushButton_bp100.setEnabled(self.connectState)
        self.pushButton_enablesimu.setEnabled(self.connectState)
        self.pushButton_bp199.setEnabled(self.connectState)
        self.pushButton_bp51.setEnabled(self.connectState)
        self.pushButton_limitPower.setEnabled(self.connectState)
        self.pushButton_highwind.setEnabled(self.connectState)
        self.pushButton_highwindStop.setEnabled(self.connectState)
        self.pushButton_lowwind.setEnabled(self.connectState)
        self.pushButton_lowwindStop.setEnabled(self.connectState)
        self.pushButton_startRecorder.setEnabled(self.connectState)
        self.pushButton_stopRecorder.setEnabled(self.connectState)
        self.pushButton_ResetSaftyChain.setEnabled(self.connectState)
        self.checkBox_turbineOP.setEnabled(self.connectState)    
        self.pushButton_SClist.setEnabled(self.connectState)
        self.pushButton_setSCbplevel.setEnabled(self.connectState)
        self.pushButton_setSCyplevel.setEnabled(self.connectState)
        self.pushButton_startRecorder.setEnabled(self.connectState and not self.varlistchanged)
        self.pushButton_batchRead1.setEnabled(self.connectState)
        self.pushButton_batchRead2.setEnabled(self.connectState)
        self.pushButton_batchRead3.setEnabled(self.connectState)
        self.pushButton_batchRead4.setEnabled(self.connectState)
        self.pushButton_batchRead5.setEnabled(self.connectState)
        self.pushButton_batchRead6.setEnabled(self.connectState)
        self.pushButton_batchRead7.setEnabled(self.connectState)
        self.pushButton_batchRead8.setEnabled(self.connectState)
        self.pushButton_batchRead9.setEnabled(self.connectState)
        self.pushButton_batchRead10.setEnabled(self.connectState)
        self.pushButton_batchRead11.setEnabled(self.connectState)
        self.pushButton_batchRead12.setEnabled(self.connectState)
        self.pushButton_batchReadAll.setEnabled(self.connectState)

        self.pushButton_batchWrite1.setEnabled(self.connectState)
        self.pushButton_batchWrite2.setEnabled(self.connectState)
        self.pushButton_batchWrite3.setEnabled(self.connectState)
        self.pushButton_batchWrite4.setEnabled(self.connectState)
        self.pushButton_batchWrite5.setEnabled(self.connectState)
        self.pushButton_batchWrite6.setEnabled(self.connectState)
        self.pushButton_batchWrite7.setEnabled(self.connectState)
        self.pushButton_batchWrite8.setEnabled(self.connectState)
        self.pushButton_batchWrite9.setEnabled(self.connectState)
        self.pushButton_batchWrite10.setEnabled(self.connectState)
        self.pushButton_batchWrite11.setEnabled(self.connectState)
        self.pushButton_batchWrite12.setEnabled(self.connectState)
        self.pushButton_batchWriteAll.setEnabled(self.connectState)
        self.pushButton_batchWrite.setEnabled(self.connectState and not self.batchVarListChanged)
        if self.versionType == 'GEN':
            self.pushButton_traclogDone.setEnabled(self.connectState)
        else:
            self.pushButton_traclogDone.setEnabled(False)
            
    #获取SC属性变量
    def  getSCvar(self):
        self.scGci =  str(self.ini.getVarValue('scGci')) 
        self.scResetType = str(self.ini.getVarValue('scResetType'))
        self.scSetDelay = str(self.ini.getVarValue('scSetDelay'))
        self.scReSetDelay = str(self.ini.getVarValue('scReSetDelay'))
        self.scRepeatRate = str(self.ini.getVarValue('scRepeatRate'))
        self.scBplevel = str(self.ini.getVarValue('scBplevel'))
        self.scDisable = str(self.ini.getVarValue('scDisable'))
        self.scYplevel = str(self.ini.getVarValue('scYplevel'))            
        
     #记录sc属性修改
    def scChangeList(self,sc,change):
        ISOTIMEFORMAT='%Y-%m-%d %X'
        path =self.ini.getConfig('disableSClistDir') 
        txtname = self.ini.getConfig('disableSClist')   
        txtPath = path + txtname
        datetime = time.strftime( ISOTIMEFORMAT, time.localtime() )
        data  = datetime + '\t' + sc + '\t' + change + '\n'
        with open(txtPath,'a') as f:
            f.write(data)
            
if __name__=="__main__":
    try:
        app=QApplication(sys.argv) 
        testwin=O2Tool()
        testwin.show()
        sys.exit(app.exec_())
        
    except Exception,e:
        print e
    
