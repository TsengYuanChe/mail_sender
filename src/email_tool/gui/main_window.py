from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
    QGroupBox,
)
from PySide6.QtCore import QThread, Qt

from email_tool.recipients import load_recipients
from email_tool.template import (
    load_template,
    render_template,
)
from email_tool.validation import validate_recipients
from email_tool.template import load_template

from .preview_window import PreviewWindow
from .attachment_tag import AttachmentTag
from .result_window import ResultWindow
from .send_worker import SendWorker


class MainWindow(QWidget):
    def __init__(self, mailer):
        super().__init__()
        
        self.mailer = mailer
        self.csv_path = None
        self.template_path = None
        self.selected_attachment_path = None
        self.attachments = []

        self.setWindowTitle("Mail Sender")
        self.resize(720, 520)
        
        self.setStyleSheet("""
            QGroupBox::title {
                font-size: 18px;
                font-weight: bold;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)
        
        # =========================
        # Recipients
        # =========================
        recipients_group = QGroupBox("Recipients")
        recipients_layout = QHBoxLayout()
        
        self.csv_input = QLineEdit()
        self.csv_input.setPlaceholderText("No CSV selected")
        self.csv_input.setReadOnly(True)

        self.csv_button = QPushButton("Select CSV")

        recipients_layout.addWidget(self.csv_input, 1)
        recipients_layout.addWidget(self.csv_button)

        recipients_group.setLayout(recipients_layout)
        
        # =========================
        # Template
        # =========================
        template_group = QGroupBox("Template")
        template_layout = QHBoxLayout()

        self.template_input = QLineEdit()
        self.template_input.setPlaceholderText("No template selected")
        self.template_input.setReadOnly(True)

        self.template_button = QPushButton("Select Template")

        template_layout.addWidget(self.template_input, 1)
        template_layout.addWidget(self.template_button)

        template_group.setLayout(template_layout)

        # =========================
        # Attachments
        # =========================
        attachments_group = QGroupBox("Attachments")
        attachments_group_layout = QVBoxLayout()

        attachment_controls = QHBoxLayout()

        self.attachment_input = QLineEdit()
        self.attachment_input.setPlaceholderText("No attachment selected")
        self.attachment_input.setReadOnly(True)

        self.attachment_select_button = QPushButton("Select File")
        self.attachment_add_button = QPushButton("Add")

        attachment_controls.addWidget(
            self.attachment_input,
            1,
        )
        attachment_controls.addWidget(
            self.attachment_select_button
        )
        attachment_controls.addWidget(
            self.attachment_add_button
        )

        self.attachments_layout = QHBoxLayout()
        self.attachments_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )
        self.attachments_layout.setSpacing(6)

        attachments_group_layout.addLayout(
            attachment_controls
        )
        attachments_group_layout.addLayout(
            self.attachments_layout
        )

        attachments_group.setLayout(
            attachments_group_layout
        )

        # =========================
        # Email
        # =========================
        email_group = QGroupBox("Email")
        email_layout = QVBoxLayout()

        subject_label = QLabel("Subject")

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText(
            "Enter email subject"
        )

        email_layout.addWidget(subject_label)
        email_layout.addWidget(self.subject_input)

        email_group.setLayout(email_layout)
        
        # =========================
        # Actions
        # =========================
        action_layout = QHBoxLayout()
        
        self.account_label = QLabel(
            f"Signed in as  {self.mailer.username}"
        )

        self.preview_button = QPushButton("Preview")
        self.send_button = QPushButton("Send Emails")

        self.preview_button.setMinimumWidth(120)
        self.send_button.setMinimumWidth(160)

        action_layout.addWidget(self.account_label)
        action_layout.addStretch()
        action_layout.addWidget(self.preview_button)
        action_layout.addWidget(self.send_button)

        # =========================
        # Main layout
        # =========================
        main_layout.addWidget(recipients_group)
        main_layout.addWidget(template_group)
        main_layout.addWidget(attachments_group)
        main_layout.addWidget(email_group)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)

        # Events
        self.csv_button.clicked.connect(self.select_csv)
        self.template_button.clicked.connect(
            self.select_template
        )
        self.preview_button.clicked.connect(self.preview)

        self.attachment_select_button.clicked.connect(
            self.select_attachment
        )
        self.attachment_add_button.clicked.connect(
            self.add_attachment
        )

        self.send_button.clicked.connect(
            self.send_emails
        )

    def select_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Recipients CSV",
            "",
            "CSV Files (*.csv)",
        )

        if path:
            self.csv_path = path
            self.csv_input.setText(
                Path(path).name
            )

            self.csv_input.setToolTip(path)

    def select_template(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Template",
            "",
            "HTML Files (*.html)",
        )

        if path:
            self.template_path = path
            self.template_input.setText(
                Path(path).name
            )
            
            self.template_input.setToolTip(path)
            
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
            self.attachment_input.setText(
                Path(path).name
            )
            
            self.attachment_input.setToolTip(path)
            
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

        recipients = load_recipients(
            self.csv_path
        )

        valid_recipients, invalid_recipients = (
            validate_recipients(recipients)
        )

        template = load_template(
            self.template_path
        )

        self.result_window = ResultWindow(
            total=len(recipients),
            valid_recipients=valid_recipients,
            invalid_recipients=invalid_recipients,
        )

        self.result_window.show()

        self.send_thread = QThread()

        self.send_worker = SendWorker(
            mailer=self.mailer,
            recipients=valid_recipients,
            template=template,
            subject=subject,
            body_template="Hi {{ name }},\n\nThis is a test email.",
            attachments=self.attachments,
        )

        self.send_worker.moveToThread(
            self.send_thread
        )

        self.send_thread.started.connect(
            self.send_worker.run
        )
        
        self.send_worker.sending.connect(
            self.result_window.mark_sending
        )

        self.send_worker.success.connect(
            self.result_window.mark_success
        )

        self.send_worker.failed.connect(
            self.result_window.mark_failed
        )

        self.send_worker.finished.connect(
            self.send_thread.quit
        )

        self.send_worker.finished.connect(
            self.send_worker.deleteLater
        )

        self.send_thread.finished.connect(
            self.send_thread.deleteLater
        )

        self.send_thread.start()