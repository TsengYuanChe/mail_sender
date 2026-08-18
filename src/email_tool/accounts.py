import json
from pathlib import Path

from PySide6.QtCore import QStandardPaths


def get_accounts_path() -> Path:
    data_dir = Path(
        QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return data_dir / "accounts.json"


def list_accounts() -> list[str]:
    path = get_accounts_path()

    if not path.exists():
        return []

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def add_account(
    username: str,
) -> None:
    accounts = list_accounts()

    if username in accounts:
        return

    accounts.append(username)

    _save_accounts(accounts)


def remove_account(
    username: str,
) -> None:
    accounts = list_accounts()

    if username not in accounts:
        return

    accounts.remove(username)

    _save_accounts(accounts)


def _save_accounts(
    accounts: list[str],
) -> None:
    path = get_accounts_path()

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            accounts,
            file,
            indent=2,
        )
    