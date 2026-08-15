import re


EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


def is_valid_email(email: str) -> bool:
    if not email:
        return False

    return bool(
        EMAIL_PATTERN.match(email.strip())
    )


def validate_recipient(
    recipient: dict[str, str],
) -> list[str]:
    errors = []

    name = recipient.get("name", "").strip()
    email = recipient.get("email", "").strip()

    if not name:
        errors.append("missing name")

    if not email:
        errors.append("missing email")
    elif not is_valid_email(email):
        errors.append("invalid email")

    return errors

def validate_recipients(
    recipients: list[dict[str, str]],
) -> tuple[
    list[dict[str, str]],
    list[dict],
]:
    valid = []
    invalid = []

    for recipient in recipients:
        errors = validate_recipient(recipient)

        if errors:
            invalid.append({
                "recipient": recipient,
                "errors": errors,
            })
        else:
            valid.append(recipient)

    return valid, invalid