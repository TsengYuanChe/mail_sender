import smtplib

import pytest

from email_tool.login import login


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