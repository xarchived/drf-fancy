from rest_framework.mixins import CreateModelMixin

from fancy.decorators import credential_required
from getter import get_model


# noinspection PyUnresolvedReferences
class SelfCreateModelMixin(CreateModelMixin):
    @credential_required
    def create(self, request, *args, **kwargs):
        if self.self_func(self.queryset, self.credential['id']):
            raise NotImplemented('with "self_func" you have to override create method')

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
