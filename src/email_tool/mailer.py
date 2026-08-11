import smtplib
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
    ) -> None:
        message = EmailMessage()

        message["From"] = self.username
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(self.host, self.port) as smtp:
            if self.use_tls:
                smtp.starttls()

            smtp.login(
                self.username,
                self.password,
            )

            smtp.send_message(message)