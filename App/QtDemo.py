import sys
import logging
import logging.config
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QAction,QTextBrowser,QMenuBar,QFileSystemModel,QGridLayout,QFileDialog,QVBoxLayout,QSpacerItem
from PyQt5.QtWidgets import QLabel,QHBoxLayout,QPushButton,QCheckBox,QSpinBox,QSizePolicy
from docx import Document
from docx.opc import exceptions
from TextBrowser import TextBrowser
from ErrorDialog import ErrorDialog

logger = logging.getLogger('logger')


class AppDemo(QWidget):
    def __init__(self):
        super(AppDemo, self).__init__()

        logger.info("initilize application")
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
        select_action.triggered.connect(lambda:self.OpenFile())

        fileMenu.addAction(select_action)
        fileMenu.addAction(exit_action)

        #textbrowser
        textBrowser=TextBrowser(self)
        self.MainTextBrowser=textBrowser
        self.MainTextBrowser.setGeometry(0,25,300,995)

        #labels
        keywordsLabel=QLabel(self)
        fileNameLabel=QLabel(self)
        numSectionsLabel=QLabel(self)

        keywordsLabel.setText("关键词:")
        fileNameLabel.setText("文档名:")
        numSectionsLabel.setText("章节数:")

        self.keywordsLabel=keywordsLabel
        self.fileNameLabel=fileNameLabel
        self.numSectionsLabel=numSectionsLabel

        #与上面labels对应的text browser

        self.keywordsBrowser=QTextBrowser(self)
        self.fileNameBrowser=QTextBrowser(self)
        self.numSectionsBrower=QTextBrowser(self)

        #底部的一些部件
        #提取按钮
        self.ExractBtn=QPushButton()
        self.ExractBtn.setText("提取")
        self.ExractBtn.setMaximumSize(200,50)

        #是否用停用词
        self.UseStopwordCheckBox=QCheckBox()
        self.UseStopwordCheckBox.setText("是否使用停用词")
        self.UseStopwordCheckBox.stateChanged.connect(self.StopwordCheckBoxChange)

        #关键词个数设置
        self.NumKeywordsBox=QSpinBox()
        self.NumKeywordsBoxLabel=QLabel()
        self.NumKeywordsBoxLabel.setText("关键词个数")

        #底部部件布局
        bottomSecondLayout=QGridLayout()
        bottomSecondLayout.setContentsMargins(10,10,10,10)
        bottomSecondLayout.addWidget(self.UseStopwordCheckBox,0,5,1,3)
        bottomSecondLayout.addWidget(self.NumKeywordsBoxLabel,1,5,1,1)
        bottomSecondLayout.addWidget(self.NumKeywordsBox,1,6,1,2)

        bottomSpacer=QSpacerItem(100,10,QSizePolicy.Fixed)
        bottomSpacer1 = QSpacerItem(100, 10, QSizePolicy.Fixed)

        bottomLayout=QHBoxLayout()
        bottomLayout.addWidget(self.ExractBtn)
        bottomLayout.addSpacerItem(bottomSpacer)
        bottomLayout.addLayout(bottomSecondLayout)
        bottomLayout.addSpacerItem(bottomSpacer1)

        #布局
        ThirdLayout = QGridLayout()
        ThirdLayout.addWidget(self.keywordsLabel,0,0,1,1)
        ThirdLayout.addWidget(self.fileNameLabel,1,0,1,1)
        ThirdLayout.addWidget(self.numSectionsLabel,2,0,1,1)
        ThirdLayout.addWidget(self.keywordsBrowser,0,1,1,1)
        ThirdLayout.addWidget(self.fileNameBrowser,1,1,1,1)
        ThirdLayout.addWidget(self.numSectionsBrower,2,1,1,1)

        SecondLayout = QGridLayout()
        SecondLayout.addWidget(self.MainTextBrowser,0,0,1,3)
        SecondLayout.addLayout(ThirdLayout,0,4,1,2)

        MainLayout=QVBoxLayout()
        MainLayout.addWidget(self.menuBar)
        MainLayout.addLayout(SecondLayout)
        MainLayout.addLayout(bottomLayout)

        self.setLayout(MainLayout)

        # 初始化预处理器



    def OpenFile(self):
        """
        打开文件
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "打开文件", "",
                                                "All Files (*);;Docx Files (*.docx)", options=options)
        if(fileName==""):
            return
        text = ""
        logger.info("open file %s",fileName)
        try:#这个是文本文件的情况
            with open(str(fileName), "r") as f:
                text=f.read()
        except UnicodeDecodeError:  # 目前只能处理docx文件
                try:
                    document = Document(str(fileName))
                    for para in document.paragraphs:
                        text += para.text + "\n"
                except (exceptions.PackageNotFoundError):
                    logger.warning("File format incorrect or not exist")
                    dia=ErrorDialog("文件格式不正确或者文件不存在！")
                    dia.exec_()
                    return
        self.MainTextBrowser.clear()
        self.MainTextBrowser.append(text)



    def StopwordCheckBoxChange(self):
        """
        停用词列表改变后的的唔做
        :return:
        """
        if(self.UseStopwordCheckBox.isChecked()):
            print("checked")
        else:
            print("unchecked")


if __name__ == '__main__':
    #初始化日志
    logging.config.fileConfig('./log.conf')

    app=QApplication(sys.argv)
    demo=AppDemo()
    demo.resize(800,600)
    demo.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("close window")