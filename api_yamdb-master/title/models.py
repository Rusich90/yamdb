from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    category = models.ForeignKey(Category)

class Genre_Title(models.Model):
    title = models.ForeignKey(Title)
    genre = models.ForeignKey(Genre)


class Review(models.Model):
    title = models.ForeignKey(Title)
    text = models.TextField()
    author = models.ForeignKey(User)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField("date_published", auto_now_add=True)


class Comments(models.Model):
    review = models.ForeignKey(Review)
    text = models.TextField()
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField("date_published", auto_now_add=True)