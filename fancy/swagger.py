from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import SwaggerAutoSchema, InlineSerializerInspector, FieldInspector, NotHandled

from fancy.fields import LoginRequiredSerializerField, SelfSerializerField


class FancyInspector(FieldInspector):
    def field_to_swagger_object(self, field, swagger_object_type, use_references, **kwargs):
        if isinstance(field, (LoginRequiredSerializerField, SelfSerializerField)):
            field = field.serializer(many=field.many, read_only=True)
            use_references = True

            inspector = InlineSerializerInspector(
                view=self.view,
                path=self.path,
                method=self.method,
                components=self.components,
                request=self.request,
                field_inspectors=self.field_inspectors,
            )
            return inspector.field_to_swagger_object(
                field=field,
                swagger_object_type=swagger_object_type,
                use_references=use_references,
                **kwargs,
            )

        return NotHandled


class FancyAutoSchema(SwaggerAutoSchema):
    field_inspectors = [FancyInspector, *swagger_settings.DEFAULT_FIELD_INSPECTORS]
