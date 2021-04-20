import time

from django.conf import settings
from django.http import JsonResponse


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
        if settings.DEBUG:
            raise exception

        status = 500
        message = 'Unknown error occurred'

        return JsonResponse(
            data={
                'detail': message,
            },
            status=status,
        )
