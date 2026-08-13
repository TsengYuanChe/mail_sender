from .template import render_template


def send_bulk(
    mailer,
    recipients: list[dict[str, str]],
    template: str,
    subject: str,
    body_template: str,
    attachments: list[str] | None = None,
) -> None:
    for recipient in recipients:
        name = recipient["name"]
        email = recipient["email"]

        html_body = render_template(
            template,
            name,
        )

        body = body_template.replace(
            "{{ name }}",
            name,
        )

        mailer.send(
            recipient=email,
            subject=subject,
            body=body,
            html_body=html_body,
            attachments=attachments,
        )