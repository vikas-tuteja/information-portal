from django.contrib import admin

from homepage.models import Configure


# Register your models here.
class ConfigureAdmin(admin.ModelAdmin):
    filter_horizontal = ('articles', 'blogs', 'news', 'library')
    def has_add_permission(self, request):
        return False

admin.site.register(Configure, ConfigureAdmin)
