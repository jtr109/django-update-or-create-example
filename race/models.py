from django.db import models


class Race(models.Model):
    user_id = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    age = models.PositiveIntegerField()


class Solution(models.Model):
    user_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32)
    age = models.PositiveIntegerField()


class Together(models.Model):
    user_id = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    age = models.PositiveIntegerField()

    class Meta:
        unique_together = [
            ['user_id', 'name'],
        ]
