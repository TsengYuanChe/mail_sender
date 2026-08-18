import smtplib

import pytest

from email_tool.login import (
    login,
    save_credential,
    get_credential,
    delete_credential,
)


def test_login(mocker):
    mock_mailer_class = mocker.patch(
        "email_tool.login.SMTPMailer"
    )

    mock_mailer = mock_mailer_class.return_value

    result = login(
        host="smtp.example.com",
        port=587,
        username="adam@example.com",
        password="password123",
        use_tls=True,
    )

    mock_mailer_class.assert_called_once_with(
        host="smtp.example.com",
        port=587,
        username="adam@example.com",
        password="password123",
        use_tls=True,
    )

    mock_mailer.test_connection.assert_called_once()

    assert result == mock_mailer
    
def test_login_failed(mocker):
    mock_mailer_class = mocker.patch(
        "email_tool.login.SMTPMailer"
    )

    mock_mailer = mock_mailer_class.return_value

    mock_mailer.test_connection.side_effect = (
        smtplib.SMTPAuthenticationError(
            535,
            b"Authentication failed",
        )
    )

    with pytest.raises(
        smtplib.SMTPAuthenticationError
    ):
        login(
            host="smtp.example.com",
            port=587,
            username="adam@example.com",
            password="wrong-password",
            use_tls=True,
        )
        
def test_save_credential(mocker):
    mock_set_password = mocker.patch(
        "email_tool.login.keyring.set_password"
    )

    save_credential(
        "adam@example.com",
        "password123",
    )

    mock_set_password.assert_called_once_with(
        "mail-sender",
        "adam@example.com",
        "password123",
    )


def test_get_credential(mocker):
    mock_get_password = mocker.patch(
        "email_tool.login.keyring.get_password",
        return_value="password123",
    )

    result = get_credential(
        "adam@example.com"
    )

    mock_get_password.assert_called_once_with(
        "mail-sender",
        "adam@example.com",
    )

    assert result == "password123"
    
def test_delete_credential(mocker):
    mock_delete_password = mocker.patch(
        "email_tool.login.keyring.delete_password"
    )

    delete_credential(
        "adam@example.com"
    )

    mock_delete_password.assert_called_once_with(
        "mail-sender",
        "adam@example.com",
    )