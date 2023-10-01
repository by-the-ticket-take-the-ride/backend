from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm

# from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'




class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'first_name', 'last_name',
                    'phone', 'telegram']
    form = CustomUserChangeForm


admin.site.register(User, UserAdmin, list_filter=('is_organizer',))
