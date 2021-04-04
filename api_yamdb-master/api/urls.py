from django.urls import path, include
from .views import TitlesViewSet, ReviewsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('reviews', ReviewsViewSet)
router.register('titles', TitlesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

