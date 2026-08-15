from email_tool.validation import is_valid_email, validate_recipient, validate_recipients


def test_valid_email():
    assert is_valid_email(
        "adam@example.com"
    )


def test_invalid_email():
    assert not is_valid_email("abc")


def test_missing_email():
    result = validate_recipient({
        "name": "Amy",
        "email": "",
    })

    assert result == ["missing email"]


def test_valid_recipient():
    result = validate_recipient({
        "name": "Adam",
        "email": "adam@example.com",
    })

    assert result == []
    
def test_validate_recipients():
    recipients = [
        {
            "name": "Adam",
            "email": "adam@example.com",
        },
        {
            "name": "Amy",
            "email": "",
        },
        {
            "name": "John",
            "email": "abc",
        },
    ]

    valid, invalid = validate_recipients(recipients)

    assert len(valid) == 1
    assert len(invalid) == 2

    assert valid[0] == {
        "name": "Adam",
        "email": "adam@example.com",
    }

    assert invalid[0]["recipient"] == {
        "name": "Amy",
        "email": "",
    }
    assert invalid[0]["errors"] == ["missing email"]

    assert invalid[1]["recipient"] == {
        "name": "John",
        "email": "abc",
    }
    assert invalid[1]["errors"] == ["invalid email"]