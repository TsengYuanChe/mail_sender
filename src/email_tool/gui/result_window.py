from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


class ResultWindow(QWidget):
    def __init__(
        self,
        total: int,
        valid_recipients: list[dict[str, str]],
        invalid_recipients: list[dict],
    ):
        super().__init__()

        self.setWindowTitle("Send Result")
        self.resize(500, 500)

        self.success_count = 0
        self.failed_count = 0

        layout = QVBoxLayout()

        self.total_label = QLabel(
            f"Total: {total}"
        )
        layout.addWidget(self.total_label)

        self.invalid_label = QLabel(
            f"Invalid: {len(invalid_recipients)}"
        )
        layout.addWidget(self.invalid_label)

        for item in invalid_recipients:
            recipient = item["recipient"]
            errors = item["errors"]

            name = recipient.get("name", "")
            reason = ", ".join(errors)

            layout.addWidget(
                QLabel(f"{name} — {reason}")
            )

        self.valid_label = QLabel(
            f"Valid: {len(valid_recipients)}"
        )
        layout.addWidget(self.valid_label)

        self.recipient_labels = {}

        for recipient in valid_recipients:
            email = recipient["email"]
            name = recipient["name"]

            label = QLabel(
                f"⏳ Sending to {name}..."
            )

            self.recipient_labels[email] = label

            layout.addWidget(label)

        self.success_label = QLabel(
            "Success: 0"
        )

        self.failed_label = QLabel(
            "Failed: 0"
        )

        layout.addWidget(self.success_label)
        layout.addWidget(self.failed_label)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(
            self.close
        )

        layout.addWidget(self.close_button)

        self.setLayout(layout)
        
    def mark_success(
        self,
        name: str,
        email: str,
    ):
        label = self.recipient_labels.get(email)

        if label:
            label.setText(
                f"✅ {name} — Success"
            )

        self.success_count += 1
        self.success_label.setText(
            f"Success: {self.success_count}"
        )


    def mark_failed(
        self,
        name: str,
        email: str,
        reason: str,
    ):
        label = self.recipient_labels.get(email)

        if label:
            label.setText(
                f"❌ {name} — {reason}"
            )

        self.failed_count += 1
        self.failed_label.setText(
            f"Failed: {self.failed_count}"
        )