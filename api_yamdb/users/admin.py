from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ('confirmation_code',)


admin.site.register(User, UserAdmin)
