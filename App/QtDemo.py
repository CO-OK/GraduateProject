import  sys
from PyQt5.QtWidgets import QApplication,QWidget
from  PyQt5 import  uic


class AppDemo(QWidget):
    def __init__(self):
        super(AppDemo, self).__init__()
        uic.loadUi('Demo.ui',self)



if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=AppDemo()
    demo.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("close window")