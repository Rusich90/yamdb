from rest_framework import viewsets, status, pagination, filters
from title.models import Review, Title, User, Category, Genre, Comments
from .serializers import (ReviewSerializers, TitleSerializers,
                          UserSerializers, CategorySerializers,
                          GenreSerializers, CommentsSerializers)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

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
    filter_class = TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return Comments.objects.filter(
            review=self.kwargs["review_id"]
        )


@api_view(['POST'])
def send_code(request):
    serializer = UserSerializers(data=request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        user = get_object_or_404(User, email=email)
        confirmation_code = default_token_generator.make_token(user)
        serializer.save
        send_mail(
            'Confirmation code',
            f'Your confirmation code: {confirmation_code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response("Confirmation code was sent to your email")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'GET':
#         comments = Comment.objects.filter(post=pk)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CommentSerializer(data=request.data)
#         post = Post.objects.get(id=pk)
#         if serializer.is_valid():
#             serializer.save(author=request.user, post=post)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# send_mail(
#     'Тема письма',
#     'Текст письма.',
#     'from@example.com',  # Это поле "От кого"
#     ['to@example.com'],  # Это поле "Кому" (можно указать список адресов)
#     fail_silently=False, # Сообщать об ошибках («молчать ли об ошибках?»)
# )