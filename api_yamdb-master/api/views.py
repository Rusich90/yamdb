from rest_framework import viewsets, status, pagination, filters
from rest_framework.exceptions import ParseError
from title.models import Review, Title, User, Category, Genre, Comments
from .serializers import (ReviewSerializers, TitleListSerializers,
                          UserSerializers, CategorySerializers,
                          GenreSerializers, CommentsSerializers,
                          UserProfileSerializers, TitlePostSerializers)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (DjangoModelPermissionsOrAnonReadOnly,
                                        DjangoModelPermissions,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .permissions import (AdminPermission, AdminPostPermission,
                          OwnResourcePermission)
from django.db.models import Avg
from django.db import IntegrityError


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, OwnResourcePermission]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        try:
            serializer.save(author=self.request.user, title=title)
        except IntegrityError:
            raise ParseError(detail="Вы уже оставили обзор на этот пост")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score')).order_by('-id')
    pagination_class = pagination.PageNumberPagination
    filterset_class = TitleFilter
    permission_classes = [IsAuthenticatedOrReadOnly, AdminPostPermission]

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH", "DELETE"):
            return TitlePostSerializers
        return TitleListSerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, AdminPermission]
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    permission_classes = [IsAuthenticatedOrReadOnly, AdminPostPermission]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    permission_classes = [IsAuthenticatedOrReadOnly, AdminPostPermission]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, OwnResourcePermission]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        return Comments.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        serializer.save(author=self.request.user, review=review)


@api_view(['GET', 'PATCH'])
def user_profile(request):
    if request.method == "GET":
        user = User.objects.get(username=request.user.username)
        serializer = UserProfileSerializers(user)
        return Response(serializer.data)
    elif request.method == "PATCH":
        user = User.objects.get(username=request.user.username)
        serializer = UserProfileSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def send_code(request):
    serializer = UserSerializers(data=request.data)
    if serializer.is_valid():
        email = request.data['email']
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


@api_view(['POST'])
def get_token(request):
    email = request.data['email']
    user = get_object_or_404(User, email=email)
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = get_tokens_for_user(user)
        return Response(token)
    return Response("Confirmation code does not match",
                    status=status.HTTP_400_BAD_REQUEST)


    # "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxODU5MDEzNSwianRpIjoiNzg0OGY5OTdjZDg0NDcxMDliZjkwMjY1YjM5ZmQzMGUiLCJ1c2VyX2lkIjoxMDB9.DA0gVADA6OrVoq-nzEtJtKNI1QD5hCqsAIvWvdI5k5w",
    # "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE5MTA4NTM1LCJqdGkiOiI2NzgxMmEwYWVmNGU0MTQzYTYxZWZiNjU0ZmNhODExOSIsInVzZXJfaWQiOjEwMH0.Qx3nWblA7iIQHIG-9ndSWPqflFeZHsaSU0sI-BWm7L0"