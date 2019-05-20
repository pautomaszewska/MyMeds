from django.db import models
from django.contrib.auth.models import User


class Medicine(models.Model):
    name = models.CharField(max_length=64)
    active_ingredient = models.CharField(max_length=128)
    amount = models.IntegerField(null=True)
    dose = models.CharField(max_length=64, null=True)
    expiration_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
