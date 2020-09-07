from rest_framework.serializers import ModelSerializer

from fancy.mixins import FancyCreateMixin, FancyUpdateMixin


class FancySerializer(FancyCreateMixin, FancyUpdateMixin, ModelSerializer):
    pass
