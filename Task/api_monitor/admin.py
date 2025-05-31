from django.contrib import admin
from .models import APIEndpoint, RTTMeasurement, Alert

@admin.register(APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'threshold_ms', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'url']

@admin.register(RTTMeasurement)
class RTTMeasurementAdmin(admin.ModelAdmin):
    list_display = ['endpoint', 'rtt_ms', 'status_code', 'timestamp']
    list_filter = ['endpoint', 'timestamp', 'status_code']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['endpoint', 'alert_type', 'rtt_value', 'threshold_value', 'resolved', 'created_at']
    list_filter = ['alert_type', 'resolved', 'created_at', 'endpoint']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
from django.contrib import admin

# Register your models here.
