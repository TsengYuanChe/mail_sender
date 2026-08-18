from PySide6.QtWidgets import QApplication

from email_tool.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USE_TLS,
)

from .login_window import LoginWindow
from .main_window import MainWindow


def run_gui():
    app = QApplication([])

    login_window = LoginWindow(
        host=SMTP_HOST,
        port=SMTP_PORT,
        use_tls=SMTP_USE_TLS,
    )

    main_window = None

    def handle_login_success(mailer):
        nonlocal main_window

        main_window = MainWindow(
            mailer=mailer
        )

        main_window.show()
        login_window.close()

    login_window.login_success.connect(
        handle_login_success
    )

    login_window.show()

    app.exec()