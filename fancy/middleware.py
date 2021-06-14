import time

from django.http import JsonResponse
from django.utils.cache import add_never_cache_headers

from fancy.settings import DEBUG


class ElapsedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.process_time()
        response = self.get_response(request)
        response['X-Elapsed-Time'] = time.process_time() - start_time

        return response


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_exception(self, request, exception):
        if DEBUG:
            raise exception

        status = 500
        message = 'Unknown error occurred'

        return JsonResponse(
            data={
                'detail': message,
            },
            status=status,
        )


class NeverCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response
