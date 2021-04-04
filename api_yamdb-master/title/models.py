from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    ROLE_CHOISE = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin")
    )
    role = models.CharField(choices=ROLE_CHOISE, default='user', max_length=10)
    description = models.TextField(default=None)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField(
            validators=[
                MinValueValidator(1000),
                MaxValueValidator(datetime.now().year)],
            help_text="Use the following format: <YYYY>")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="category")


class Genre_Title(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="genres")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField("date_published", auto_now_add=True)


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField("date_published", auto_now_add=True)
