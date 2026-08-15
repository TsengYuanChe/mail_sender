from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mail Sender")

        layout = QVBoxLayout()

        self.csv_label = QLabel("No recipient file selected")
        self.csv_button = QPushButton("Select Recipients CSV")

        self.template_label = QLabel("No template selected")
        self.template_button = QPushButton("Select Template")

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Email subject")

        self.preview_button = QPushButton("Preview")
        self.send_button = QPushButton("Send Emails")

        layout.addWidget(self.csv_label)
        layout.addWidget(self.csv_button)
        layout.addWidget(self.template_label)
        layout.addWidget(self.template_button)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.preview_button)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.csv_button.clicked.connect(self.select_csv)
        self.template_button.clicked.connect(self.select_template)

    def select_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Recipients CSV",
            "",
            "CSV Files (*.csv)",
        )

        if path:
            self.csv_label.setText(path)

    def select_template(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Template",
            "",
            "HTML Files (*.html)",
        )

        if path:
            self.template_label.setText(path)


def run_gui():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()