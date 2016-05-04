# -*- coding: utf-8 -*-

"""
Module implementing SCstate.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time,threading
from Ui_scHistory import Ui_SChistory
from FUC import config
import sys
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)
    
if sys.getdefaultencoding() != 'gbk':
    print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding('gbk')

class SChistory(QDialog, Ui_SChistory):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        #self.setMinimumSize(QSize(485,100))
        self.ip = ""
        self.listening = False
        self.version = ""
        #self.getSClist()
    
    def update(self):
        self.table_SC.clearContents()
        self.getSClist()

    def getSClist(self):
        try:
            sclist = []
            scarray = []
            conf = config.Config()
            path = conf.getConfig('disableSClistDir') 
            txtname = conf.getConfig('disableSClist')   
            txtPath = path + txtname            
            with open(txtPath, 'r') as f:
                for line in f.readlines():
                    if line == '':
                        break
                    datalist =line.split('\t')
                    scarray.append(datalist)
            if scarray != []:
                self.table_SC.clearContents()
                i = 0
                scarray.reverse()
                for sclist in scarray:
                    self.table_SC.setItem(i,0, QTableWidgetItem(sclist[0]))
                    self.table_SC.setItem(i,1, QTableWidgetItem(sclist[1]))
                    self.table_SC.setItem(i,2, QTableWidgetItem(unicode(sclist[2],'gbk')))          
                    i += 1               
        except Exception,e:
            self.table_SC.clearContents()
            print e
            
    @pyqtSignature("QModelIndex")
    def on_table_SC_doubleClicked(self, index):
        try:
            row = self.table_SC.currentRow()        
            item = self.table_SC.item(row,1)  
            if item != None:
                self.emit(SIGNAL('output(QString)'),item.text())
        except Exception,e:
            print e    

if __name__=="__main__":
    try:
        import sys
        app=QApplication(sys.argv) 
        testwin=SChistory()
        testwin.show()
        sys.exit(app.exec_())
        
    except Exception,e:
        print e
    
