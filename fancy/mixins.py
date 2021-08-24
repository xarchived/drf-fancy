from inspect import getsourcelines

from rest_framework.mixins import CreateModelMixin

from fancy.decorators import credential_required
from getter import get_model


# noinspection PyUnresolvedReferences
class SelfCreateModelMixin(CreateModelMixin):
    @credential_required
    def create(self, request, *args, **kwargs):
        # There should be a better way to handle this!
        # When "get_func" is used there should be custom method to store out model
        source_lines = getsourcelines(self.self_func)
        if 'pass' not in source_lines[0][1]:
            raise NotImplemented('with "self_func" you have to override create method')

        # Beware "self_field" when there is "__" in field name we should handle it with "self_model"
        if hasattr(self, 'self_field') and '__' not in self.self_field:
            request.data[self.self_field] = self.credential['id']

        # Run DRF create method
        response = super().create(request, *args, **kwargs)

        # Handle self model
        if hasattr(self, 'self_model'):
            model_name, left, right = self.self_model
            model_class = get_model(model_name)
            args = {left: response.data['id'], right: self.credential['id']}
            instant = model_class(**args)
            instant.save()

        return response
