from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOISE = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin")
    )
    role = models.CharField(choices=ROLE_CHOISE, default='user', max_length=10)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)


class Genre_Title(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField("date_published", auto_now_add=True)


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date_published", auto_now_add=True)