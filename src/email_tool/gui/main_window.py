from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
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
from email_tool.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_USE_TLS,
)
from email_tool.mailer import SMTPMailer
from email_tool.sender import send_bulk

from .preview_window import PreviewWindow
from .attachment_tag import AttachmentTag


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.csv_path = None
        self.template_path = None
        self.selected_attachment_path = None
        self.attachments = []

        self.setWindowTitle("Mail Sender")

        layout = QVBoxLayout()

        self.csv_label = QLabel("No recipient file selected")
        self.csv_button = QPushButton("Select Recipients CSV")

        self.template_label = QLabel("No template selected")
        self.template_button = QPushButton("Select Template")
        
        self.attachment_input = QLineEdit()
        self.attachment_input.setPlaceholderText("No attachment selected")
        self.attachment_input.setReadOnly(True)
        
        self.attachment_select_button = QPushButton("Select File")
        self.attachment_add_button = QPushButton("Add Attachment")

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Email subject")

        self.preview_button = QPushButton("Preview")
        self.send_button = QPushButton("Send Emails")
        
        attachment_controls = QHBoxLayout()

        attachment_controls.addWidget(self.attachment_input)
        attachment_controls.addWidget(self.attachment_select_button)
        attachment_controls.addWidget(self.attachment_add_button)
        
        self.attachments_layout = QVBoxLayout()

        layout.addWidget(self.csv_label)
        layout.addWidget(self.csv_button)
        layout.addWidget(self.template_label)
        layout.addWidget(self.template_button)
        layout.addWidget(QLabel("Attachments"))
        layout.addLayout(attachment_controls)
        layout.addLayout(self.attachments_layout)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.preview_button)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.csv_button.clicked.connect(self.select_csv)
        self.template_button.clicked.connect(self.select_template)
        self.preview_button.clicked.connect(self.preview)
        self.attachment_select_button.clicked.connect(self.select_attachment)
        self.attachment_add_button.clicked.connect(self.add_attachment)
        self.send_button.clicked.connect(self.send_emails)

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
            attachments=self.attachments,
        )

        self.preview_window.show()
        
    def select_attachment(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Attachment",
            "",
            "All Files (*)",
        )

        if path:
            self.selected_attachment_path = path
            self.attachment_input.setText(path)
            
    def add_attachment(self):
        if not self.selected_attachment_path:
            return

        if self.selected_attachment_path in self.attachments:
            self.selected_attachment_path = None
            self.attachment_input.clear()
            return

        self.attachments.append(
            self.selected_attachment_path
        )

        self.add_attachment_tag(
            self.selected_attachment_path
        )

        self.selected_attachment_path = None
        self.attachment_input.clear()
        
    def add_attachment_tag(self, path: str):
        tag = AttachmentTag(
            path,
            self.remove_attachment,
        )

        self.attachments_layout.addWidget(tag)

    def remove_attachment(self, path: str, tag):
        if path in self.attachments:
            self.attachments.remove(path)

        tag.deleteLater()
        
    def send_emails(self):
        if not self.csv_path:
            return

        if not self.template_path:
            return

        subject = self.subject_input.text().strip()

        if not subject:
            return

        recipients = load_recipients(self.csv_path)

        valid_recipients, invalid_recipients = (
            validate_recipients(recipients)
        )

        template = load_template(self.template_path)

        mailer = SMTPMailer(
            host=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            use_tls=SMTP_USE_TLS,
        )

        result = send_bulk(
            mailer=mailer,
            recipients=valid_recipients,
            template=template,
            subject=subject,
            body_template="Hi {{ name }},\n\nThis is a test email.",
            attachments=self.attachments,
        )

        print(f"Valid: {len(valid_recipients)}")
        print(f"Invalid: {len(invalid_recipients)}")
        print(f"Success: {len(result['success'])}")
        print(f"Failed: {len(result['failed'])}")