from django.conf import settings
from django.http import JsonResponse


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

        return JsonResponse({
            'detail': message
        }, status=status)
