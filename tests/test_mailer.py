from email_tool.mailer import SMTPMailer


def test_connection(mocker):
    mock_smtp = mocker.patch("email_tool.mailer.smtplib.SMTP")

    mock_connection = mock_smtp.return_value.__enter__.return_value

    mailer = SMTPMailer(
        host="smtp.example.com",
        port=587,
        username="test@example.com",
        password="password",
        use_tls=True,
    )

    mailer.test_connection()

    mock_smtp.assert_called_once_with(
        "smtp.example.com",
        587,
    )

    mock_connection.starttls.assert_called_once()

    mock_connection.login.assert_called_once_with(
        "test@example.com",
        "password",
    )
    
def test_connection_without_tls(mocker):
    mock_smtp = mocker.patch("email_tool.mailer.smtplib.SMTP")
    mock_connection = mock_smtp.return_value.__enter__.return_value

    mailer = SMTPMailer(
        host="smtp.example.com",
        port=587,
        username="test@example.com",
        password="password",
        use_tls=False,
    )

    mailer.test_connection()

    mock_smtp.assert_called_once_with(
        "smtp.example.com",
        587,
    )

    mock_connection.starttls.assert_not_called()

    mock_connection.login.assert_called_once_with(
        "test@example.com",
        "password",
    )