from django.contrib import admin
from .models import User, Profile, Posts, Employee, Permission

#Mix Profile, Posts, Employes into User info

class ProfileInLine(admin.StackedInline):
    model = Profile

class ProfilePosts(admin.TabularInline):
    model = Posts

class ProfileEmployee(admin.TabularInline):
    model = Employee

#Extend User model
class UserAdmin(admin.ModelAdmin):
    model=User
    inlines = [ProfileInLine, ProfilePosts, ProfileEmployee]


#unregister User Model
admin.site.unregister(User)

#registerUsr and Profile
admin.site.register(User, UserAdmin)
