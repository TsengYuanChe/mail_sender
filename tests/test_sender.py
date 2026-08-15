from unittest.mock import Mock

from email_tool.sender import send_bulk


def test_send_bulk():
    mailer = Mock()

    recipients = [
        {
            "name": "Adam",
            "email": "adam@example.com",
        },
        {
            "name": "Amy",
            "email": "amy@example.com",
        },
    ]

    template = "<p>Hi {{ name }},</p>"

    send_bulk(
        mailer=mailer,
        recipients=recipients,
        template=template,
        subject="Test Email",
        body_template="Hi {{ name }},",
    )

    assert mailer.send.call_count == 2
    
def test_send_bulk_continues_when_one_email_fails():
    mailer = Mock()

    mailer.send.side_effect = [
        None,
        Exception("Send failed"),
        None,
    ]

    recipients = [
        {"name": "Adam", "email": "adam@example.com"},
        {"name": "Amy", "email": "amy@example.com"},
        {"name": "John", "email": "john@example.com"},
    ]

    result = send_bulk(
        mailer=mailer,
        recipients=recipients,
        template="<p>Hi {{ name }}</p>",
        subject="Test",
        body_template="Hi {{ name }}",
    )

    assert mailer.send.call_count == 3

    assert len(result["success"]) == 2
    assert len(result["failed"]) == 1

    assert result["failed"][0]["email"] == "amy@example.com"
    assert result["failed"][0]["error"] == "Send failed"