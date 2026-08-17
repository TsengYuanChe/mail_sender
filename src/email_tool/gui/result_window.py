from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QScrollArea,
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
        self.resize(650, 550)

        self.total = total
        self.valid_count = len(valid_recipients)
        self.invalid_count = len(invalid_recipients)
        self.success_count = 0
        self.failed_count = 0
        self.recipient_labels = {}

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Invalid
        invalid_group = QGroupBox(
            f"Invalid ({len(invalid_recipients)})"
        )
        invalid_layout = QVBoxLayout()

        for item in invalid_recipients:
            recipient = item["recipient"]
            errors = item["errors"]

            name = recipient.get("name", "")
            reason = ", ".join(errors)

            invalid_layout.addWidget(
                QLabel(
                    f"{name or '(No name)'} — {reason}"
                )
            )

        invalid_group.setLayout(invalid_layout)

        # Valid
        valid_group = QGroupBox(
            f"Valid ({len(valid_recipients)})"
        )
        valid_layout = QVBoxLayout()

        for recipient in valid_recipients:
            email = recipient["email"]
            name = recipient["name"]

            label = QLabel(
                f"⏸ {name} — Waiting"
            )

            self.recipient_labels[email] = label
            valid_layout.addWidget(label)

        valid_group.setLayout(valid_layout)

        # Scroll area
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        scroll_layout.addWidget(invalid_group)
        scroll_layout.addWidget(valid_group)
        scroll_layout.addStretch()

        scroll_content.setLayout(scroll_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)

        # Bottom summary
        bottom_layout = QHBoxLayout()

        self.summary_label = QLabel(
            f"Total: {self.total} | "
            f"Invalid: {self.invalid_count} | "
            f"To Send: {self.valid_count} | "
            f"Success: 0 | "
            f"Failed: 0"
        )

        self.close_button = QPushButton("Close")
        self.close_button.setMinimumWidth(120)
        self.close_button.clicked.connect(
            self.close
        )

        bottom_layout.addWidget(self.summary_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.close_button)

        main_layout.addWidget(scroll_area, 1)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def update_summary(self):
        self.summary_label.setText(
            f"Total: {self.total} | "
            f"Invalid: {self.invalid_count} | "
            f"To Send: {self.valid_count} | "
            f"Success: {self.success_count} | "
            f"Failed: {self.failed_count}"
        )

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
        self.update_summary()

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
        self.update_summary()

    def mark_sending(
        self,
        name: str,
        email: str,
    ):
        label = self.recipient_labels.get(email)

        if label:
            label.setText(
                f"⏳ Sending to {name}..."
            )