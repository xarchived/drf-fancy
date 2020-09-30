from collections import defaultdict

from django.db import models
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer, ListSerializer


class FancySerializer(ModelSerializer):
    class Meta:
        model: models.Model

    def _prepare_relational_fields(self) -> None:
        many_to_many = defaultdict(list)

        for field_name, field_value in self.initial_data.items():
            field = self.fields.fields[field_name]
            if isinstance(field, ListSerializer):
                for record in field_value:
                    obj = field.child.Meta.model.objects.create(**record)
                    many_to_many[field_name].append(obj.pk)
            elif field_name.endswith('_ids'):
                _field_name = field_name[:field_name.rfind('_ids')]
                many_to_many[_field_name] += field_value
            elif isinstance(field, ModelSerializer):
                if hasattr(field, 'Meta'):
                    obj = field.Meta.model.objects.create(**field_value)
                    self.validated_data[field_name + '_id'] = obj.pk
                    self.validated_data.pop(field_name)
                else:
                    raise APIException('Meta not found')

        self.many_to_many_data = many_to_many
        for field_name in many_to_many:
            self.validated_data.pop(field_name)

    def _save_none_relational_fields(self) -> None:
        instance = self.Meta.model.objects.create(**self.validated_data)
        self.instance = instance

    def _update_none_relational_fields(self) -> None:
        for field_name, field_value in self.validated_data.items():
            setattr(self.instance, field_name, field_value)
        self.instance.save()

    def _save_or_update_many_to_many_fields(self, update=True) -> None:
        for field_name, field_value in self.many_to_many_data.items():
            attr = getattr(self.instance, field_name)

            if update:
                attr.clear()

            for pk in field_value:
                attr.add(pk)

    def _save_many_to_many_fields(self) -> None:
        self._save_or_update_many_to_many_fields()

    def _update_many_to_many_fields(self) -> None:
        self._save_or_update_many_to_many_fields(update=True)

    def create(self, validated_data):
        self._prepare_relational_fields()
        self._save_none_relational_fields()
        self._save_many_to_many_fields()

        return self.instance

    def update(self, instance, validated_data):
        self._prepare_relational_fields()
        self._update_many_to_many_fields()
        self._update_none_relational_fields()

        return self.instance
