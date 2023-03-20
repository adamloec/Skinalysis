# Skin Stealer QT application.
# Author: Adam Loeckle

import sys

from PyQt6 import QtGui
from PyQt6.QtGui import QAction, QIcon
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
myappid = 'Skinalysis.v1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class Skinalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Skinalysis"
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()

    # Initialize UI.
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('app/imgs/skinalysis-icon.png'))

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

        # Add layouts to vbox (vertical layout).
        vbox.addLayout(hbox1)
        vbox.addWidget(self.market_table)
        self.setLayout(vbox)
        
        # Connect the submit button to the addEntry() method.
        self.submit_button.clicked.connect(self.addEntry)
        
        # Show window.
        self.show()
        self.market_table.display()

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
        self.customContextMenuRequested.connect(self.contextMenu)

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
        # Find selected row
        selection = self.selectionModel().selectedRows()
        if not selection:
            return
        row = selection[0].row()
        print(row)

        # Delete the selected row, and update the SQL tables row-id's to resync.
        self.c.execute("DELETE FROM market WHERE rowid=?", (row + 1,))
        self.c.execute("SELECT rowid, * FROM market")
        rows = self.c.fetchall()
        for i, row_data in enumerate(rows, 1):
            rowid = row_data[0]
            self.c.execute("UPDATE market SET rowid=? WHERE rowid=?", (i, rowid))
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
    def contextMenu(self, pos):
        index = self.indexAt(pos)

        if index.isValid():
            menu = QMenu()
            menu.setStyleSheet(open('app/css/table-context.css').read())

            deleteAction = QAction("Delete", self)
            deleteAction.triggered.connect(self.delete)
            menu.addAction(deleteAction)

            menu.addSeparator()
            renameAction = QAction("Rename", self)
            menu.addAction(renameAction)
            menu.addSeparator()
            cutAction = QAction("Cut", self)
            menu.addAction(cutAction)
            copyAction = QAction("Copy", self)
            menu.addAction(copyAction)
            pasteAction = QAction("Paste", self)
            menu.addAction(pasteAction)

            menu.exec(self.viewport().mapToGlobal(pos))
        
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
    ex = Skinalysis()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()