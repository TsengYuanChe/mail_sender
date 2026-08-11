from .config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_USE_TLS,
)
from .mailer import SMTPMailer


def main():
    mailer = SMTPMailer(
        host=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        use_tls=SMTP_USE_TLS,
    )

    mailer.test_connection()

    print("SMTP authentication successful.")


if __name__ == "__main__":
    main()