from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class NonClient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    job_title = models.CharField(max_length = 255)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField()

class Outcome(models.Model):
    CATEGORY_CHOICES = [
        ('rent', 'Rent'),
        ('car', 'Car'),
        ('insurance', 'Insurance'),
    ]
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.CharField(max_length = 50, choices = CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField()