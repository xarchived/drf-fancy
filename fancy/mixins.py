from django.db import models
from rest_framework.serializers import ModelSerializer, ListSerializer


class _BaseSerializer(ModelSerializer):
    class Meta:
        model: models.Model

    @property
    def grouped_fields(self) -> tuple:
        many_to_many = dict()
        one_to_many = dict()
        not_relation = dict()

        for field_name, field_value in self.initial_data.items():
            field = self.fields.fields[field_name]
            if isinstance(field, ListSerializer):
                for record in field_value:
                    obj = field.child.Meta.model.objects.create(**record)
                    if field_name in many_to_many:
                        many_to_many[field_name].append(obj.pk)
                    else:
                        many_to_many[field_name] = [obj.pk]
            elif field_name.endswith('_ids'):
                _field_name = field_name[:field_name.rfind('_ids')]
                if _field_name in many_to_many:
                    many_to_many[_field_name] += field_value
                else:
                    many_to_many[_field_name] = field_value
            elif field_name.endswith('_id'):
                pass
            else:
                not_relation[field_name] = field_value

        return many_to_many, one_to_many, not_relation

    @staticmethod
    def save_many_to_many_fields(instance, data, clear=False):
        for field_name, field_value in data.items():
            attr = getattr(instance, field_name)

            if clear:
                attr.clear()

            for pk in field_value:
                attr.add(pk)

    def save_one_to_many_fields(self):
        raise NotImplemented()


class FancyCreateMixin(_BaseSerializer):
    def create(self, validated_data):
        many_to_many, one_to_many, normal = self.grouped_fields

        instance = self.Meta.model.objects.create(**normal)
        self.save_many_to_many_fields(instance, many_to_many)

        return instance


class FancyUpdateMixin(_BaseSerializer):
    def update(self, instance, validated_data):
        many_to_many, one_to_many, normal = self.grouped_fields

        self.save_many_to_many_fields(instance, many_to_many, clear=True)
        for field_name, field_value in normal.items():
            setattr(instance, field_name, field_value)
        instance.save()

        return instance
