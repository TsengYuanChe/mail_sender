from email_tool.recipients import load_recipients


def test_load_recipients(tmp_path):
    csv_file = tmp_path / "recipients.csv"

    csv_file.write_text(
        "name,email\n"
        "Adam,adam@example.com\n"
        "Amy,amy@example.com\n",
        encoding="utf-8",
    )

    result = load_recipients(str(csv_file))

    assert result == [
        {
            "name": "Adam",
            "email": "adam@example.com",
        },
        {
            "name": "Amy",
            "email": "amy@example.com",
        },
    ]