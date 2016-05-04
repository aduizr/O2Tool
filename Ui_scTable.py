# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MainControl_QA\TestDevelopment\O2T\scTable.ui'
#
# Created: Mon Aug 10 17:45:30 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import time
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SCstate(object):
    def setupUi(self, SCstate):
        SCstate.setObjectName(_fromUtf8("SCstate"))
        SCstate.resize(480, 799)
        SCstate.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)        
        self.table_SC = QtGui.QTableWidget(SCstate)
        self.table_SC.setGeometry(QtCore.QRect(0, 20, 440, 501))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_SC.sizePolicy().hasHeightForWidth())
        self.table_SC.setSizePolicy(sizePolicy)
        self.table_SC.setMinimumSize(QtCore.QSize(485,480))
        self.table_SC.setMaximumSize(QtCore.QSize(0, 751))
        self.table_SC.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_SC.setRowCount(36)
        self.table_SC.setObjectName(_fromUtf8("table_SC"))
        self.table_SC.setColumnCount(5)
        item = QtGui.QTableWidgetItem()
        self.table_SC.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_SC.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_SC.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.table_SC.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.table_SC.setHorizontalHeaderItem(4, item)
        self.table_SC.horizontalHeader().setVisible(True)
        self.table_SC.horizontalHeader().setCascadingSectionResizes(True)
        self.table_SC.verticalHeader().setVisible(False)
        self.table_SC.verticalHeader().setCascadingSectionResizes(False)
        self.table_SC.verticalHeader().setDefaultSectionSize(20)
        self.table_SC.verticalHeader().setSortIndicatorShown(False)
        self.table_SC.verticalHeader().setStretchLastSection(False)
        self.table_SC.setColumnWidth(0,80)
        self.table_SC.setColumnWidth(1,220)
        self.table_SC.setColumnWidth(2,50)
        self.table_SC.setColumnWidth(3,50)
        self.table_SC.setColumnWidth(4,60)        
        self.retranslateUi(SCstate)
        QtCore.QMetaObject.connectSlotsByName(SCstate)

    def retranslateUi(self, SCstate):
        
        item = self.table_SC.horizontalHeaderItem(0)
        item.setText(_translate("SCstate", "编号", None))
        item = self.table_SC.horizontalHeaderItem(1)
        item.setText(_translate("SCstate", "SC", None))
        item = self.table_SC.horizontalHeaderItem(2)
        item.setText(_translate("SCstate", "刹车", None))
        item = self.table_SC.horizontalHeaderItem(3)
        item.setText(_translate("SCstate", "偏航", None))
        item = self.table_SC.horizontalHeaderItem(4)
        item.setText(_translate("SCstate", "复位方式", None))


if __name__ == "__main__":
    import sys
    print time.strptime
    
    #app = QtGui.QApplication(sys.argv)
    #SCstate = QtGui.QDockWidget()
    #ui = Ui_SCstate()
    #ui.setupUi(SCstate)
    #SCstate.show()
    #sys.exit(app.exec_())

