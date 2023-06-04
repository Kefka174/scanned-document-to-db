from PyQt5.QtWidgets import QApplication, QFormLayout, QWidget, QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
import sys

class TableWidget(QWidget):
    def __init__(self, tableName, fields):
        super().__init__()
        self.setObjectName(tableName)
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
        clearButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        clearButton.clicked.connect(self.clearFields)
        tableLayout.addWidget(clearButton)

        self.setMinimumSize(groupBox.sizeHint())
        self.setFocusProxy(self.fields[0])

    def clearFields(self):
        for fieldLineEdit in self.fields:
            fieldLineEdit.clear()
        self.fields[0].setFocus()

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = TableWidget("Race", ["Year", "Series", "Class"])
    myApp.show()

    sys.exit(app.exec_())