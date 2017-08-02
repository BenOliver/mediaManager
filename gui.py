'''
Following tutorial http://zetcode.com/gui/pyqt5/
'''

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox,
                             QDesktopWidget, QMainWindow, qApp, QAction, QTextEdit, QLabel,
                             QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QGridLayout)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtCore import QCoreApplication


class exampleAbsolute(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        okButton = QPushButton("OK2")

        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15,10)

        lbl2 = QLabel('tutorials', self)
        lbl2.move(35,40)

        lbl3 = QLabel('tutorials', self)
        lbl3.move(55, 70)

        self.setGeometry(300, 300, 250, 150)
        self.setBaseSize(100,100)
        # self.setWindowTitle('Absolute')

class exampleBox(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

class exampleGrid(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        title = QLabel("Title")
        author = QLabel("Author")
        review = QLabel("Review")

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        textWid=QWidget()
        vbox=QVBoxLayout()
        vbox.addWidget(review)
        vbox.addStretch(1)
        textWid.setLayout(vbox)

        grid.addWidget(textWid, 3, 0, 5, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)


        self.setLayout(grid)

class myWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        # textEdit = QTextEdit()
        centralWidget=QWidget()

        hbox = QHBoxLayout()
        exampleA = exampleAbsolute()
        exampleA2 = exampleAbsolute()
        exampleB = exampleBox()
        exampleG = exampleGrid()

        # hbox.addWidget(exampleA)
        # hbox.addStretch(1)
        # hbox.addWidget(exampleA2)
        # hbox.addWidget(exampleB)
        hbox.addWidget(exampleG)

        centralWidget.setLayout(hbox)

        self.setCentralWidget(centralWidget)

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