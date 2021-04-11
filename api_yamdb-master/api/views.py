from rest_framework import viewsets, status, pagination, filters
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
from .permissions import (AdminPermission, AdminPostPermission)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    pagination_class = pagination.PageNumberPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return Review.objects.filter(
            title=self.kwargs['title_id']
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = pagination.PageNumberPagination
    filter_class = TitleFilter
    permission_classes = [IsAuthenticatedOrReadOnly, AdminPostPermission]

    def get_serializer_class(self):
        if self.request.method == ["POST", "PATCH", "DELETE"]:
            return TitlePostSerializers
        return TitleListSerializers



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
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

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]
    permission_classes = [IsAuthenticatedOrReadOnly, AdminPostPermission]


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    pagination_class = pagination.PageNumberPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return Comments.objects.filter(
            review=self.kwargs["review_id"]
        )

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


    # "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNzk0NjYwMiwianRpIjoiODAxY2JmOGY4NzI5NGRlMGIwNmVkNjljNGRmZDRiMjkiLCJ1c2VyX2lkIjoxMDB9.bfEDXM1Nrit6oiI3NOMWDxQgiofyRrYeR_lMjXZqUO0",
    # "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE4NDY1MDAyLCJqdGkiOiI0NWEyM2I0MTg3MjI0MDdkODkyZDg0MDllODI5NGJkOCIsInVzZXJfaWQiOjEwMH0.dWvll0QXvV9GcSehWYmQ7VAZXG2RTZDNroh7QywYTMk"