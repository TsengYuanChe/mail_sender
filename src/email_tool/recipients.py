import csv
from pathlib import Path


def load_recipients(path: str) -> list[dict[str, str]]:
    recipients = []

    with Path(path).open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            recipients.append(dict(row))

    return recipients