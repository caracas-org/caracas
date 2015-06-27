from django.contrib.auth.models import User
from django.db import models

class Character(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(
        'auth.user',
    )

    image = models.ImageField(
        blank=True, null=True,
    )

    XP = models.PositiveIntegerField(
        default=0,
    )
    points = models.PositiveIntegerField(
        default=0,
    )
    level = models.PositiveIntegerField(
        default=0,
    )
    # optional location
    lon = models.FloatField(
        blank=True, null=True,
    )
    lat = models.FloatField(
        blank=True, null=True,
    )
