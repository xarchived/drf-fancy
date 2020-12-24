from collections import defaultdict
from typing import Any

from django.db import models
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer, ListSerializer


class FancySerializer(ModelSerializer):
    class Meta:
        model: models.Model

    def _prepare_relational_fields(self) -> None:
        # We only should concern about many to many fields, as Django handles one to many fields by itself
        many_to_many = defaultdict(list)

        for field_name, field_value in self.initial_data.items():
            field = self.fields.fields[field_name]

            # Insertion on read only field will cause security issues
            if field.read_only:
                raise APIException(f'Read only field ({field_name})')

            # Detect relation fields and append them to the list
            if isinstance(field, ListSerializer):  # It's a many to many field with new records
                for record in field_value:
                    obj = field.child.Meta.model.objects.create(**record)
                    many_to_many[field_name].append(obj.pk)
            elif field_name.endswith('_ids'):  # It's a many to many field with preexisted records
                _field_name = field_name[:field_name.rfind('_ids')]
                many_to_many[_field_name] += field_value
            elif isinstance(field, ModelSerializer):
                if hasattr(field, 'Meta'):  # It's a one to many record with new record
                    obj = field.Meta.model.objects.create(**field_value)
                    self.validated_data[field_name + '_id'] = obj.pk
                    self.validated_data.pop(field_name)
                else:
                    raise APIException('Meta not found')

        # Assign our list to an attribute for future reference
        self.many_to_many_data = many_to_many

        # Remove all the relation fields from "validated_data" and make it safe to use
        for field_name in many_to_many:
            self.validated_data.pop(field_name)

    def _save_none_relational_fields(self) -> None:
        # Simply call Django "create" function with "validated_data" as previously we extracted all relations fields
        instance = self.Meta.model.objects.create(**self.validated_data)

        # It's really important to fill "self.instance" with new value, hence future calls refer to the right values
        self.instance = instance

    def _update_none_relational_fields(self) -> None:
        # If we set new values to our attributes and then call "save" method, it will save changes into database
        for field_name, field_value in self.validated_data.items():
            setattr(self.instance, field_name, field_value)
        self.instance.save()

    def _save_or_update_many_to_many_fields(self, update: bool = True) -> None:
        # We have to call "_prepare_relational_fields" before calling this method, otherwise an "AttributeError" error
        # will raise because "many_to_many_data" define by "_prepare_relational_fields"
        for field_name, field_value in self.many_to_many_data.items():
            attr = getattr(self.instance, field_name)

            # For update requests, we are going to remove all previous relations and replace them with the new ones
            if update:
                attr.clear()

            for pk in field_value:
                obj = attr.model.objects.get(id=pk)
                attr.add(obj)

    def _save_many_to_many_fields(self) -> None:
        # A proxy method
        self._save_or_update_many_to_many_fields()

    def _update_many_to_many_fields(self) -> None:
        # A proxy method
        self._save_or_update_many_to_many_fields(update=True)

    def create(self, validated_data: dict) -> Any:
        self._prepare_relational_fields()
        self._save_none_relational_fields()
        self._save_many_to_many_fields()

        return self.instance

    def update(self, instance: object, validated_data: dict) -> Any:
        self._prepare_relational_fields()
        self._update_many_to_many_fields()
        self._update_none_relational_fields()

        return self.instance
