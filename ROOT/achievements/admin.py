from .models import Achievement, APIUser, AchievementUnlocked
from django.contrib import admin

# Register your models here.

admin.site.register(Achievement)
admin.site.register(AchievementUnlocked)
admin.site.register(APIUser)
