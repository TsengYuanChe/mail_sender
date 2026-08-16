from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
)

from email_tool.recipients import load_recipients
from email_tool.template import (
    load_template,
    render_template,
)
from email_tool.validation import validate_recipients

from .preview_window import PreviewWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.csv_path = None
        self.template_path = None

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
        self.preview_button.clicked.connect(self.preview)

    def select_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Recipients CSV",
            "",
            "CSV Files (*.csv)",
        )

        if path:
            self.csv_path = path
            self.csv_label.setText(path)

    def select_template(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Template",
            "",
            "HTML Files (*.html)",
        )

        if path:
            self.template_path = path
            self.template_label.setText(path)
            
    def preview(self):
        if not self.csv_path:
            return

        if not self.template_path:
            return

        recipients = load_recipients(
            self.csv_path
        )

        valid_recipients, invalid_recipients = (
            validate_recipients(recipients)
        )

        template = load_template(
            self.template_path
        )

        if valid_recipients:
            preview_name = valid_recipients[0]["name"]

            html_body = render_template(
                template,
                preview_name,
            )
        else:
            html_body = "<p>No valid recipients.</p>"

        subject = self.subject_input.text()

        self.preview_window = PreviewWindow(
            total=len(recipients),
            valid=len(valid_recipients),
            invalid=len(invalid_recipients),
            subject=subject,
            html_body=html_body,
        )

        self.preview_window.show()