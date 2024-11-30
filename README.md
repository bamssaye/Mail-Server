# Advanced Email Sender

A Python-based email sending system with support for multiple protocols (SMTP/MX), proxy integration, and customizable templates.

## Project Structure

```
├── Msg/
│   ├── emails-insta.txt    # Target email addresses list
│   ├── fname.txt          # First names for personalization
│   ├── from_email.txt     # Sender email addresses
│   ├── html_type.html     # HTML email template
│   ├── placehold.txt      # Placeholder values for templates
│   └── subject.txt        # Email subject lines
│   └── text_type.txt      # Plain text email template
├── info/
│   ├── dk.pem            # DKIM private key
│   ├── header.json       # Email headers configuration
│   └── smtp.txt          # SMTP server configurations
├── log/
│   ├── error_sended.txt  # Failed delivery logs
│   └── logs.txt          # General operation logs
├── header.py             # Email header management
├── main.py              # Main application entry point
├── send_mx.py           # Direct MX record sending
├── send_smtp.py         # SMTP protocol sending
└── utils.py             # Utility functions
```

## Features

- Multiple sending protocols support (SMTP and direct MX)
- HTML and plain text email templates
- Email personalization with custom fields
- DKIM signing support
- Detailed logging system
- Custom header management
- Error handling and retry mechanism
- Random Tags System
## Configuration Files

### Msg Directory
- `emails-insta.txt`: List of recipient email addresses (one per line)
- `fname.txt`: First names for personalization
- `from_email.txt`: List of sender email addresses
- `html_type.html`: HTML email template with placeholders
- `placehold.txt`: Replacement values for template placeholders
- `subject.txt`: Email subject lines
- `text_type.txt`: Plain text version of email template

### Info Directory
- `dk.pem`: DKIM private key for email signing
- `header.json`: Custom email headers configuration
- `smtp.txt`: SMTP server configurations (host:port:username:password)

### Log Directory
- `error_sended.txt`: Records of failed email deliveries
- `logs.txt`: General operation logs

## Core Components

### main.py
Main entry point for the application. Handles:
- Configuration loading
- Thread management
- Email queue processing
- Error handling

### send_smtp.py
SMTP sending implementation:
- SMTP connection management
- TLS/SSL support
- Rate limiting
- Error handling and retries

### send_mx.py
Direct MX record sending:
- DNS MX record lookup
- Direct server connection
- DKIM signing
- Custom headers

### header.py
Email header management:
- Custom header generation
- DKIM signing integration
- Header validation

### utils.py
Utility functions for:
- File operations
- Template processing
- Logging
- Error handling
- Proxy management

## Usage

1. Configure your settings:
```bash
# Setup SMTP servers
echo "smtp.server.com:587:username:password" > info/smtp.txt

# Add recipient emails
echo "recipient@example.com" > Msg/emails-insta.txt

# Configure sender emails
echo "sender@yourdomain.com" > Msg/from_email.txt
```

2. Run the sender:
```bash
python main.py
```

## Error Handling

The system includes comprehensive error handling:
- SMTP connection failures
- DNS lookup errors
- Template processing errors
- Rate limiting
- Proxy failures

Errors are logged to:
- `log/error_sended.txt` for delivery failures
- `log/logs.txt` for general operations


## Security Notes

- Store sensitive data securely
- Use strong passwords
- Keep DKIM keys private
- Follow email sending best practices
- Respect rate limits
- Comply with anti-spam regulations

## Dependencies

- Python 3.7+
- Required packages:
  ```
  dnspython
  pysocks
  cryptography
  ```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Random Tags System

The email sender supports dynamic content generation using special tags in your templates. These tags are replaced with random or dynamic content when sending emails.

## Pattern Types and Special Variables

### Core Pattern Types
The system supports various pattern types for generating dynamic content. Here's a detailed breakdown:

| Pattern | Source | Description | Example Usage | Example Output |
|---------|--------|-------------|---------------|----------------|
| `N` | `string.digits` | Numbers only | `[4N]` | "5739" |
| `A` | `string.ascii_letters` | Any letters (upper & lower) | `[3A]` | "kMz" |
| `LA` | `string.ascii_lowercase` | Lowercase letters only | `[5LA]` | "abcde" |
| `UA` | `string.ascii_uppercase` | Uppercase letters only | `[4UA]` | "WXYZ" |
| `AN` | `string.ascii_letters + string.digits` | Alphanumeric characters | `[6AN]` | "a7Kp9q" |

### Special Variables

| Variable | Description | Format | Example Output |
|----------|-------------|---------|----------------|
| `FNAME` | First name from fname.txt | `[FNAME]` | "John" (UTF-8 encoded) |
| `SUBJECT` | Subject from subject.txt | `[SUBJECT]` | "Special Offer" (UTF-8 encoded) |
| `DATE` | UTC timestamp | `[DATE]` | "Sat, 30 Nov 2024 14:30:45.000 +0000 (UTC)" |
| `TEXT` | Content from placehold.txt | `[TEXT]` | Custom placeholder content |
| `EID` | Unique identifier | `[EID]` | "550e8400-e29b-41d4-a716-446655440000" |

### Usage Examples

1. Pattern Combinations:
```
[4N] -> "5739"           # 4 random numbers
[3UA] -> "XYZ"          # 3 uppercase letters
[5LA] -> "abcde"        # 5 lowercase letters
[6AN] -> "a7Kp9q"       # 6 alphanumeric characters
```

2. Special Variables in Templates:
```html
<html>
<body>
    <p>Dear [FNAME],</p>
    <p>Message ID: [EID]</p>
    <p>Generated on [DATE]</p>
    <p>[TEXT]</p>
</body>
</html>
```

### Important Notes

1. Encoding:
   - All special variables (FNAME, SUBJECT) are UTF-8 encoded
   - Pattern-generated content uses ASCII characters only

2. Date Format:
   - DATE uses UTC timezone
   - Format follows RFC 2822 standard
   - Includes microseconds and timezone information

3. UUID Generation:
   - EID uses UUID version 4 (random)
   - Guarantees uniqueness across messages
