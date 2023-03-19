# Skin Stealer QT application.
# Author: Adam Loeckle

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from market import Market
from mmath import MMath

# url = "https://steamcommunity.com/market/listings/730/Revolution%20Case"
# market = Market(url)
# market.scan()
# # for i in range(0, len(market.history)):
# #     print(market.history[i])
# print(MMath.sma(21, market.history))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Skin Stealer")
        self.setFixedSize(QSize(800, 600))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
