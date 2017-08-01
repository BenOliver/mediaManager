import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox,
                             QDesktopWidget, QMainWindow, qApp, QAction, QTextEdit)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtCore import QCoreApplication


class myWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('exit24.png'), 'Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar().showMessage('Ready')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setGeometry(300,300,300,220)
        self.center()
        self.setWindowTitle('Ben\'s Application')
        self.show()

        # self.setToolTip('This is a <b>Qidget</b> widget')

        # btn = QPushButton('Btn', self)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        # btn.move(50,50)
        #
        # qbtn = QPushButton('Quit',self)
        # qbtn.clicked.connect(QCoreApplication.instance().quit)
        # qbtn.resize(qbtn.sizeHint())
        # qbtn.move(50,100)






    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




if __name__ == "__main__":

    app = QApplication(sys.argv)

    w=myWidget()
    sys.exit(app.exec_())