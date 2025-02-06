import sys
from PyQt5.QtWidgets import QApplication
from main_gui import StressMeasurementApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = StressMeasurementApp()
    mainWin.show()
    sys.exit(app.exec())