from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema, InlineSerializerInspector

from fancy.fields import LoginRequiredSerializerField, SelfSerializerField


class FancyInspector(InlineSerializerInspector):
    def field_to_swagger_object(self, field, swagger_object_type, use_references, **kwargs):
        if isinstance(field, (LoginRequiredSerializerField, SelfSerializerField)):
            field = field.serializer(many=field.many, read_only=True)
            use_references = True

        return super(FancyInspector, self).field_to_swagger_object(
            field=field,
            swagger_object_type=swagger_object_type,
            use_references=use_references,
            **kwargs)


class FancyAutoSchema(SwaggerAutoSchema):
    field_inspectors = [FancyInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS
