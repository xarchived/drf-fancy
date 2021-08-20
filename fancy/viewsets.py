from rest_framework.viewsets import ModelViewSet

from fancy.mixins import SelfCreateModelMixin
from fancy.views import FancyAPIView, CredentialAPIView, DynamicFilterAPIView, SelfAPIView


class FancyViewSet(ModelViewSet, FancyAPIView, CredentialAPIView, DynamicFilterAPIView):
    pass


class FancySelfViewSet(FancyViewSet, SelfCreateModelMixin, SelfAPIView):
    pass
