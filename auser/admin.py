from django.contrib import admin
from django.contrib.auth import get_user_model, admin as uadmin

User = get_user_model()


@admin.register(User)
class UserAdmin(uadmin.UserAdmin):
    pass
