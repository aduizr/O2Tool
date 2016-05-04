# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MainControl_QA\TestDevelopment\O2T\scTable.ui'
#
# Created: Mon Aug 10 17:45:30 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_SChistory(object):
    def setupUi(self, SChistory):
        SChistory.setObjectName(_fromUtf8("SChistory"))
        SChistory.resize(490, 180)
        #SChistory.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)   

        self.table_SC = QtGui.QTableWidget(SChistory)
        self.table_SC.setGeometry(QtCore.QRect(0, 0, 490, 180))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.table_SC.sizePolicy().hasHeightForWidth())
        self.table_SC.setSizePolicy(sizePolicy)
        self.table_SC.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_SC.setRowCount(35)
        self.table_SC.setObjectName(_fromUtf8("table_SC"))
        self.table_SC.setColumnCount(3)
        item = QtGui.QTableWidgetItem()
        self.table_SC.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_SC.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_SC.setHorizontalHeaderItem(2, item)
        self.table_SC.horizontalHeader().setVisible(True)
        self.table_SC.horizontalHeader().setCascadingSectionResizes(True)
        self.table_SC.verticalHeader().setVisible(True)
        self.table_SC.verticalHeader().setCascadingSectionResizes(False)
        self.table_SC.verticalHeader().setDefaultSectionSize(20)
        self.table_SC.verticalHeader().setSortIndicatorShown(False)
        self.table_SC.verticalHeader().setStretchLastSection(False)
        self.table_SC.setColumnWidth(0,150)
        self.table_SC.setColumnWidth(1,115)
        self.table_SC.setColumnWidth(2,180)   
        self.retranslateUi(SChistory)
        QtCore.QMetaObject.connectSlotsByName(SChistory)

    def retranslateUi(self, SChistory):       

        item = self.table_SC.horizontalHeaderItem(0)
        item.setText(_translate("SChistory", "操作时间", None))
        item = self.table_SC.horizontalHeaderItem(1)
        item.setText(_translate("SChistory", "SC", None))
        item = self.table_SC.horizontalHeaderItem(2)
        item.setText(_translate("SChistory", "动作", None))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SChistory = QtGui.QDockWidget()
    ui = Ui_SChistory()
    ui.setupUi(SChistory)
    SChistory.show()
    sys.exit(app.exec_())

