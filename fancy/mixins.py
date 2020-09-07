from django.db import models
from rest_framework.serializers import ModelSerializer, ListSerializer


class _BaseSerializer(ModelSerializer):
    class Meta:
        model: models.Model


class FancyCreateMixin(_BaseSerializer):
    def create(self, validated_data):
        many_to_many = dict()
        for field_name, field_value in self.initial_data.items():
            field = self.fields.fields[field_name]
            if isinstance(field, ListSerializer):
                for record in field_value:
                    obj = field.child.Meta.model.objects.create(**record)
                    if field_name in many_to_many:
                        many_to_many[field_name].append(obj.pk)
                    else:
                        many_to_many[field_name] = [obj.pk]
                validated_data.pop(field_name)
            if field_name.endswith('_id'):
                validated_data.pop(field_name)
            if field_name.endswith('_ids'):
                _field_name = field_name[:field_name.rfind('_ids')]
                if _field_name in many_to_many:
                    many_to_many[_field_name] += field_value
                else:
                    many_to_many[_field_name] = field_value
                validated_data.pop(_field_name)

        instance = self.Meta.model.objects.create(**validated_data)
        for field_name, field_value in many_to_many.items():
            attr = getattr(instance, field_name)
            for pk in field_value:
                attr.add(pk)

        return instance


class FancyUpdateMixin(_BaseSerializer):
    def update(self, instance, validated_data):
        raise NotImplemented()
