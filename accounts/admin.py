from django.contrib import admin
from .models import User, Profile

#Mix Profile into User info

class ProfileInLine(admin.StackedInline):
    model = Profile

#Extend User model
class UserAdmin(admin.ModelAdmin):
    model=User
    fields = ['username', 'first_name', 'last_name']
    inlines = [ProfileInLine]

#unregister User Model
admin.site.unregister(User)

#registerUsr and Profile
admin.site.register(User, UserAdmin)
