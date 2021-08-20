from rest_framework.viewsets import ModelViewSet

from fancy.mixins import SelfCreateModelMixin
from fancy.views import FancyAPIView, DynamicFilterAPIView, SelfAPIView


class FancyViewSet(ModelViewSet, FancyAPIView, DynamicFilterAPIView):
    pass


class FancySelfViewSet(FancyViewSet, SelfCreateModelMixin, SelfAPIView):
    pass
