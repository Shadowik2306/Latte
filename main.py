import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('main.ui', self)
        self.load_table()

    def load_table(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        lst = cur.execute('SELECT * FROM main')
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels('ID, название сорта, степень обжарки,'
                                                   ' молотый/в зернах, описание вкуса,'
                                                   ' цена, объем упаковки'.split(','))
        self.tableWidget.horizontalHeader().setSectionResizeMode(1)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(lst):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Window()
    wind.show()
    sys.exit(app.exec())