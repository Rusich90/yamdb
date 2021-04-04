from rest_framework import viewsets, status
from title.models import Review, Title
from .serializers import ReviewSerializers, TitleSerializers


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializers
