from django.db import models

class Drop(models.Model):
    lookup = models.CharField(max_length=64, unique=True)
    salt = models.CharField(max_length=32)
    drop = models.TextField()

class Stats(models.Model):
    created = models.IntegerField(default=0)
    retrived = models.IntegerField(default=0)
    destroyed = models.IntegerField(default=0)