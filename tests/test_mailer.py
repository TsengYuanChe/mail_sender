import pytest

from email_tool.mailer import SMTPMailer

@pytest.fixture
def mailer():
    return SMTPMailer(
        host="smtp.example.com",
        port=587,
        username="test@example.com",
        password="password",
        use_tls=True,
    )

def test_connection(mocker, mailer):
    mock_smtp = mocker.patch("email_tool.mailer.smtplib.SMTP")

    mock_connection = mock_smtp.return_value.__enter__.return_value

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
    
def test_send(mocker, mailer):
    mock_smtp = mocker.patch("email_tool.mailer.smtplib.SMTP")
    mock_connection = mock_smtp.return_value.__enter__.return_value

    mailer.send(
        recipient="recipient@example.com",
        subject="Test Subject",
        body="Hello World",
    )

    mock_smtp.assert_called_once_with(
        "smtp.example.com",
        587,
    )

    mock_connection.starttls.assert_called_once()

    mock_connection.login.assert_called_once_with(
        "test@example.com",
        "password",
    )

    mock_connection.send_message.assert_called_once()

    sent_message = mock_connection.send_message.call_args.args[0]

    assert sent_message["From"] == "test@example.com"
    assert sent_message["To"] == "recipient@example.com"
    assert sent_message["Subject"] == "Test Subject"
    assert sent_message.get_content().strip() == "Hello World"