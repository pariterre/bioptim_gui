import sys
from PyQt5 import QtCore, QtWidgets


class BioptimGui(QtWidgets.QMainWindow):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self, *args):
        super(BioptimGui, self).__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(600, 150, 400, 150)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        h_layout = QtWidgets.QHBoxLayout(central_widget)

        self.load_file = QtWidgets.QPushButton('Load')
        h_layout.addWidget(self.load_file)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = BioptimGui()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
