from unittest.mock import Mock

from email_tool.sender import send_bulk


def test_send_bulk():
    mailer = Mock()

    recipients = [
        {
            "name": "Adam",
            "email": "adam@example.com",
            "company": "OpenAI",
        },
        {
            "name": "Amy",
            "email": "amy@example.com",
            "company": "Example Inc",
        },
    ]

    template = (
        "<p>Hi {{ name }},</p>"
        "<p>Company: {{ company }}</p>"
    )

    send_bulk(
        mailer=mailer,
        recipients=recipients,
        template=template,
        subject="Test Email",
        body_template="Hi {{ name }} from {{ company }}",
    )

    assert mailer.send.call_count == 2

    first_call = mailer.send.call_args_list[0]
    second_call = mailer.send.call_args_list[1]

    assert first_call.kwargs["recipient"] == "adam@example.com"
    assert first_call.kwargs["html_body"] == (
        "<p>Hi Adam,</p>"
        "<p>Company: OpenAI</p>"
    )
    assert first_call.kwargs["body"] == (
        "Hi Adam from OpenAI"
    )

    assert second_call.kwargs["recipient"] == "amy@example.com"
    assert second_call.kwargs["html_body"] == (
        "<p>Hi Amy,</p>"
        "<p>Company: Example Inc</p>"
    )
    assert second_call.kwargs["body"] == (
        "Hi Amy from Example Inc"
    )
    
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
    
def test_send_bulk_without_name():
    mailer = Mock()

    recipients = [
        {
            "email": "adam@example.com",
            "company": "OpenAI",
        },
    ]

    send_bulk(
        mailer=mailer,
        recipients=recipients,
        template="<p>{{ company }}</p>",
        subject="Test",
        body_template="{{ company }}",
    )

    mailer.send.assert_called_once()

    sent_call = mailer.send.call_args

    assert sent_call.kwargs["recipient"] == "adam@example.com"
    assert sent_call.kwargs["html_body"] == "<p>OpenAI</p>"
    
