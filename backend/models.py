from django.db import models


class purchase_category(models.Model):
    category = models.CharField(
        max_length=50, unique=True)

    def __str__(self):
        return f"{self.category}"


class expense(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    category = models.ForeignKey(
        purchase_category, on_delete=models.CASCADE, related_name="expenses")
    description = models.TextField()

    def __str__(self):
        return f"{self.name}, {self.amount}, {self.date}, {self.category}, {self.description}"

    # Create your models here.
