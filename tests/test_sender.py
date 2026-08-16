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
    
def test_send_bulk_callbacks():
    mailer = Mock()

    on_sending = Mock()
    on_success = Mock()
    on_failed = Mock()

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

    mailer.send.side_effect = [
        None,
        Exception("Send failed"),
    ]

    send_bulk(
        mailer=mailer,
        recipients=recipients,
        template="<p>Hi {{ name }}</p>",
        subject="Test",
        body_template="Hi {{ name }}",
        on_sending=on_sending,
        on_success=on_success,
        on_failed=on_failed,
    )

    assert on_sending.call_count == 2

    on_sending.assert_any_call(
        "Adam",
        "adam@example.com",
    )
    on_sending.assert_any_call(
        "Amy",
        "amy@example.com",
    )

    on_success.assert_called_once_with(
        "Adam",
        "adam@example.com",
    )

    on_failed.assert_called_once_with(
        "Amy",
        "amy@example.com",
        "Send failed",
    )