# Mail Sender

A simple desktop application for sending personalized bulk emails
using SMTP.

## Features

- Send personalized emails to multiple recipients
- Import recipients from CSV
- Use HTML email templates
- Add multiple attachments
- Validate recipient data before sending
- Preview emails before sending
- View real-time sending results
- Secure credential storage on supported platforms
- Support for macOS and Windows

## Download

Download the latest version from the **Releases** page.

Available builds:

- macOS Apple Silicon (arm64)
- Windows x64

The packaged application does not require Python to be installed.

> macOS builds are currently unsigned. Credential saving is disabled
> in the packaged macOS version.

## How to Use

### 1. Login

Enter your email address and App Password.

For Gmail, create and use a Google App Password instead of your
regular account password.

If **Remember account** is available and enabled, the credential will be stored
using the operating system's secure credential storage.

> **Note:** Remember Account is currently disabled in packaged macOS builds.

### 2. Prepare Recipients

Create a CSV file containing `name` and `email` columns.

Example:

| name | email |
|------|-------|
| Adam | adam@example.com |
| Amy | amy@example.com |
| John | john@example.com |

Invalid or incomplete recipients will automatically be excluded
before sending.

### 3. Prepare an Email Template

Create an HTML template.

Use `{{ name }}` to insert the recipient's name.

Example:

```html
<p>Hi {{ name }},</p>

<p>This is a bulk email test.</p>

<p>
Best Regards,<br>
Adam
</p>
```

### 4. Select Files

In the main window:

1. Select the recipients CSV file.
2. Select the HTML email template.
3. Add attachments if needed.
4. Enter the email subject.

### 5. Preview

Click **Preview** to review the email before sending.

The preview window displays:

- Email subject
- Rendered email content
- Attachments
- Total number of recipients
- Number of valid recipients
- Number of invalid recipients

### 6. Send Emails

Click **Send Emails** to start sending.

The result window displays the status of each recipient:

- ⏳ **Sending** — Email is being sent
- ✅ **Success** — Email was sent successfully
- ❌ **Failed** — Email could not be sent

Invalid recipients are listed separately and will automatically be excluded from sending.

## CSV Format

The recipients CSV file must contain the following columns:

| Column | Description |
| --- | --- |
| `name` | Recipient name |
| `email` | Recipient email address |

Example:

```csv
name,email
Adam,adam@example.com
Amy,amy@example.com
John,john@example.com
```

## Template Variables

The following variable is currently supported in HTML email templates:

| Variable | Description |
| --- | --- |
| `{{ name }}` | Recipient name |

## Notes

- An internet connection is required to send emails.
- SMTP authentication must be available for the email account.
- Gmail users should use an **App Password** instead of their regular account password.
- Use **Preview** to verify the email content and recipient list before sending.
- Invalid recipients are automatically excluded from sending.

## Built With

- Python
- PySide6
- Jinja2
- keyring
- pytest
- PyInstaller
- GitHub Actions