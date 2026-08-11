import smtplib
import mimetypes
from pathlib import Path
from email.message import EmailMessage


class SMTPMailer:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool = True,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def test_connection(self) -> None:
        with smtplib.SMTP(self.host, self.port) as smtp:
            if self.use_tls:
                smtp.starttls()

            smtp.login(
                self.username,
                self.password,
            )

    def send(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: list[str] | None = None,
    ) -> None:
        message = EmailMessage()

        message["From"] = self.username
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)
        
        if attachments:
            for attachment in attachments:
                path = Path(attachment)
                mime_type, _ = mimetypes.guess_type(path)
                
                if mime_type is None:
                    main_type, sub_type = "application", "octet-stream"
                else:
                    main_type, sub_type = mime_type.split("/", 1)

                with path.open("rb") as file:
                    message.add_attachment(
                        file.read(),
                        maintype=main_type,
                        subtype=sub_type,
                        filename=path.name,
                    )

        with smtplib.SMTP(self.host, self.port) as smtp:
            if self.use_tls:
                smtp.starttls()

            smtp.login(
                self.username,
                self.password,
            )

            smtp.send_message(message)