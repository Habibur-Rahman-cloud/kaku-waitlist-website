import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_welcome_email(email):
        subject = "Welcome to Kaku! 🎌 You're on the list"
        
        # Professional HTML Template
        html_content = f"""
        <html>
        <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #0a0612; color: #f8f4ff; margin: 0; padding: 40px 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #130e20; border: 1px solid #2a2438; border-radius: 16px; padding: 40px; text-align: center;">
                <h1 style="color: #a855f7; font-size: 28px; margin-bottom: 10px;">Welcome to Kaku <span style="font-size: 20px;">かく</span></h1>
                <p style="font-size: 16px; line-height: 1.6; color: #d1d5db; margin-bottom: 24px;">
                    Hi there,<br><br>
                    You are officially on the waitlist! 🎉 We're thrilled to have you join us on this journey to master Japanese writing.
                </p>
                <div style="background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 24px;">
                    <p style="font-size: 14px; color: #a855f7; margin: 0;"><strong>What's next?</strong></p>
                    <p style="font-size: 14px; color: #d1d5db; margin: 10px 0 0 0;">
                        We are currently polishing the app to give you the best experience possible. You'll be the first to know the moment we launch so you can claim your early access.
                    </p>
                </div>
                <p style="font-size: 14px; color: #9ca3af;">
                    Keep an eye on this inbox.<br>
                    Cheers,<br>
                    <strong>The Kaku Team</strong>
                </p>
            </div>
        </body>
        </html>
        """
        
        # Fallback text content for clients that don't support HTML
        text_content = strip_tags(html_content)

        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            return True
        except Exception as e:
            logger.error(f"Failed to send welcome email to {email}: {e}")
            return False

    @staticmethod
    def send_broadcast_email(subject, body, recipients):
        success_count = 0
        
        # Simple HTML wrapper for broadcasts
        for recipient in recipients:
            html_content = f"""
            <html>
            <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #0a0612; color: #f8f4ff; margin: 0; padding: 40px 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #130e20; border: 1px solid #2a2438; border-radius: 16px; padding: 40px;">
                    <div style="font-size: 16px; line-height: 1.6; color: #d1d5db; white-space: pre-wrap;">
                        {body}
                    </div>
                </div>
            </body>
            </html>
            """
            text_content = strip_tags(body)

            try:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send broadcast email to {recipient}: {e}")
        return success_count
