import json

from email_tool import accounts


def test_list_accounts_when_file_does_not_exist(mocker, tmp_path):
    accounts_file = tmp_path / "accounts.json"

    mocker.patch(
        "email_tool.accounts.get_accounts_path",
        return_value=accounts_file,
    )

    result = accounts.list_accounts()

    assert result == []


def test_add_account(mocker, tmp_path):
    accounts_file = tmp_path / "accounts.json"

    mocker.patch(
        "email_tool.accounts.get_accounts_path",
        return_value=accounts_file,
    )

    accounts.add_account(
        "adam@example.com"
    )

    result = json.loads(
        accounts_file.read_text(
            encoding="utf-8"
        )
    )

    assert result == [
        "adam@example.com"
    ]


def test_add_duplicate_account(mocker, tmp_path):
    accounts_file = tmp_path / "accounts.json"

    mocker.patch(
        "email_tool.accounts.get_accounts_path",
        return_value=accounts_file,
    )

    accounts.add_account(
        "adam@example.com"
    )

    accounts.add_account(
        "adam@example.com"
    )

    result = accounts.list_accounts()

    assert result == [
        "adam@example.com"
    ]


def test_remove_account(mocker, tmp_path):
    accounts_file = tmp_path / "accounts.json"

    mocker.patch(
        "email_tool.accounts.get_accounts_path",
        return_value=accounts_file,
    )

    accounts.add_account(
        "adam@example.com"
    )

    accounts.add_account(
        "amy@example.com"
    )

    accounts.remove_account(
        "adam@example.com"
    )

    result = accounts.list_accounts()

    assert result == [
        "amy@example.com"
    ]