from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.User._meta.fields]
    search_fields = [field.name for field in models.User._meta.fields]

    class Meta:
        model = models.User


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Post._meta.fields]
    search_fields = [field.name for field in models.Post._meta.fields]

    class Meta:
        model = models.Post


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Post, PostAdmin)
