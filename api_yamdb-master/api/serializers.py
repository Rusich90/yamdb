from rest_framework import serializers
from title.models import Title, Review


class TitleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ("name", "year", "category")


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("title", "text", "author", "score")