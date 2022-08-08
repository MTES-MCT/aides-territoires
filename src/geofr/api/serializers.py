from rest_framework import serializers

from geofr.models import Perimeter


class PerimeterSerializer(serializers.ModelSerializer):
    """
    Renaming 'name' to 'text' for autocomplete with select2.
    """

    id = serializers.CharField(source="id_slug")
    text = serializers.CharField(source="__str__")
    scale = serializers.CharField(source="get_scale_display")
    zipcodes = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Perimeter
        fields = ("id", "text", "name", "scale", "zipcodes")


class PerimeterScaleSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
