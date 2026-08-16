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

        self.preview_content = QTextEdit()
        self.preview_content.setReadOnly(True)
        self.preview_content.setHtml(html_body)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        layout.addWidget(self.summary_label)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.preview_content)
        layout.addWidget(self.close_button)

        self.setLayout(layout)