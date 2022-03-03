import  sys
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QAction
from  PyQt5 import uic
from docx import Document

class AppDemo(QMainWindow):
    def __init__(self):
        super(AppDemo, self).__init__()
        uic.loadUi('Demo.ui',self)

        self.MainBtn.clicked.connect(self.printValue)

        #工具栏
        self.menuBar=self.menuBar()
        fileMenu=self.menuBar.addMenu('文件')

        #退出动作
        exit_action=QAction('退出',self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(lambda:QApplication.quit())

        #选择要处理的文件
        select_action=QAction('打开...',self)
        select_action.setShortcut('O')
        select_action.triggered.connect(lambda:self.OpenFile("../Data/安监总管三〔2013〕88号.docx"))

        fileMenu.addAction(select_action)
        fileMenu.addAction(exit_action)

    def OpenFile(self,path):
        """

        :param path: 文件路径
        :return: 目前只返回文本格式
        """
        text=""
        try:#这个是文本文件的情况
            with open(path, "r") as f:
                text=f.read()
        except UnicodeDecodeError:#目前只能处理docx文件
            document = Document(path)
            for para in document.paragraphs:
                text+=para.text+"\n"
        self.MainTextBrowser.clear()
        self.MainTextBrowser.append(text)


    def printValue(self):
        print("nb")


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=AppDemo()
    demo.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("close window")