from datetime import datetime, timedelta

from django.core.cache import cache
from django.http import HttpResponse
from django.utils import timezone

from django.http import Http404

class UnderMaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        raise Http404

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client's IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Get the number of requests made in the last minute
        request_count = cache.get(ip_address, 0)
        if request_count >= 400:
            # If the number of requests is too high, return a 403 Forbidden response
            return HttpResponse(status=400)

        # Increment the request count for the IP address
        cache.set(ip_address, request_count + 1, timeout=120)

        response = self.get_response(request)
        return response

class UpdateIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.META.get('REMOTE_ADDR'))
        if request.user.is_authenticated:
            request.user.profile.ip = request.META.get('REMOTE_ADDR')
            request.user.profile.last_active = timezone.now()
            request.user.profile.are_active = (timezone.now() - request.user.profile.last_active).total_seconds() <= 420
            request.user.profile.save()
        response = self.get_response(request)
        return response
