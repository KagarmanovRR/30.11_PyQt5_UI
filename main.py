import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from form_stud import Ui_widget

STUD_GROUP = ['205ИС', '195ИС', '204ОИБ']


class MyWidget(QMainWindow, Ui_widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cbGroup.addItems(STUD_GROUP)
        self.rbMale.setChecked(True)
        self.pbInsert.clicked.connect(self.insert_stud)
        self.pbOpen.clicked.connect(self.open_file)
        self.pbDelete.clicked.connect(self.delete_stud)
        self.pbFind.clicked.connect(self.find_for_val)
        self.conn = None

    def open_file(self):
        try:
            self.conn = sqlite3.connect('stud_db.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from student")
            col_name = [i[0] for i in data.description]
            print(col_name)
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.twStud.setColumnCount(len(col_name))
        self.twStud.setHorizontalHeaderLabels(col_name)
        self.twStud.setRowCount(0)
        #self.cbColNames.addItems(col_name)
        for i, row in enumerate(data_rows):
            self.twStud.setRowCount(self.twStud.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStud.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStud.resizeColumnsToContents()
        #self.avg_age()

    def update_stud(self, query="select * from student"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e

        self.twStud.setRowCount(0)
        for i, row in enumerate(data):
            self.twStud.setRowCount(self.twStud.rowCount() + 1)
            for j, elem in enumerate(row):
                self.twStud.setItem(i, j, QTableWidgetItem(str(elem)))
        self.twStud.resizeColumnsToContents()
        #self.avg_age()

    def insert_stud(self):
        row = [self.leFIO.text(), 'м' if self.rbMale.isChecked() else 'ж', self.sbAge.text(),
               self.lePhone.text(), self.leEmail.text(), self.cbGroup.itemText(self.cbGroup.currentIndex()),
               self.sbKurs.text()]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into student(fio, gender, age, tel, email, groups, kurses)
            values('{row[0]}', '{row[1]}', {row[2]}, '{row[3]}', '{row[4]}', '{row[5]}', {row[6]})""")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_stud()

    def delete_stud(self):
        row = self.twStud.currentRow()
        num = self.twStud.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from student where studbilet = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_stud()

    def find_for_val(self):
        val = self.leFIO.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_stud(f"select * from student where {col} like '{val}%'")
        # try:
        #     cur = self.conn.cursor()
        #     avg = cur.execute(f"select * from student where {col} like '{val}%'").fetchone()
        # except Exception as e:
        #     print(f"Проблемы с подключением к БД. {e}")
        #     return e
        # self.lblAvgAge.setText(f"Средний возрст {round(avg[0], 2)}")

    def closeEvent(self, event):
        if self.conn is not None:
            self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

