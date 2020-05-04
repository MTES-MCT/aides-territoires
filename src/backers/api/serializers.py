from rest_framework import serializers

from backers.models import Backer


class BackerSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='id_slug')
    text = serializers.CharField(source='name')

    class Meta:
        model = Backer
        fields = ('id', 'text')
