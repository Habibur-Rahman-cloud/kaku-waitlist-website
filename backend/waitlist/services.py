import os
import logging
import requests

logger = logging.getLogger(__name__)

BREVO_API_KEY = os.environ.get('BREVO_API_KEY', '')
BREVO_API_URL = 'https://api.brevo.com/v3/smtp/email'
FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'rahmanbuilds.app@gmail.com')
FROM_NAME = 'Kaku か'


def _send_brevo_email(to_email, subject, html_content):
    """Core function to send a single email via Brevo HTTP API."""
    if not BREVO_API_KEY:
        logger.error("BREVO_API_KEY is not set. Cannot send email.")
        return False

    headers = {
        'accept': 'application/json',
        'api-key': BREVO_API_KEY,
        'content-type': 'application/json',
    }
    payload = {
        'sender': {'name': FROM_NAME, 'email': FROM_EMAIL},
        'to': [{'email': to_email}],
        'subject': subject,
        'htmlContent': html_content,
    }
    try:
        response = requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=10)
        if response.status_code in (200, 201):
            return True
        else:
            logger.error(f"Brevo API error for {to_email}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


WELCOME_EMAIL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Welcome to Kaku</title>
</head>
<body style="margin:0;padding:0;background-color:#0a0a0f;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0a0a0f;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

          <!-- Header / Logo -->
          <tr>
            <td align="center" style="padding-bottom:32px;">
              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:linear-gradient(135deg,#7c3aed,#ec4899);border-radius:16px;padding:14px 22px;">
                    <span style="font-size:26px;font-weight:800;color:#ffffff;letter-spacing:-0.5px;">Kaku か</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Main Card -->
          <tr>
            <td style="background:linear-gradient(145deg,#1a1a2e,#16213e);border-radius:24px;border:1px solid rgba(124,58,237,0.3);overflow:hidden;">

              <!-- Purple top accent bar -->
              <tr>
                <td style="background:linear-gradient(90deg,#7c3aed,#ec4899,#7c3aed);height:4px;display:block;line-height:4px;font-size:0;">&nbsp;</td>
              </tr>

              <!-- Body -->
              <tr>
                <td style="padding:48px 48px 40px;">

                  <!-- Big Kanji Hero -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:32px;">
                    <tr>
                      <td align="center">
                        <div style="background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(236,72,153,0.1));border:1px solid rgba(124,58,237,0.25);border-radius:20px;padding:28px;display:inline-block;">
                          <span style="font-size:72px;line-height:1;">か</span>
                        </div>
                      </td>
                    </tr>
                  </table>

                  <!-- Heading -->
                  <h1 style="margin:0 0 12px;font-size:32px;font-weight:800;color:#ffffff;letter-spacing:-0.5px;text-align:center;line-height:1.2;">
                    You're on the list! 🎉
                  </h1>

                  <p style="margin:0 0 32px;font-size:17px;color:#a0a0b8;line-height:1.6;text-align:center;">
                    Welcome to <strong style="color:#c084fc;">Kaku</strong> — the smarter way to master Japanese Hiragana & Katakana. We'll let you know the moment early access opens.
                  </p>

                  <!-- Divider -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:32px;">
                    <tr>
                      <td style="border-top:1px solid rgba(124,58,237,0.2);height:1px;font-size:0;">&nbsp;</td>
                    </tr>
                  </table>

                  <!-- What's Coming -->
                  <p style="margin:0 0 20px;font-size:13px;font-weight:700;color:#7c3aed;letter-spacing:0.12em;text-transform:uppercase;">What's Coming</p>

                  <!-- Feature 1 -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:16px;">
                    <tr>
                      <td width="44" valign="top">
                        <div style="background:rgba(124,58,237,0.15);border-radius:12px;width:36px;height:36px;text-align:center;line-height:36px;font-size:18px;">✍️</div>
                      </td>
                      <td style="padding-left:14px;" valign="middle">
                        <p style="margin:0;font-size:15px;font-weight:600;color:#e0e0f0;">Stroke-by-stroke tracing</p>
                        <p style="margin:4px 0 0;font-size:13px;color:#7070a0;">Learn the exact stroke order used by native writers</p>
                      </td>
                    </tr>
                  </table>

                  <!-- Feature 2 -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:16px;">
                    <tr>
                      <td width="44" valign="top">
                        <div style="background:rgba(236,72,153,0.12);border-radius:12px;width:36px;height:36px;text-align:center;line-height:36px;font-size:18px;">🧠</div>
                      </td>
                      <td style="padding-left:14px;" valign="middle">
                        <p style="margin:0;font-size:15px;font-weight:600;color:#e0e0f0;">AI-powered spaced repetition</p>
                        <p style="margin:4px 0 0;font-size:13px;color:#7070a0;">Remember characters forever with smart review timing</p>
                      </td>
                    </tr>
                  </table>

                  <!-- Feature 3 -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:40px;">
                    <tr>
                      <td width="44" valign="top">
                        <div style="background:rgba(52,211,153,0.12);border-radius:12px;width:36px;height:36px;text-align:center;line-height:36px;font-size:18px;">⚡</div>
                      </td>
                      <td style="padding-left:14px;" valign="middle">
                        <p style="margin:0;font-size:15px;font-weight:600;color:#e0e0f0;">Full Hiragana in 7 days</p>
                        <p style="margin:4px 0 0;font-size:13px;color:#7070a0;">Proven system that gets beginners reading fast</p>
                      </td>
                    </tr>
                  </table>

                  <!-- CTA Button -->
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td align="center">
                        <a href="https://kaku-waitlist.netlify.app" style="display:inline-block;background:linear-gradient(135deg,#7c3aed,#ec4899);color:#ffffff;font-size:16px;font-weight:700;text-decoration:none;padding:16px 40px;border-radius:14px;letter-spacing:0.01em;">
                          Visit Kaku →
                        </a>
                      </td>
                    </tr>
                  </table>

                </td>
              </tr>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="padding:32px 20px 0;">
              <p style="margin:0 0 8px;font-size:13px;color:#404060;">
                You're receiving this because you joined the Kaku waitlist.
              </p>
              <p style="margin:0;font-size:12px;color:#303050;">
                © 2026 Kaku. Made with ♥ for Japanese learners.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


class EmailService:
    @staticmethod
    def send_welcome_email(to_email: str) -> bool:
        subject = "You're on the Kaku waitlist 🎉"
        return _send_brevo_email(to_email, subject, WELCOME_EMAIL_HTML)

    @staticmethod
    def send_broadcast_email(subject: str, body: str, recipients: list) -> int:
        """Send an email to a list of recipients. Returns count of successes."""
        success_count = 0
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;background:#0a0a0f;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0a0f;padding:40px 20px;">
            <tr><td align="center">
              <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
                <tr>
                  <td align="center" style="padding-bottom:28px;">
                    <div style="background:linear-gradient(135deg,#7c3aed,#ec4899);border-radius:14px;padding:12px 20px;display:inline-block;">
                      <span style="font-size:22px;font-weight:800;color:#fff;">Kaku か</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="background:linear-gradient(145deg,#1a1a2e,#16213e);border-radius:20px;border:1px solid rgba(124,58,237,0.3);padding:40px;">
                    <div style="height:4px;background:linear-gradient(90deg,#7c3aed,#ec4899);border-radius:4px;margin-bottom:32px;"></div>
                    <div style="font-size:16px;color:#c0c0d8;line-height:1.7;white-space:pre-line;">{body}</div>
                    <div style="margin-top:32px;padding-top:24px;border-top:1px solid rgba(124,58,237,0.2);font-size:12px;color:#404060;text-align:center;">
                      © 2026 Kaku. You received this as a Kaku waitlist member.
                    </div>
                  </td>
                </tr>
              </table>
            </td></tr>
          </table>
        </body>
        </html>
        """
        for email in recipients:
            if _send_brevo_email(email, subject, html_body):
                success_count += 1
        return success_count
