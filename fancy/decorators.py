from rest_framework.exceptions import NotAuthenticated


def credential_required(func):
    def wrapper(*args, **kwargs):
        self = args[0]

        if not self.credential:
            raise NotAuthenticated('No credential found')

        return func(*args, **kwargs)

    return wrapper
