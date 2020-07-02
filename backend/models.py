from django.db import models


class Dummy(models.Model):
    content = models.TextField()

    def __str__(self):
        return f" i am {self.cotent}"
# Create your models here.
