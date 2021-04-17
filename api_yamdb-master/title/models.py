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
    bio = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['-id']


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['-id']


class Title(models.Model):
    name = models.CharField(max_length=200, blank=False)
    year = models.PositiveIntegerField(
            validators=[
                MinValueValidator(1000),
                MaxValueValidator(datetime.now().year)],
            help_text="Use the following format: <YYYY>")
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name="category",
                                 blank=True,
                                 null=True)
    genre = models.ManyToManyField(Genre, related_name="genre")


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField("date_published", auto_now_add=True)

    class Meta:
        unique_together = ['title', 'author']
        ordering = ['-id']


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField("date_published", auto_now_add=True)

    class Meta:
        ordering = ['-id']
