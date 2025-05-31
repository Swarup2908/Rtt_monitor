import requests
import time
import logging
from celery import shared_task
from django.utils import timezone
from .models import APIEndpoint, RTTMeasurement, Alert

logger = logging.getLogger('api_monitor')


@shared_task
def monitor_all_endpoints():
    """Monitor all active API endpoints"""
    endpoints = APIEndpoint.objects.filter(is_active=True)

    logger.info(f"Starting monitoring cycle for {endpoints.count()} endpoints")

    for endpoint in endpoints:
        monitor_single_endpoint.delay(endpoint.id)

    return f"Dispatched monitoring tasks for {endpoints.count()} endpoints"


@shared_task
def monitor_single_endpoint(endpoint_id):
    """Monitor a single API endpoint for RTT"""
    try:
        endpoint = APIEndpoint.objects.get(id=endpoint_id)

        # Measure RTT
        start_time = time.time()

        try:
            response = requests.get(endpoint.url, timeout=30)
            end_time = time.time()

            rtt_ms = (end_time - start_time) * 1000  # Convert to milliseconds
            status_code = response.status_code
            error_message = None

            logger.info(f"RTT for {endpoint.name}: {rtt_ms:.2f}ms")

        except requests.exceptions.RequestException as e:
            end_time = time.time()
            rtt_ms = (end_time - start_time) * 1000
            status_code = None
            error_message = str(e)

            logger.error(f"Error monitoring {endpoint.name}: {error_message}")

        # Save measurement
        measurement = RTTMeasurement.objects.create(
            endpoint=endpoint,
            rtt_ms=rtt_ms,
            status_code=status_code,
            error_message=error_message
        )

        # Check threshold and create alerts
        if error_message:
            create_alert(endpoint, 'API_ERROR', f"API Error: {error_message}", rtt_ms)
        elif rtt_ms > endpoint.threshold_ms:
            create_alert(endpoint, 'THRESHOLD_BREACH',
                         f"RTT {rtt_ms:.2f}ms exceeded threshold {endpoint.threshold_ms}ms",
                         rtt_ms)

        return f"Monitored {endpoint.name}: RTT={rtt_ms:.2f}ms"

    except APIEndpoint.DoesNotExist:
        logger.error(f"Endpoint with ID {endpoint_id} not found")
        return f"Endpoint {endpoint_id} not found"
    except Exception as e:
        logger.error(f"Unexpected error monitoring endpoint {endpoint_id}: {str(e)}")
        return f"Error: {str(e)}"


def create_alert(endpoint, alert_type, message, rtt_value=None):
    """Create an alert for threshold breach or error"""
    alert = Alert.objects.create(
        endpoint=endpoint,
        alert_type=alert_type,
        message=message,
        rtt_value=rtt_value,
        threshold_value=endpoint.threshold_ms
    )

    # Log the alert
    log_message = f"🚨 ALERT: {alert_type} for {endpoint.name} - {message}"
    logger.warning(log_message)
    print(log_message)  # Also print to console for immediate visibility

    return alert