from rest_framework import serializers

from programs.models import Program


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ('id', 'slug', 'name')
