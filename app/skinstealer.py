# Skin Stealer QT application.
# Author: Adam Loeckle

import sys

from PyQt6 import QtGui
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QMenu,
)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sqlite3

from mutils.market import Market
from mutils.mmath import MMath

# url = "https://steamcommunity.com/market/listings/730/Revolution%20Case"
# market = Market(url)
# market.scan()
# # for i in range(0, len(market.history)):
# #     print(market.history[i])
# print(MMath.sma(21, market.history))

import ctypes
myappid = 'SkinStealer.v1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
        self.setWindowIcon(QtGui.QIcon('app/imgs/skinstealer-icon.png'))

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
        self.market_table = MarketTable(self)
        self.market_table.display()

        # Add layouts to vbox (vertical layout).
        vbox.addLayout(hbox1)
        vbox.addWidget(self.market_table)

        # Set main layout for window.
        self.setLayout(vbox)
        
        # Connect the submit button to the addEntry() method.
        self.submit_button.clicked.connect(self.addEntry)
        
        # Show window.
        self.show()

    # Add new market URL link to database.
    # NEEDS: pre-check to ensure URL is valid CSGO market item web page.
    def addEntry(self):
        
        # Get URL from the text box.
        url = self.textbox.text()

        # Call Market Table add entry function.
        self.market_table.add(url)

        # Clear the text box.
        self.textbox.clear()

# Custom Table Widget for displaying market data and related functions.
class MarketTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Connect to the database to access market data.
        self.conn = sqlite3.connect('app/market.db')
        self.c = self.conn.cursor()

        # Create the DB table if it does not exist.
        self.c.execute('''CREATE TABLE IF NOT EXISTS market
                     (id INTEGER PRIMARY KEY,
                      content TEXT NOT NULL)''')

        # Table styling.
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)

        # Context menu.
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # On-click launches graph view of market data for selected item.
        self.itemClicked.connect(self.graphWindow)
    
    # Adds a new listing to the table/DB.
    def add(self, url):
        
        # Insert the new URL into the database table.
        self.c.execute('INSERT INTO market (content) VALUES (?)', (url,))
        self.conn.commit()

        # Displays the contents of the database in the market table.
        self.display()

    # Deletes a listing from the table/DB.
    def delete(self):
        # Index of row to delete.
        index = int(self.sender().objectName())

        # Corresponding ID from database.
        self.c.execute('SELECT id FROM market LIMIT 1 OFFSET ?', (index,))
        item_id = self.c.fetchone()[0]

        # Delete the item from the database.
        self.c.execute('DELETE FROM market WHERE id = ?', (item_id,))
        self.conn.commit()

        # Display new table contents.
        self.display()

    # Display the table contents from the database.
    def display(self):
        # Query the database for all of the market information.
        self.c.execute('SELECT content FROM market')
        rows = self.c.fetchall()

        # Clear the market table widget.
        self.clear()

        # Add market data to the market table widget.
        self.setColumnCount(1)
        self.setRowCount(len(rows))

        for i, row in enumerate(rows):

            # Add each database listing to table in client.
            self.setItem(i, 0, QTableWidgetItem(row[0]))
            
            # Item listing flags.
            # Non-editable, clickable table contents.
            listing = self.item(i, 0)

            flags = listing.flags()
            flags &= ~Qt.ItemFlag.ItemIsEditable # Non-editable
            flags |= Qt.ItemFlag.ItemIsSelectable # Clickable, to open seperate window
            listing.setFlags(flags)

    # Context Menu for each table listing.
    # Right click on table listing to display context menu.
    def showContextMenu(self, position):
        indexes = self.selectedIndexes()
        if not indexes:
            return

        row = indexes[0].row()

        menu = QMenu()
        delete_action = QtGui.QAction('Delete', self)
        delete_action.triggered.connect(lambda: self.delete_item(row))
        menu.addAction(delete_action)
        menu.exec_(self.viewport().mapToGlobal(position))
        
    def graphWindow(self, item):

        # Create the dialog window
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Window")
        dialog.resize(200, 100)

        # Add some widgets to the dialog window
        dialog_label = QLabel(item.text(), dialog)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(dialog_label)
        layout.addStretch()

        dialog.setLayout(layout)

        # Show the dialog window
        dialog.exec()

def main():

    app = QApplication(sys.argv)
    ex = SkinStealer()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()