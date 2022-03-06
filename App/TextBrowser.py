from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import  *
from docx import Document
from docx.opc import exceptions
import logging
from ErrorDialog import ErrorDialog
logger = logging.getLogger('logger')
class TextBrowser(QTextBrowser):
    HasTextSignal=pyqtSignal(str)
    def __init__(self,parent):
        super(TextBrowser, self).__init__(parent)
        #可以接受拖过来的文件
        self.setAcceptDrops(True)

        logger.info("Initilize TextBorwser")
    def dragEnterEvent(self, event):
        if(event.mimeData().hasText()):
            event.accept()
            logger.info("TextBrowser darg enter event accept")
        else:
            event.ignore()
            logger.info("TextBrowser darg enter event ignore")
    def dropEvent(self, event):

        logger.info("TextBrowser drag event , file: %s",event.mimeData().text()[7:])
        self.OpenFile(event.mimeData().text()[7:])#不同系统1可能需要更改这一行


    def dragMoveEvent(self, event):
        """
        Need to accept DragMove to catch drop for TextBrowser
        """
        if (event.mimeData().hasText()):
            # logger.info("TextBrowser darg move event accept")
            event.accept()
        else:
            # logger.info("TextBrowser darg move event ignore")
            event.ignore()

    def OpenFile(self,fileName):
        """
        打开文件
        """
        if (fileName == ""):
            return
        text=""
        logger.info("open file %s", fileName)
        try:#这个是文本文件的情况
            with open(str(fileName), "r") as f:
                text=f.read()
        except UnicodeDecodeError:  # 目前只能处理docx文件
                try:
                    document = Document(str(fileName))
                    for para in document.paragraphs:
                        text += para.text + "\n"
                    logger.info("emit signal")
                    self.HasTextSignal.emit(fileName)
                except (exceptions.PackageNotFoundError):
                    logger.warning("File format incorrect or not exist")
                    dia = ErrorDialog("文件格式不正确或者文件不存在！")
                    dia.exec_()
                    return
        self.clear()
        self.setText(text)

