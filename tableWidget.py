from PyQt5.QtWidgets import QApplication, QFormLayout, QWidget, QGroupBox, QLabel, QPushButton, QLineEdit
import sys

class TableWidget(QWidget):
    def __init__(self, tableName, fields):
        super().__init__()
        groupBox = QGroupBox(tableName, self)
        tableLayout = QFormLayout(self)
        groupBox.setLayout(tableLayout)
        self.fields = []

        for field in fields:
            fieldLineEdit = QLineEdit()
            fieldLineEdit.setObjectName(field)
            self.fields.append(fieldLineEdit)
            tableLayout.addRow(QLabel(field + ':'), fieldLineEdit)

        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(self.clearFields)
        tableLayout.addWidget(clearButton)

        self.setMinimumSize(groupBox.sizeHint())

    def clearFields(self):
        for fieldLineEdit in self.fields:
            fieldLineEdit.clear()

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = TableWidget("Race", ["Year", "Series", "Class"])
    myApp.show()

    sys.exit(app.exec_())