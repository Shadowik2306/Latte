import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from UI.addEditCoffeeForm import Ui_EditCoffeeForm
from UI.mainWindow import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('data/coffee.sqlite')
        self.cur = self.con.cursor()
        self.load_table()
        self.pushButton.clicked.connect(self.switch)

    def load_table(self):
        lst = self.cur.execute('SELECT * FROM coffee').fetchall()
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

    def switch(self):
        self.wind = EditCoffee()
        self.wind.show()
        self.close()


class EditCoffee(QMainWindow, Ui_EditCoffeeForm):
    def __init__(self):
        super(EditCoffee, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.act)

    def act(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        lst = self.textEdit.toPlainText().split(', ')
        try:
            self.cur.execute(f'INSERT INTO coffee(id, name, roast, type, description,'
                             f' cost, volume) VALUES(?, ?, ?, ?, ?, ?, ?)', (*lst,))
        except sqlite3.IntegrityError:
            self.cur.execute("""UPDATE coffee
                                SET name = ?,
                                roast = ?,
                                type = ?,
                                description = ?,
                                cost = ?,
                                volume = ?
                                WHERE id = ?""", (*lst[1:], lst[0]))
        except Exception:
            return
        self.con.commit()
        self.wind = Window()
        self.wind.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Window()
    wind.show()
    sys.exit(app.exec())
