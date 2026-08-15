from .config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_USE_TLS,
)
from .mailer import SMTPMailer
from .recipients import load_recipients
from .template import load_template
from .sender import send_bulk


def main():
    mailer = SMTPMailer(
        host=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        use_tls=SMTP_USE_TLS,
    )

    recipients = load_recipients(
        "samples/recipients.csv"
    )

    template = load_template(
        "samples/template.html"
    )

    result = send_bulk(
        mailer=mailer,
        recipients=recipients,
        template=template,
        subject="Bulk Email Test",
        body_template="Hi {{ name }},\n\nThis is a test email.",
    )

    print(f"Success: {len(result['success'])}")
    print(f"Failed: {len(result['failed'])}")


if __name__ == "__main__":
    main()