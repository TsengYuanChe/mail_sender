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
from .validation import validate_recipients


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
    
    valid_recipients, invalid_recipients = validate_recipients(
        recipients
    )
    
    print(f"Recipients: {len(recipients)}")
    print(f"Valid: {len(valid_recipients)}")
    print(f"Invalid: {len(invalid_recipients)}")

    result = send_bulk(
        mailer=mailer,
        recipients=valid_recipients,
        template=template,
        subject="Bulk Email Test",
        body_template="Hi {{ name }},\n\nThis is a test email.",
    )

    print(f"Success: {len(result['success'])}")
    print(f"Failed: {len(result['failed'])}")


if __name__ == "__main__":
    main()