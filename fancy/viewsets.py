from rest_framework import viewsets


class FancyViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(**self.request.query_params.dict())
