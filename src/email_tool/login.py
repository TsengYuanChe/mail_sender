from .mailer import SMTPMailer


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