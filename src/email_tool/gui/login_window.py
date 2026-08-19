import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QCheckBox,
    QGroupBox,
    QMessageBox,
    QHBoxLayout
)

from email_tool.accounts import (
    list_accounts,
    add_account,
    remove_account,
)
from email_tool.login import (
    login,
    get_credential,
    save_credential,
    delete_credential,
)


class LoginWindow(QWidget):
    login_success = Signal(object)

    def __init__(
        self,
        host: str,
        port: int,
        use_tls: bool = True,
    ):
        super().__init__()

        self.host = host
        self.port = port
        self.use_tls = use_tls

        self.setWindowTitle("Mail Sender - Login")
        self.resize(500, 400)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Saved account
        saved_group = QGroupBox("Saved Account")
        saved_layout = QVBoxLayout()

        self.account_combo = QComboBox()

        self.saved_login_button = QPushButton(
            "Login with Saved Account"
        )
        
        self.remove_account_button = QPushButton(
            "Remove"
        )
        
        account_row = QHBoxLayout()

        account_row.addWidget(self.account_combo, 1)
        account_row.addWidget(self.remove_account_button)

        saved_layout.addLayout(account_row)
        saved_layout.addWidget(self.saved_login_button)
        
        saved_group.setLayout(saved_layout) 

        # New account
        new_group = QGroupBox("New Account")
        new_layout = QVBoxLayout()

        new_layout.addWidget(QLabel("Email"))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(
            "example@gmail.com"
        )

        new_layout.addWidget(self.username_input)

        new_layout.addWidget(QLabel("App Password"))

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        new_layout.addWidget(self.password_input)

        self.remember_checkbox = QCheckBox(
            "Remember account"
        )
        
        is_frozen = getattr(sys, "frozen", False)
        
        if sys.platform == "darwin" and is_frozen:
            self.remember_checkbox.setChecked(False)
            self.remember_checkbox.setEnabled(False)
            self.remember_checkbox.setToolTip(
                "Remember account is unavailable in this macOS build."
            )

        new_layout.addWidget(self.remember_checkbox)

        self.login_button = QPushButton("Login")

        new_layout.addWidget(self.login_button)

        new_group.setLayout(new_layout)

        main_layout.addWidget(saved_group)
        main_layout.addWidget(new_group)

        self.setLayout(main_layout)

        self.load_accounts()
        
        self.remove_account_button.clicked.connect(
            self.remove_saved_account
        )

        self.saved_login_button.clicked.connect(
            self.login_saved_account
        )

        self.login_button.clicked.connect(
            self.login_new_account
        )
        
    def load_accounts(self):
        self.account_combo.clear()

        accounts = list_accounts()

        self.account_combo.addItems(accounts)

        has_accounts = bool(accounts)

        self.account_combo.setEnabled(has_accounts)
        self.saved_login_button.setEnabled(has_accounts)
        self.remove_account_button.setEnabled(has_accounts)
        
    def login_new_account(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Login",
                "Email and password are required.",
            )
            return

        try:
            mailer = login(
                host=self.host,
                port=self.port,
                username=username,
                password=password,
                use_tls=self.use_tls,
            )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Login Failed",
                str(exc),
            )
            return

        if self.remember_checkbox.isChecked():
            try:
                save_credential(
                    username,
                    password,
                )

                add_account(username)
            
            except Exception as exc:
                QMessageBox.critical(
                    self,
                    "Save Credential Failed",
                    str(exc),
                )
                return

        self.password_input.clear()
        self.login_success.emit(mailer)
        
    def login_saved_account(self):
        username = self.account_combo.currentText()

        if not username:
            return

        password = get_credential(username)

        if not password:
            QMessageBox.warning(
                self,
                "Login",
                "Saved credential was not found.",
            )
            return

        try:
            mailer = login(
                host=self.host,
                port=self.port,
                username=username,
                password=password,
                use_tls=self.use_tls,
            )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Login Failed",
                str(exc),
            )
            return

        self.password_input.clear()
        self.login_success.emit(mailer)
        
    def remove_saved_account(self):
        username = self.account_combo.currentText()

        if not username:
            return

        reply = QMessageBox.question(
            self,
            "Remove Account",
            f"Remove saved account {username}?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            delete_credential(username)
        except Exception:
            pass

        remove_account(username)

        self.load_accounts()