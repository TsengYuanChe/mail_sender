from collections.abc import Callable

from .template import render_template


def send_bulk(
    mailer,
    recipients: list[dict[str, str]],
    template: str,
    subject: str,
    body_template: str,
    attachments: list[str] | None = None,
    on_sending: Callable[[str, str], None] | None = None,
    on_success: Callable[[str, str], None] | None = None,
    on_failed: Callable[[str, str, str], None] | None = None,
) -> None:
    result = {
        "success": [],
        "failed": [],
    }
    
    for recipient in recipients:
        email = recipient["email"]
        name = recipient.get("name", email)
        
        if on_sending:
            on_sending(name, email)

        html_body = render_template(template, recipient)
        body = render_template(body_template, recipient)

        try: 
            mailer.send(
                recipient=email,
                subject=subject,
                body=body,
                html_body=html_body,
                attachments=attachments,
            )
            
            result["success"].append({
                "name": name,
                "email": email,
            })
            
            if on_success:
                on_success(name, email)
        
        except Exception as e:
            error = str(e)
            
            result["failed"].append({
                "name": name,
                "email": email,
                "error": error,
            })
            
            if on_failed:
                on_failed(name, email, error)
    
    return result