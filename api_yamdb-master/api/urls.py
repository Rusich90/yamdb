from django.urls import path, include
from .views import (TitleViewSet, ReviewViewSet, UserViewSet,
                    CategoryViewSet, GenreViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('reviews', ReviewViewSet)
router.register('titles', TitleViewSet)
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

