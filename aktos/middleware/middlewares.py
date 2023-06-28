from django.http import HttpResponseForbidden
from django.core.cache import cache
import time


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client's IP address or unique identifier
        client_id = request.META.get("REMOTE_ADDR") or request.user.username

        # Generate a cache key based on the client ID and current minute
        cache_key = f"rate_limit:{client_id}:{int(time.time() // 60)}"

        # Increment the request count by 1 or initialize it to 1
        request_count = cache.get(cache_key, 0) + 1

        # Set the new request count in the cache
        cache.set(cache_key, request_count, 60)

        # Check if the request count exceeds the limit
        if request_count > 20:
            return HttpResponseForbidden("Rate limit exceeded")

        return self.get_response(request)
