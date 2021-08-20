from ast import literal_eval

from rest_framework.fields import CharField, IntegerField, DateTimeField
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView

from fancy.decorators import queryset_credential_handler
from fancy.settings import TYPE_CASTING, RESERVED_PARAMS


class CredentialAPIView(GenericAPIView):
    # noinspection PyProtectedMember
    @property
    def credential(self):
        if hasattr(self.request._request, 'credential'):
            return self.request._request.credential
        return None


class SelfAPIView(CredentialAPIView):
    self_field: str
    self_model: tuple

    @queryset_credential_handler
    def get_queryset(self):
        return super().get_queryset().filter(**{self.self_field: self.credential['id']})


class DynamicFilterAPIView(GenericAPIView):
    def get_queryset(self):
        type_casting = TYPE_CASTING
        reserved_params = RESERVED_PARAMS

        params = {}
        for param in self.request.query_params:
            if param in reserved_params:
                continue

            value = self.request.query_params[param]
            if param.endswith('__in'):  # When we use "in" we have to convert our value into a list
                value = literal_eval(value)
                if not isinstance(value, tuple):
                    value = (value,)
                params[param] = value
            elif value == 'null':
                params[param] = None
            elif value == 'true':
                params[param] = True
            elif value == 'false':
                params[param] = False
            elif type_casting:  # Django dose not convert JSON numeric value automatically
                try:
                    if '.' in value:
                        params[param] = float(value)
                    else:
                        params[param] = int(value)
                except ValueError:
                    params[param] = value
            else:  # We trust Django and do not check for correct values
                params[param] = value

        return self.queryset.filter(**params).distinct()


class SearchOrderingAPIView(GenericAPIView):
    filter_backends = [OrderingFilter, SearchFilter]

    def __init__(self, **kwargs):
        if hasattr(self.serializer_class, 'Meta') and hasattr(self.serializer_class.Meta, 'fields'):
            temp = []
            # noinspection PyProtectedMember
            for field, field_type in self.serializer_class._declared_fields.items():
                if field not in self.serializer_class.Meta.fields:
                    continue

                if field_type.write_only:
                    continue

                conditions = (
                        isinstance(field_type, CharField)
                        or isinstance(field_type, IntegerField)
                        or isinstance(field_type, DateTimeField)
                )
                if conditions:
                    temp.append(field)

            self.ordering_fields = temp
            self.search_fields = temp

        super().__init__(**kwargs)
