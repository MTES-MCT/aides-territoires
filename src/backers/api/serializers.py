from rest_framework import serializers

from backers.models import Backer


class BackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Backer
        fields = ('id', 'name')
