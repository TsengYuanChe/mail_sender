from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
)


class PreviewWindow(QWidget):
    def __init__(
        self,
        total: int,
        valid: int,
        invalid: int,
        subject: str,
        html_body: str,
        attachments: list[str],
    ):
        super().__init__()

        self.setWindowTitle("Email Preview")
        self.resize(600, 500)

        layout = QVBoxLayout()

        self.summary_label = QLabel(
            f"Total: {total} | "
            f"Valid: {valid} | "
            f"Invalid: {invalid}"
        )

        self.subject_label = QLabel(
            f"Subject: {subject}"
        )
        
        self.attachments = attachments

        self.preview_content = QTextEdit()
        self.preview_content.setReadOnly(True)
        self.preview_content.setHtml(html_body)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        layout.addWidget(self.summary_label)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.preview_content)
        
        attachments_label = QLabel(
            f"Attachments ({len(self.attachments)})"
        )

        layout.addWidget(attachments_label)

        for attachment in self.attachments:
            path = Path(attachment)

            button = QPushButton(path.name)

            button.clicked.connect(
                lambda checked=False, file_path=attachment:
                    self.open_attachment(file_path)
            )

            layout.addWidget(button)
        
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        
    def open_attachment(self, path: str):
        file_path = Path(path)

        if not file_path.exists():
            return
        
        QDesktopServices.openUrl(
            QUrl.fromLocalFile(path)
        )