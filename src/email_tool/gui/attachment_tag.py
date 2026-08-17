from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)


class AttachmentTag(QWidget):
    def __init__(
        self,
        path: str,
        remove_callback,
    ):
        super().__init__()

        self.path = path

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 4, 4, 4)
        layout.setSpacing(6)

        self.label = QLabel(Path(path).name)

        self.remove_button = QPushButton("×")
        self.remove_button.setFixedSize(24, 24)

        self.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Fixed,
        )

        layout.addWidget(self.label)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

        self.remove_button.clicked.connect(
            lambda: remove_callback(
                self.path,
                self,
            )
        )