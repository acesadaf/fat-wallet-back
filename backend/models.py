from django.db import models
from django.contrib.auth.models import User

GENERAL_USER = 10


class purchase_category(models.Model):
    category = models.CharField(
        max_length=50, unique=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=GENERAL_USER)

    def __str__(self):
        return f"{self.category}, {self.user}"


class expense(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    category = models.ForeignKey(
        purchase_category, on_delete=models.CASCADE, related_name="expenses")
    description = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expenses")

    def __str__(self):
        return f"{self.name}, {self.amount}, {self.date}, {self.category}, {self.description}, {self.user}"

    # Create your models here.
