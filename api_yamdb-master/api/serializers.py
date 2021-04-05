from rest_framework import serializers
from title.models import Title, Review, User, Category, Genre, Comments


class TitleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ("name", "year", "category")


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("title", "text", "author", "score")


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "description",
                  "email", "role")


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
