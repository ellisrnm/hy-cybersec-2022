from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Mood(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    date = models.DateTimeField()

