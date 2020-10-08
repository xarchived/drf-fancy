from rest_framework.fields import JSONField, IntegerField


class RestrictedIntegerField(IntegerField):
    def to_internal_value(self, data):
        if not isinstance(data, int):
            self.fail('invalid')

        return super(RestrictedIntegerField, self).to_internal_value(data)


class FancyJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        if 'serializer' not in kwargs:
            raise ValueError('Serializer is required')

        self.serializer = kwargs['serializer']
        del kwargs['serializer']

        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        _data = self.serializer(data=data)
        _data.is_valid(raise_exception=True)

        return super(FancyJSONField, self).to_internal_value(data)
