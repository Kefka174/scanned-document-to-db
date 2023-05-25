from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGroupBox, QFormLayout, QLineEdit
import sys

class TableWidget(QWidget):
    def __init__(self, table, fields):
        super().__init__()
        self.table = QGroupBox(table, self)
        tableLayout = QFormLayout(self)
        self.table.setLayout(tableLayout)
        self.fields = []

        for field in fields:
            fieldLineEdit = QLineEdit()
            fieldLineEdit.setObjectName(field)
            self.fields.append(fieldLineEdit)
            tableLayout.addRow(QLabel(field + ':'), fieldLineEdit)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearFields)
        tableLayout.addWidget(self.clearButton)

        self.setMinimumSize(self.table.sizeHint())

    def clearFields(self):
        for fieldLineEdit in self.fields:
            fieldLineEdit.clear()

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = TableWidget("Race", ["Year", "Series", "Class"])
    myApp.show()

    sys.exit(app.exec_())