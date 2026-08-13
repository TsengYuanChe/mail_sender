from .config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_USE_TLS,
)
from .mailer import SMTPMailer
from .template import load_template, render_template


def main():
    mailer = SMTPMailer(
        host=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        use_tls=SMTP_USE_TLS,
    )
    
    html = load_template("samples/template.html")
    html = render_template(html, "Adam")

    mailer.send(
        recipient=SMTP_USERNAME,
        subject="HTML Test",
        body="Hi Adam,\n\nThis is a test email.",
        html_body=html,
    )

    print("Email sent successfully.")


if __name__ == "__main__":
    main()