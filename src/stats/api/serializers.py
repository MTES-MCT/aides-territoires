
from rest_framework import serializers

from stats.models import AidMatchProjectEvent


class AidMatchProjectEventSerializer(serializers.ModelSerializer):
    querystring = serializers.CharField(allow_blank=True)

    class Meta:
        model = AidMatchProjectEvent
        fields = '__all__'