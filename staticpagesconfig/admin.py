from django.contrib import admin

from staticpagesconfig.models import FAQs

# Register your models here.
class FAQsAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'position', 'active')

admin.site.register(FAQs, FAQsAdmin)
