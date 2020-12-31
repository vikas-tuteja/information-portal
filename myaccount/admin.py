from django.contrib import admin

from myaccount.models import UserDetail

# Register your models here.
class UserDetailAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
admin.site.register(UserDetail, UserDetailAdmin)
