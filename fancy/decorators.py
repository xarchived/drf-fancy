from rest_framework.exceptions import NotAuthenticated


def credential_required(func):
    def wrapper(*args, **kwargs):
        self = args[0]

        if not self.credential:
            raise NotAuthenticated('No credential found')

        return func(*args, **kwargs)

    return wrapper


def queryset_credential_handler(func):
    def wrapper(*args, **kwargs):
        self = args[0]

        if not self.credential:
            return self.serializer_class.Meta.model.objects.none()

        return func(*args, **kwargs)

    return wrapper
