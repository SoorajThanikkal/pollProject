from django.contrib import admin
from .import models
admin.site.register(models.PollModel)
admin.site.register(models.PollOption)
admin.site.register(models.UserVote)

# Register your models here.
