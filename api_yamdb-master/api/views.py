from rest_framework import viewsets, status, pagination, filters
from title.models import Review, Title, User, Category, Genre, Comments
from .serializers import (ReviewSerializers, TitleSerializers,
                          UserSerializers, CategorySerializers,
                          GenreSerializers, CommentsSerializers)
from django_filters.rest_framework import DjangoFilterBackend


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return Review.objects.filter(
            title=self.kwargs['title_id']
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializers
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["genre",]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = pagination.PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    pagination_class = pagination.PageNumberPagination

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    pagination_class = pagination.PageNumberPagination


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return Comments.objects.filter(
            review=self.kwargs["review_id"]
        )
