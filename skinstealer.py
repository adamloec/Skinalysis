# Skin Stealer QT application.
# Author: Adam Loeckle

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QListWidget
)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sqlite3

from market import Market
from mmath import MMath

# url = "https://steamcommunity.com/market/listings/730/Revolution%20Case"
# market = Market(url)
# market.scan()
# # for i in range(0, len(market.history)):
# #     print(market.history[i])
# print(MMath.sma(21, market.history))

class SkinStealer(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Skin Stealer"
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()

    # Initialize UI.
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create vertical layout.
        vbox = QVBoxLayout()

        # Create horizontal layout for URL text input.
        hbox1 = QHBoxLayout()
        self.label = QLabel("CSGO Market Item URL:")
        self.textbox = QLineEdit()
        self.submit_button = QPushButton("Submit")
        hbox1.addWidget(self.label)
        hbox1.addWidget(self.textbox)
        hbox1.addWidget(self.submit_button)

        # Create URL table widget to display database information.
        self.market_table = QTextEdit()
        self.market_table.setReadOnly(True)

        # Add layouts to vbox (vertical layout).
        vbox.addLayout(hbox1)
        vbox.addWidget(self.market_table)

        # Set main layout for window.
        self.setLayout(vbox)
        
        # Connect the submit button to the addEntry() method.
        self.submit_button.clicked.connect(self.addEntry)
        
        # Show window.
        self.show()

        # Display database market contents.
        self.displayEntries()

    # Displays database table to client.
    def displayEntries(self):
        
        # Connect to the database.
        conn = sqlite3.connect('market.db')
        c = conn.cursor()

        # Create the DB table if it does not exist.
        c.execute('''CREATE TABLE IF NOT EXISTS market
                     (id INTEGER PRIMARY KEY,
                      content TEXT NOT NULL)''')
        
        # Query the database for all of the market information.
        c.execute('SELECT content FROM market')
        rows = c.fetchall()

        # Close the database connection.
        conn.close()

        # Clear the URL table widget.
        self.market_table.clear()

        # Add market data to the URL table widget.
        for row in rows:
            self.market_table.append(row[0])

    
    # Add new market URL link to database.
    # NEEDS: pre-check to ensure URL is valid CSGO market item web page.
    def addEntry(self):
        
        # Get URL from the text box.
        url = self.textbox.text()

        # Connect to the database.
        conn = sqlite3.connect('market.db')
        c = conn.cursor()

        # Insert the new URL into the database table.
        c.execute('INSERT INTO market (content) VALUES (?)', (url,))
        conn.commit()

        # Close the database connection.
        conn.close()

        # Clear the text box.
        self.textbox.clear()

        # Displays the contents of the database in the market table.
        self.displayEntries()

def main():

    app = QApplication(sys.argv)
    ex = SkinStealer()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()