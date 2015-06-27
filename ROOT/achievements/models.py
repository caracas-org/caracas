from django.db import models


class Achievement(models.Model):

    def __str__(self):
        return "{}: {}".format(self.id, self.name)

    name = models.CharField(
        max_length = 256
    )
    description = models.TextField(
        blank=True, null=True,
    )

    XP_gained = models.PositiveIntegerField(
    )

    icon = models.ImageField(
        blank=True, null=True,
    )

    max_progress = models.PositiveIntegerField(
        default=1
    )

    # optional location
    lon = models.FloatField(
        blank=True, null=True,
    )
    lat = models.FloatField(
        blank=True, null=True,
    )
    radius = models.FloatField(
        blank=True, null=True,
        help_text='"Activation radius", ie. when you are inside of this radius around lat/lon, the Achievement will unlock',
    )


class AchievementUnlocked(models.Model):

    def __str__(self):
        return "{}: {}".format(self.character.user.username, self.achievement.name)

    achievement = models.ForeignKey(Achievement)
    character = models.ForeignKey('character.Character')

    progress = models.PositiveIntegerField(
        default=0
    )

    started = models.DateTimeField(
        auto_now_add=True,
        help_text='When was progress on this achievement started?',
    )

    unlocked = models.DateTimeField(
        blank=True, null=True,
        help_text='When was this achievement unlocked (completed).',
    )

    last_progress = models.DateTimeField(
        auto_now=True,
    )


class APIUser(models.Model):
    def __str__(self):
        return self.auth_token
    auth_token = models.CharField(max_length=32)
    achievements = models.ManyToManyField(Achievement)