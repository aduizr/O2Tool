# -*- coding: utf-8 -*-

"""
Module implementing SCstate.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time,threading
from Ui_scTable import Ui_SCstate
from FUC.scListShow import SCshow
import sys
reload(sys)   
sys.setdefaultencoding('gbk') 


try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class SCstate(QDockWidget, Ui_SCstate):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.setMinimumSize(QSize(485,480))
        self.ip = ""
        self.listening = False
        self.version = ""
        self.scShowThread = SCshow()
        self.scShowThread.sinOut1.connect(self.showSClist)
        self.scShowThread.sinOut2.connect(self.disConn)

       
    def getip(self,ip,version):
        self.ip = ip
        self.version = version
        
    def startThread(self):
        self.listening = True
        try:
            self.scShowThread.update(self.ip, self.version)
            self.setWindowTitle(_translate("SCstate", "SC-list Connected...", None))
        except Exception,e:
            print e
            
    def disConn(self):
        QMessageBox.warning(self, 'WORNING', u'断开连接，请确认网络及PLC状态.')
        
    def stopThread(self):
        try:
            if self.listening:
                self.listening = False        
                if self.scShowThread.listening:
                    self.scShowThread.stop()       
                    print 'kill the thread to listion the SC'  
        except Exception,e:
            print e

            
    @pyqtSignature("QModelIndex")
    def on_table_SC_doubleClicked(self, index):
        try:
            row = self.table_SC.currentRow()        
            item = self.table_SC.item(row,0)  
            if item != None:
                self.emit(SIGNAL('output(QString)'),item.text())
        except Exception,e:
            print e

    def showSClist(self,scarray):
        try:
            self.table_SC.clearContents()
            if scarray != []:                
                try:
                    for i,sclist in enumerate(scarray):
                        self.table_SC.setItem(i,0, QTableWidgetItem(sclist[3]))
                        self.table_SC.setItem(i,4, QTableWidgetItem(sclist[1]))
                        self.table_SC.setItem(i,3, QTableWidgetItem(sclist[2]))
                        self.table_SC.setItem(i,2, QTableWidgetItem(sclist[0]))
                        self.table_SC.setItem(i,1, QTableWidgetItem(sclist[4]))               
                    oldlist = scarray
                    scarray = []
                except Exception,e:
                    print e
            else:   
                self.setWindowTitle(_translate("SCstate", "SC-list NO Connection...", None))
                self.disConn()
      
        except Exception,e:
            self.table_SC.clearContents()
            self.setWindowTitle(_translate("SCstate", "SC-list NO Connection...", None))
            self.disConn()
            print e

        
    def closeEvent(self,event):
        print "close sctable"
        try:
            if self.listening:
                self.stopThread()
                self.emit(SIGNAL('output(int)'),0)
        except Exception,e:
            print e
        
