import keyring

from .mailer import SMTPMailer

SERVICE_NAME = "mail-sender"

def login(
    host: str,
    port: int,
    username: str,
    password: str,
    use_tls: bool = True,
) -> SMTPMailer:
    mailer = SMTPMailer(
        host=host,
        port=port,
        username=username,
        password=password,
        use_tls=use_tls,
    )

    mailer.test_connection()

    return mailer

def save_credential(
    username: str,
    password: str,
) -> None:
    keyring.set_password(
        SERVICE_NAME,
        username,
        password,
    )


def get_credential(
    username: str,
) -> str | None:
    return keyring.get_password(
        SERVICE_NAME,
        username,
    )
    
def delete_credential(
    username: str,
) -> None:
    keyring.delete_password(
        SERVICE_NAME,
        username,
    )