from rest_framework import serializers

from geofr.models import Perimeter


class PerimeterSerializer(serializers.ModelSerializer):

    scale = serializers.CharField(source='get_scale_display')
    _str = serializers.CharField(source='__str__')

    class Meta:
        model = Perimeter
        fields = ('name', 'scale', '_str')
