from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Mood(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    date = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)