from django.db import models
from rest_framework.serializers import ModelSerializer, ListSerializer


class _BaseSerializer(ModelSerializer):
    class Meta:
        model: models.Model

    def _extract_relations(self, validated_data) -> tuple:
        many_to_many = dict()
        one_to_many = dict()

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

        for field_name in many_to_many:
            validated_data.pop(field_name)

        return many_to_many, one_to_many

    def _save_none_relational_fields(self, validated_data):
        instance = self.Meta.model.objects.create(**validated_data)

        self.instance = instance
        return instance

    def _update_none_relational_fields(self, instance, validated_data):
        for field_name, field_value in validated_data.items():
            setattr(instance, field_name, field_value)
        instance.save()

        self.instance = instance
        return instance

    @staticmethod
    def _save_or_update_many_to_many_fields(instance, many_to_many_data, update=True) -> None:
        for field_name, field_value in many_to_many_data.items():
            attr = getattr(instance, field_name)

            if update:
                attr.clear()

            for pk in field_value:
                attr.add(pk)

    def _save_many_to_many_fields(self, instance, many_to_many_data) -> None:
        self._save_or_update_many_to_many_fields(instance, many_to_many_data)

    def _update_many_to_many_fields(self, instance, many_to_many_data) -> None:
        self._save_or_update_many_to_many_fields(instance, many_to_many_data, update=True)

    def _save_one_to_many_fields(self):
        raise NotImplemented()


class FancyCreateMixin(_BaseSerializer):
    def create(self, validated_data):
        many_to_many, one_to_many = self._extract_relations(validated_data)
        instance = self._save_none_relational_fields(validated_data)
        self._save_many_to_many_fields(instance, many_to_many)

        return self.instance


class FancyUpdateMixin(_BaseSerializer):
    def update(self, instance, validated_data):
        many_to_many, one_to_many = self._extract_relations(validated_data)
        self._update_many_to_many_fields(instance, many_to_many)
        self._update_none_relational_fields(instance, validated_data)

        return self.instance
