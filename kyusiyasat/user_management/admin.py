from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


# Inline Profile model inside UserAdmin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


# Extend UserAdmin to include Profile
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

# Unregister the original User model and register the new one with Profile
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register Profile separately (optional, but useful for debugging)
admin.site.register(Profile)
