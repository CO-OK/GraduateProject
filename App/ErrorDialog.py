from PyQt5.QtWidgets import QDialog,QPushButton,QApplication,QLabel,QGridLayout,QVBoxLayout,QSpacerItem,QSizePolicy,QHBoxLayout
import sys
import logging
logger = logging.getLogger('logger')
#用来打印错误信息
class ErrorDialog(QDialog):
    def __init__(self,msg):
        """
        :param ErrorMsg: 错误信息
        :param parent:
        """
        super(QDialog, self).__init__()

        logger.info("Initilize ErrorDialog")

        self.setMinimumSize(400,200)

        self.Button=QPushButton(self)
        self.Button.setMaximumSize(150,45)
        self.Button.setText("确定")
        self.Button.clicked.connect(self.Confirm)
        # self.Button.set
        self.lable=QLabel()
        self.lable.setText(msg)
        self.lable.setStyleSheet("QLabel{border:1px solid rgb(255, 255, 255);}");

        self.spacer=QSpacerItem(50,35,QSizePolicy.Expanding)
        # self.spacer.setText("")

        seccondLayout=QHBoxLayout()

        spacer1=QSpacerItem(100,15,QSizePolicy.Fixed)
        spacer2=QSpacerItem(100,15,QSizePolicy.Fixed)

        seccondLayout.addSpacerItem(spacer1)
        seccondLayout.addWidget(self.Button)
        seccondLayout.addSpacerItem(spacer2)

        layout=QVBoxLayout()

        layout.addWidget(self.lable)

        layout.addSpacerItem(self.spacer)

        layout.addLayout(seccondLayout)

        self.setLayout(layout)

    def Confirm(self):
        self.close()




if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=ErrorDialog("888")
    demo.resize(400,300)
    demo.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("close window")