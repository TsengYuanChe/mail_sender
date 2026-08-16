from PySide6.QtCore import QObject, Signal, Slot

from email_tool.sender import send_bulk


class SendWorker(QObject):
    sending = Signal(str, str)
    success = Signal(str, str)
    failed = Signal(str, str, str)
    finished = Signal()

    def __init__(
        self,
        mailer,
        recipients: list[dict[str, str]],
        template: str,
        subject: str,
        body_template: str,
        attachments: list[str] | None = None,
    ):
        super().__init__()

        self.mailer = mailer
        self.recipients = recipients
        self.template = template
        self.subject = subject
        self.body_template = body_template
        self.attachments = attachments

    @Slot()
    def run(self):
        send_bulk(
            mailer=self.mailer,
            recipients=self.recipients,
            template=self.template,
            subject=self.subject,
            body_template=self.body_template,
            attachments=self.attachments,
            on_sending=self.sending.emit,
            on_success=self.success.emit,
            on_failed=self.failed.emit,
        )

        self.finished.emit()