from django.db import models
from django.utils import timezone

class WaitlistUser(models.Model):
    email = models.EmailField(unique=True)
    joined_at = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    
    # New tracking fields
    welcome_email_sent = models.BooleanField(default=False)
    last_email_sent = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Instagram, YouTube, X, direct")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-joined_at']

    def __str__(self):
        return self.email
