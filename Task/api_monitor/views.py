from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from .models import APIEndpoint, RTTMeasurement, Alert
from .tasks import monitor_single_endpoint
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging
logger = logging.getLogger('api_monitor')


def dashboard(request):
    """Main dashboard view"""
    try:
        endpoints = APIEndpoint.objects.filter(is_active=True)
        recent_alerts = Alert.objects.filter(resolved=False)[:10]

        # Get latest measurements for each endpoint
        endpoint_stats = []
        for endpoint in endpoints:
            latest_measurement = endpoint.measurements.first()
            avg_rtt_24h = endpoint.measurements.filter(
                timestamp__gte=timezone.now() - timedelta(hours=24)
            ).aggregate(avg_rtt=Avg('rtt_ms'))['avg_rtt'] or 0

            # Determine status
            status = 'unknown'
            if latest_measurement:
                if latest_measurement.error_message:
                    status = 'error'
                elif latest_measurement.rtt_ms <= endpoint.threshold_ms:
                    status = 'healthy'
                else:
                    status = 'warning'

            endpoint_stats.append({
                'endpoint': endpoint,
                'latest_rtt': latest_measurement.rtt_ms if latest_measurement else None,
                'avg_rtt_24h': round(avg_rtt_24h, 2),
                'status': status,
                'last_check': latest_measurement.timestamp if latest_measurement else None,
            })

        context = {
            'endpoint_stats': endpoint_stats,
            'recent_alerts': recent_alerts,
            'total_endpoints': endpoints.count(),
            'active_alerts': recent_alerts.count(),
        }

        return render(request, 'api_monitor/dashboard.html', context)

    except Exception as e:
        # Log the error and show a basic page
        logger.error(f"Dashboard error: {str(e)}")
        return render(request, 'api_monitor/dashboard.html', {
            'endpoint_stats': [],
            'recent_alerts': [],
            'total_endpoints': 0,
            'active_alerts': 0,
            'error': str(e)
        })


def endpoint_detail(request, endpoint_id):
    """Detailed view for a specific endpoint"""
    endpoint = get_object_or_404(APIEndpoint, id=endpoint_id)

    # Get recent measurements (last 100)
    measurements = endpoint.measurements.all()[:100]

    # Get recent alerts
    alerts = endpoint.alerts.all()[:20]

    context = {
        'endpoint': endpoint,
        'measurements': measurements,
        'alerts': alerts,
    }

    return render(request, 'api_monitor/endpoint_detail.html', context)



@csrf_exempt  # Add this decorator
@require_http_methods(["POST"])  # Add this decorator
def trigger_manual_check(request, endpoint_id):
    """Manually trigger monitoring for an endpoint"""
    endpoint = get_object_or_404(APIEndpoint, id=endpoint_id)

    # Trigger the monitoring task
    task = monitor_single_endpoint.delay(endpoint_id)

    return JsonResponse({
        'status': 'success',
        'message': f'Manual check triggered for {endpoint.name}',
        'task_id': task.id
    })
