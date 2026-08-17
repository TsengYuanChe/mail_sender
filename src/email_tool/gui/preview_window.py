from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QGroupBox,
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

        self.attachments = attachments

        self.setWindowTitle("Email Preview")
        self.resize(720, 620)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)
        
        # Subject
        subject_group = QGroupBox("Subject")
        subject_layout = QVBoxLayout()

        subject_label = QLabel(subject)
        subject_label.setWordWrap(True)

        subject_layout.addWidget(subject_label)
        subject_group.setLayout(subject_layout)

        # Email content
        content_group = QGroupBox("Email Content")
        content_layout = QVBoxLayout()

        self.preview_content = QTextEdit()
        self.preview_content.setReadOnly(True)
        self.preview_content.setHtml(html_body)

        content_layout.addWidget(self.preview_content)
        content_group.setLayout(content_layout)

        # Attachments
        attachments_group = QGroupBox(
            f"Attachments ({len(self.attachments)})"
        )
        attachments_layout = QHBoxLayout()

        if self.attachments:
            for attachment in self.attachments:
                path = Path(attachment)

                button = QPushButton(path.name)

                button.clicked.connect(
                    lambda checked=False, file_path=attachment:
                        self.open_attachment(file_path)
                )

                attachments_layout.addWidget(button)

            attachments_layout.addStretch()
        else:
            attachments_layout.addWidget(
                QLabel("No attachments")
            )

        attachments_group.setLayout(
            attachments_layout
        )

        # Footer with summary and close button
        action_layout = QHBoxLayout()
        self.summary_label = QLabel(
            f"Total: {total} | "
            f"Valid: {valid} | "
            f"Invalid: {invalid}"
        )

        self.close_button = QPushButton("Close")
        self.close_button.setMinimumWidth(120)
        self.close_button.clicked.connect(self.close)

        action_layout.addWidget(self.summary_label)
        action_layout.addStretch()
        action_layout.addWidget(self.close_button)

        main_layout.addWidget(subject_group)
        main_layout.addWidget(content_group, 1)
        main_layout.addWidget(attachments_group)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)

    def open_attachment(self, path: str):
        file_path = Path(path)

        if not file_path.exists():
            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(str(file_path))
        )