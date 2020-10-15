from rest_framework import viewsets


class FancyViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        params = {}
        for param in self.request.query_params:
            # To avoid confusion we start our filter parameters with "__"
            if not param.startswith('__'):
                continue
            key = param[2:]

            # Django "filter" dose not support numerical conversion for JSON fields. We convert all params ourself
            try:
                params[key] = float(self.request.query_params[param])
            except ValueError:
                params[key] = self.request.query_params[param]

        return self.serializer_class.Meta.model.objects.filter(**params)
