from email_tool.recipients import load_recipients


def test_load_recipients(tmp_path):
    csv_file = tmp_path / "recipients.csv"

    csv_file.write_text(
        "name,email,company,position\n"
        "Adam,adam@example.com,OpenAI,Engineer\n"
        "Amy,amy@example.com,Example Inc,Manager\n",
        encoding="utf-8",
    )

    result = load_recipients(str(csv_file))

    assert result == [
        {
            "name": "Adam",
            "email": "adam@example.com",
            "company": "OpenAI",
            "position": "Engineer",
        },
        {
            "name": "Amy",
            "email": "amy@example.com",
            "company": "Example Inc",
            "position": "Manager",
        },
    ]
    
def test_load_recipients_without_name(tmp_path):
    csv_file = tmp_path / "recipients.csv"

    csv_file.write_text(
        "email,company\n"
        "adam@example.com,OpenAI\n",
        encoding="utf-8",
    )

    result = load_recipients(str(csv_file))

    assert result == [
        {
            "email": "adam@example.com",
            "company": "OpenAI",
        }
    ]
