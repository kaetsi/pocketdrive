from django.db import models

class Drop(models.Model):
    lookup = models.CharField(max_length=64, unique=True)
    salt = models.CharField(max_length=32)
    drop = models.TextField()