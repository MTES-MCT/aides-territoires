from rest_framework import serializers

from geofr.models import Perimeter


class PerimeterSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='id_slug')
    scale = serializers.CharField(source='get_scale_display')
    text = serializers.CharField(source='__str__')

    zipcodes = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Perimeter
        fields = ('id', 'name', 'scale', 'zipcodes', 'text')


class PerimeterScaleSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
