from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Channel)
admin.site.register(models.WorkSpace)
admin.site.register(models.UserWorkSpace)
admin.site.register(models.UserChannel)