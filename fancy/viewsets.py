from rest_framework.viewsets import ModelViewSet

from fancy.mixins import SelfCreateModelMixin
from fancy.views import SearchOrderingAPIView, DynamicFilterAPIView, SelfAPIView


class FancyViewSet(ModelViewSet, SearchOrderingAPIView, DynamicFilterAPIView):
    pass


class FancySelfViewSet(FancyViewSet, SelfCreateModelMixin, SelfAPIView):
    pass
