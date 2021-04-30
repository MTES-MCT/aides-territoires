from rest_framework import serializers

from stats.models import AidMatchProjectEvent, AidEligibilityTestEvent


class AidMatchProjectEventSerializer(serializers.ModelSerializer):
    querystring = serializers.CharField(allow_blank=True)

    class Meta:
        model = AidMatchProjectEvent
        fields = '__all__'


class AidEligibilityTestEventSerializer(serializers.ModelSerializer):
    querystring = serializers.CharField(allow_blank=True)

    class Meta:
        model = AidEligibilityTestEvent
        fields = '__all__'
