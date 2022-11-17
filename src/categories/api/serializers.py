from rest_framework import serializers

from categories.models import Theme, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ThemeSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)

    class Meta:
        model = Theme
        fields = ("id", "name", "slug", "categories")
