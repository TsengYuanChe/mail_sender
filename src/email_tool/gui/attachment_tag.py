from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
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

        self.label = QLabel(Path(path).name)
        self.remove_button = QPushButton("×")

        layout.addWidget(self.label)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

        self.remove_button.clicked.connect(
            lambda: remove_callback(
                self.path,
                self,
            )
        )