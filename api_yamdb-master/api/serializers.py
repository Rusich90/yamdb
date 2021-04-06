from rest_framework import serializers
from title.models import Title, Review, User, Category, Genre, Comments
from django.db.models import Avg


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


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


class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ("id", "text", "author", "pub_date")


class TitleSerializers(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategorySerializers()
    genre = GenreSerializers(many=True)

    class Meta:
        model = Title
        fields = ("id", "name", "year",
                  "rating", "description", "genre", "category")

    def get_rating(self, obj):
        rt = obj.reviews.all().aggregate(Avg('score'))
        if rt == None:
            return 0
        rating = int(rt["score__avg"])
        return rating

    # def get_category(self, obj):
    #     category = {"name": obj.category.name,
    #                 "slug": obj.category.slug}
    #     return category

