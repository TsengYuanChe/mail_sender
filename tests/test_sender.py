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