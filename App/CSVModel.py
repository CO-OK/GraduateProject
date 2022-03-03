import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication,QTableView
from PyQt5.QtCore import QAbstractTableModel,Qt

#用于展示csv文件
class CsvModel(QAbstractTableModel):
    def __init__(self,data):
        """

        :param data:要进行处理的数据
        """
        QAbstractTableModel.__init__(self)
        self._data=data

    def rowCount(self,parent=None):
        """
        获得数据表行数
        :return:行数
        这个函数是QAbstractTableModel里的抽象函数，必须被overwrite
        """
        return  self._data.shape[0]
    def columnCount(self,parent=None):
        """
        获数据表列数
        :return: 列数
        这个函数是QAbstractTableModel里的抽象函数，必须被overwrite
        """
        return  self._data.shape[1]
    def data(self,index,role=Qt.DisplayRole):
        """

        :param index:
        :param role:
        :return:

        """
        if(index.isValid()):
            if(role==Qt.DisplayRole):
                return str(self._data.iloc[index.row(),index.column()])
        return None
    def HeaderData(self,col,orientation,role):
        """

        :param col:
        :param orientation:
        :param role:
        :return:
        """
        if(orientation==Qt.Horizontal and role==Qt.DisplayRole):
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    df = pd.read_csv('../Data/Res.csv')
    app = QApplication(sys.argv)
    csv = CsvModel(df)
    view = QTableView()
    view.setModel(csv)
    view.resizeColumnsToContents()
    view.resizeRowsToContents()
    #view.resize(1920,1080)
    view.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("close window")