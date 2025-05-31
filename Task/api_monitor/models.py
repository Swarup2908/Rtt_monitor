from django.db import models
from django.utils import timezone


class APIEndpoint(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    threshold_ms = models.FloatField(help_text="RTT threshold in milliseconds")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.url}"


class RTTMeasurement(models.Model):
    endpoint = models.ForeignKey(APIEndpoint, on_delete=models.CASCADE, related_name='measurements')
    rtt_ms = models.FloatField(help_text="Round trip time in milliseconds")
    status_code = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.endpoint.name} - {self.rtt_ms}ms at {self.timestamp}"


class Alert(models.Model):
    ALERT_TYPES = [
        ('THRESHOLD_BREACH', 'Threshold Breach'),
        ('API_ERROR', 'API Error'),
        ('TIMEOUT', 'Timeout'),
    ]

    endpoint = models.ForeignKey(APIEndpoint, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    rtt_value = models.FloatField(null=True, blank=True)
    threshold_value = models.FloatField(null=True, blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.alert_type} - {self.endpoint.name} at {self.created_at}"


from django.db import models

# Create your models here.
