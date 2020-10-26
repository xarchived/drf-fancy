from getter import get_setting
from rest_framework import viewsets


class FancyViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        type_casting = get_setting('FANCY', 'TYPE_CASTING')

        params = {}
        for param in self.request.query_params:
            # To avoid confusion we start our filter parameters with "__"
            if not param.startswith('__'):
                continue
            key = param[2:]

            # Django "filter" dose not support numerical conversion for JSON fields. We convert all params ourself
            value = self.request.query_params[param]
            if type_casting:
                try:
                    if '.' in value:
                        params[key] = float(value)
                    else:
                        params[key] = int(value)
                except ValueError:
                    params[key] = value
            else:
                params[key] = value

        return self.serializer_class.Meta.model.objects.filter(**params)
