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
    
def test_send_with_attachment(mocker, mailer, tmp_path):
    mock_smtp = mocker.patch("email_tool.mailer.smtplib.SMTP")
    mock_connection = mock_smtp.return_value.__enter__.return_value

    attachment = tmp_path / "sample.pdf"
    attachment.write_bytes(b"fake pdf content")

    mailer.send(
        recipient="recipient@example.com",
        subject="Attachment Test",
        body="Hello",
        attachments=[str(attachment)],
    )

    mock_connection.send_message.assert_called_once()

    sent_message = mock_connection.send_message.call_args.args[0]

    assert sent_message.is_multipart()

    attachments = list(sent_message.iter_attachments())

    assert len(attachments) == 1
    assert attachments[0].get_filename() == "sample.pdf"
    assert attachments[0].get_content_type() == "application/pdf"
    assert attachments[0].get_payload(decode=True) == b"fake pdf content"
    
def test_send_with_multiple_attachments(mocker, mailer, tmp_path):
    mock_smtp = mocker.patch("email_tool.mailer.smtplib.SMTP")
    mock_connection = mock_smtp.return_value.__enter__.return_value

    pdf = tmp_path / "sample.pdf"
    txt = tmp_path / "sample.txt"

    pdf.write_bytes(b"pdf")
    txt.write_text("hello")

    mailer.send(
        recipient="recipient@example.com",
        subject="Multiple Attachments",
        body="Hello",
        attachments=[
            str(pdf),
            str(txt),
        ],
    )

    sent_message = mock_connection.send_message.call_args.args[0]
    attachments = list(sent_message.iter_attachments())

    assert len(attachments) == 2
    
def test_send_with_html(mocker, mailer):
    mock_smtp = mocker.patch("email_tool.mailer.smtplib.SMTP")
    mock_connection = mock_smtp.return_value.__enter__.return_value

    mailer.send(
        recipient="recipient@example.com",
        subject="HTML Test",
        body="Hi Adam,\n\nThis is a test email.",
        html_body="<p>Hi Adam,</p><p>This is a test email.</p>",
    )

    mock_connection.send_message.assert_called_once()

    sent_message = mock_connection.send_message.call_args.args[0]

    assert sent_message.is_multipart()

    plain_part = sent_message.get_body(preferencelist=("plain",))
    html_part = sent_message.get_body(preferencelist=("html",))

    assert plain_part is not None
    assert html_part is not None

    assert plain_part.get_content().strip() == "Hi Adam,\n\nThis is a test email."
    assert html_part.get_content().strip() == (
        "<p>Hi Adam,</p><p>This is a test email.</p>"
    )
    assert html_part.get_content_type() == "text/html"