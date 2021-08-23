from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from fancy.mixins import SelfCreateModelMixin
from fancy.views import SelfAPIView


class GenericSelfViewSet(GenericViewSet, SelfAPIView):
    pass


class ReadOnlySelfModelViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               GenericSelfViewSet):
    pass


class SelfModelViewSet(SelfCreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericSelfViewSet):
    pass
