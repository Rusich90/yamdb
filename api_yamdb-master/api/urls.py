from django.urls import path, include
from .views import (TitleViewSet, ReviewViewSet, UserViewSet,
                    CategoryViewSet, GenreViewSet, CommentsViewSet,
                    send_code, get_token, user_profile)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentsViewSet,
                basename='comments')
router.register('titles', TitleViewSet)
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('auth/email/', send_code, name='send_code'),
    path('auth/token/', get_token, name='get_token'),
    path('users/me/', user_profile, name='user_profile'),
    path('', include(router.urls)),
]

