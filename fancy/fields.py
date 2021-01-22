from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException
from rest_framework.fields import JSONField, IntegerField, Field


class SelfSerializerField(Field):
    def __init__(self, serializer, self_field, relation_field, many=False, **kwargs):
        self.serializer = serializer
        self.self_field = self_field
        self.relation_field = relation_field
        self.many = many

        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, value):
        if self.context['view'].credential:
            queryset = self.serializer.Meta.model.objects.filter(**{
                self.relation_field: value.id,
                self.self_field: self.context['view'].credential.id
            })

            if not self.many:
                queryset = queryset.first()

            serializer = self.serializer(instance=queryset, many=self.many, context=self.context)

            return serializer.data

        if self.many:
            return []
        return None

    def to_internal_value(self, data):
        raise NotImplementedError()


class LoginRequiredSerializerField(Field):
    def __init__(self, serializer, many=False, **kwargs):
        self.serializer = serializer
        self.many = many

        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, value):
        if not self.context['view'].credential:
            return None

        try:
            queryset = self.serializer.Meta.model.objects.get(id=value.seller_id)
        except ObjectDoesNotExist:
            return None

        serializer = self.serializer(instance=queryset, context=self.context)
        return serializer.data

    def to_internal_value(self, data):
        raise NotImplementedError()


class RestrictedIntegerField(IntegerField):
    def to_internal_value(self, data):
        if not isinstance(data, int):
            self.fail('invalid')

        return super(RestrictedIntegerField, self).to_internal_value(data)


class FancyJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        if 'serializer' not in kwargs:
            raise APIException('Serializer is required')

        self.serializer = kwargs['serializer']
        del kwargs['serializer']

        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        _data = self.serializer(data=data)
        _data.is_valid(raise_exception=True)

        return super(FancyJSONField, self).to_internal_value(data)
