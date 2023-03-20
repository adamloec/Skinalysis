import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Connect to the database and create the table if it doesn't exist
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, content TEXT)')

        # Create the table widget
        self.tablewidget = QTableWidget(self)
        self.tablewidget.setColumnCount(2)
        self.tablewidget.setHorizontalHeaderLabels(["Content", ""])

        # Add some data to the table widget from the database
        self.populateTable()

        # Set the item as clickable and non-editable
        for i in range(self.tablewidget.rowCount()):
            contentItem = self.tablewidget.item(i, 0)
            contentItem.setFlags(contentItem.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Remove ItemIsEditable flag
            deleteButton = QPushButton("Delete")
            deleteButton.setObjectName(str(i))  # Set object name to the row index for easy access later
            self.tablewidget.setCellWidget(i, 1, deleteButton)

            # Connect the delete button clicked signal to the deleteItem method
            deleteButton.clicked.connect(self.deleteItem)

        # Set the horizontal header stretch mode to Stretch
        self.tablewidget.horizontalHeader().setStretchLastSection(True)

        self.setCentralWidget(self.tablewidget)

    def populateTable(self):
        # Clear the table before repopulating
        self.tablewidget.setRowCount(0)

        # Populate the table from the database
        self.c.execute('SELECT * FROM items')
        items = self.c.fetchall()
        self.tablewidget.setRowCount(len(items))

        for i, item in enumerate(items):
            content = item[1]
            contentItem = QTableWidgetItem(content)
            contentItem.setTextAlignment(Qt.AlignCenter)
            self.tablewidget.setItem(i, 0, contentItem)

    def addItem(self):
        # Add the new item to the database
        content = self.textbox.text()
        self.c.execute('INSERT INTO items (content) VALUES (?)', (content,))
        self.conn.commit()

        # Clear the text box and repopulate the table
        self.textbox.clear()
        self.populateTable()

    def deleteItem(self):
        # Get the index of the row to delete
        index = int(self.sender().objectName())

        # Get the corresponding item ID from the database
        self.c.execute('SELECT id FROM items LIMIT 1 OFFSET ?', (index,))
        item_id = self.c.fetchone()[0]

        # Delete the item from the database
        self.c.execute('DELETE FROM items WHERE id = ?', (item_id,))
        self.conn.commit()

        # Repopulate the table
        self.populateTable()

    def closeEvent(self, event):
        # Close the database connection when the window is closed
        self.conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
