from django.urls import path, include
from .views import (TitleViewSet, ReviewViewSet, UserViewSet,
                    CategoryViewSet, GenreViewSet, CommentsViewSet)
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
    path('', include(router.urls)),
]

