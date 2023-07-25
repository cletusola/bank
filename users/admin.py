from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# custom user admin display 
class CustomeUserAdmin(UserAdmin):

    model = CustomUser

    list_display = ['first_name','last_name','username','email','is_active','is_staff','is_superuser','last_login']
    list_display_links = ['first_name','last_name','username','email']
    list_filter = ['username','email','is_active','is_staff','is_superuser']
    fieldsets = [
        ('Basic Info', {'fields':('first_name', 'last_name', 'email','username','password')}),
        ('Permissions', {'fields':('is_active','is_staff','is_superuser',
                        'groups','user_permissions')}),
        ('Dates', {'fields': ('last_login',)})
    ]
    ordering = ('email',)
    search_fields = ['username','email']

admin.site.register(CustomUser,CustomeUserAdmin)