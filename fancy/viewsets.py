from rest_framework.viewsets import ModelViewSet

from fancy.decorators import credential_required, queryset_credential_handler
from fancy.views import FancyAPIView, CredentialAPIView, DynamicFilterAPIView
from getter import get_model


class FancyViewSet(ModelViewSet, FancyAPIView, CredentialAPIView, DynamicFilterAPIView):
    pass


class FancySelfViewSet(FancyViewSet):
    self_field: str
    self_model: tuple

    @queryset_credential_handler
    def get_queryset(self):
        return super().get_queryset().filter(**{self.self_field: self.credential['id']})

    @credential_required
    def create(self, request, *args, **kwargs):
        if hasattr(self, 'self_field') and '__' not in self.self_field:
            request.data[self.self_field] = self.credential['id']

        response = super().create(request, *args, **kwargs)

        if hasattr(self, 'self_model'):
            model_name, left, right = self.self_model
            model_class = get_model(model_name)
            args = {left: response.data['id'], right: self.credential['id']}
            instant = model_class(**args)
            instant.save()

        return response
