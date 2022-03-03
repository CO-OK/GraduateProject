import  sys
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QAction,QTextBrowser,QMenuBar,QFileSystemModel,QVBoxLayout,QFileDialog
from PyQt5 import uic
from docx import Document

class AppDemo(QWidget):
    def __init__(self):
        super(AppDemo, self).__init__()
        self.setWindowTitle("SmartAss")

        self.fileSystem=QFileSystemModel()
        self.fileSystem.setRootPath("/")


        #工具栏
        self.menuBar=QMenuBar(self)
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

        #textbrowser
        textBrowser=QTextBrowser(self)
        self.MainTextBrowser=textBrowser
        self.MainTextBrowser.setGeometry(0,25,300,995)


        #布局
        layout=QVBoxLayout()
        layout.addWidget(self.menuBar)
        layout.addWidget(self.MainTextBrowser)
        self.setLayout(layout)



    def OpenFile(self,path):
        """
        :param path: 文件路径
        :return: 目前只返回文本格式
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        text=""
        try:#这个是文本文件的情况
            with open(str(fileName), "r") as f:
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
    demo.resize(1920,1080)
    demo.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("close window")