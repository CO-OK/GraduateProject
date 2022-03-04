from PyQt5.QtWidgets import QTextBrowser
from docx import Document
from docx.opc import exceptions
class TextBrowser(QTextBrowser):
    def __init__(self,parent):
        super(TextBrowser, self).__init__(parent)
        #可以接受拖过来的文件
        self.setAcceptDrops(True)
    def dragEnterEvent(self, event):
        if(event.mimeData().hasText()):
            event.accept()
            print("accept")
        else:
            event.ignore()
            print("ignore")
    def dropEvent(self, event):
        print("666")
        #self.setText(event.mimeData().text())

        self.OpenFile(event.mimeData().text()[7:])#不同系统1可能需要更改这一行
        print("set text")

    def dragMoveEvent(self, event):
        """
        Need to accept DragMove to catch drop for TextBrowser
        """
        if (event.mimeData().hasText()):
            event.accept()
    def OpenFile(self,fileName):
        """
        打开文件
        """
        text=""
        try:#这个是文本文件的情况
            with open(str(fileName), "r") as f:
                text=f.read()
        except UnicodeDecodeError:#目前只能处理docx文件
            try:
                document = Document(str(fileName))
            except (ValueError,exceptions.PackageNotFoundError) :
                print("wrong")


        self.clear()
        self.setText(text)

