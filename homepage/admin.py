from django.contrib import admin

from homepage.models import Configure


# Register your models here.
class ConfigureAdmin(admin.ModelAdmin):
    filter_horizontal = ('category', 'content', 'library')

    def has_add_permission(self, request):
        # allow only 1 row to be added
        return not Configure.objects.exists()

admin.site.register(Configure, ConfigureAdmin)
