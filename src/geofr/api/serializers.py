from rest_framework import serializers

from geofr.models import Perimeter


class PerimeterSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='id_slug')
    scale = serializers.CharField(source='get_scale_display')
    text = serializers.CharField(source='__str__')

    class Meta:
        model = Perimeter
        fields = ('id', 'name', 'scale', 'text')
