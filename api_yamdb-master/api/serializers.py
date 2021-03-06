from rest_framework import serializers
from title.models import Title, Review, User, Category, Genre, Comments


class ReviewSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "bio",
                  "email", "role")
        extra_field_kwargs = {"url": {"lookup_field": "username"}}


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class CommentsSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comments
        fields = ("id", "text", "author", "pub_date")


class TitleListSerializers(serializers.ModelSerializer):
    rating = serializers.FloatField()
    category = CategorySerializers()
    genre = GenreSerializers(many=True)

    class Meta:
        model = Title
        fields = "__all__"


class TitlePostSerializers(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        required=False,
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ("id", "name", "year", "genre",
                  "category", "description")
        model = Title


class UserProfileSerializers(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "bio",
                  "email", "role")


class EmailSerializers(serializers.Serializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=50)


class TokenSerializers(serializers.Serializer):

    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)