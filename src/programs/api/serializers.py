from rest_framework import serializers

from programs.models import Program


class ProgramSerializer(serializers.ModelSerializer):

    perimeter = serializers.StringRelatedField()

    class Meta:
        model = Program
        fields = ('id', 'name', 'slug', 'perimeter')
