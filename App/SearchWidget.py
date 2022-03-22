from PyQt5.QtWidgets import *
import sys
import ErrorDialog
from LuceneDemo.Indexer_Searcher import Searcher
from org.apache.lucene.index import IndexNotFoundException
class SearchWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.title = '查找'
        # self.left = 0
        # self.top = 0
        # self.width = 300
        # self.height = 200

        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        # self.createTable()
        self.tableWidget = QTableWidget()

        # Row count
        # self.tableWidget.setRowCount(4)
        #
        # # Column count
        # self.tableWidget.setColumnCount(2)



        self.searchBtn=QPushButton()
        self.searchBtn.setText("搜索")
        self.searchBtn.setMinimumSize(200,50)
        self.searchBtn.clicked.connect(self.SearchProcess)

        self.textEdit=QLineEdit()
        self.textEdit.setMaximumSize(1000,50)

        self.keywordLable=QLabel()
        self.keywordLable.setText("输入关键字:")

        self.indexLable=QLabel()
        self.indexLable.setText("当前索引文件:")

        self.currentIndex=QLineEdit()
        self.currentIndex.setText("")
        self.currentIndex.setMaximumSize(1000,50)

        self.chooseIndexBtn=QPushButton()
        self.chooseIndexBtn.setText("选择索引文件")
        self.chooseIndexBtn.setMinimumSize(200,50)
        self.chooseIndexBtn.clicked.connect(self.ChooseIndex)

        secondLayout = QHBoxLayout()


        thirdLayout=QFormLayout()
        thirdLayout.setContentsMargins(0,0,0,0)

        thirdLayout.addRow(self.keywordLable,self.textEdit)
        thirdLayout.addRow(self.indexLable,self.currentIndex)

        thirdLayout1=QVBoxLayout()
        thirdLayout1.setContentsMargins(0, 0, 0, 0)

        thirdLayout1.addWidget(self.searchBtn)
        thirdLayout1.addWidget(self.chooseIndexBtn)

        secondLayout.addLayout(thirdLayout1)
        secondLayout.addLayout(thirdLayout)
        secondLayout.setContentsMargins(0,0,0,0)

        # 整体布局
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.layout.addLayout(secondLayout)
        self.layout.setContentsMargins(10,10,10,10)
        self.setLayout(self.layout)

        self.indexPath=""


    def ChooseIndex(self):
        """
        选择要查找的索引文件
        :return:
        """
        self.indexPath = QFileDialog.getExistingDirectory(self, "选择索引文件夹")
        self.currentIndex.setText(self.indexPath)

    def SearchProcess(self):
        """
        在索引中查找并将结果返回
        :return:
        """
        if(self.indexPath==""):
            dia=ErrorDialog.ErrorDialog("没有选择索引路径！")
            dia.exec_()
            return

        searcher=Searcher()
        if(self.textEdit.text()==""):
            dia = ErrorDialog.ErrorDialog("关键词不能为空！")
            dia.exec_()
            return

        res,field,flag = searcher.NormalSearch(self.indexPath, self.textEdit.text())
        if(flag==0):
            # 查找成功
            self.tableWidget.setRowCount(len(res))
            self.tableWidget.setColumnCount(len(field))
            for col,f in enumerate(field):
                self.tableWidget.setItem(0, col, QTableWidgetItem(f))
            for i,item in enumerate(res):
                for j,subItem in enumerate(item):
                    self.tableWidget.setItem(i+1,j,QTableWidgetItem(subItem))
        elif(flag==1):
            # 索引文件错误
            dia = ErrorDialog.ErrorDialog("请选择有效的索引文件夹！")
            dia.exec_()

        else:
            # 没有找到
            dia = ErrorDialog.ErrorDialog("没有找到相关结果")
            dia.exec_()


# if __name__ == '__main__':
#     #初始化日志
#     # logging.config.fileConfig('./log.conf')
#
#     app=QApplication(sys.argv)
#     demo=SearchWidget()
#     demo.resize(800,600)
#     demo.show()
#     try:
#         sys.exit(app.exec_())
#     except SystemExit:
#         pass