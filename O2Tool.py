# -*- coding: utf-8 -*-
import O2T
from PyQt4.QtGui import   * #QDialog, QApplication, QMainWindow, 
from PyQt4.QtCore import *  #pyqtSignature
import sys
import ctypes
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    try:
        app=QApplication(sys.argv) 
        testwin=O2T.O2Tool()
        testwin.show()
        sys.exit(app.exec_())
        
    except Exception,e:
        print e    
        
if __name__=="__main__":
    main()
    
