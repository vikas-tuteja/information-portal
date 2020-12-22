from django.contrib import admin
from category.models import Category, SubCategory

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'active', 'active_from', 'active_till')
    readonly_fields = ('slug',)

class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'get_category', 'active', 'active_from', 'active_till')
    readonly_fields = ('slug',)
    filter_horizontal = ('category',)

    def get_category(self, obj):
        return ", ".join([x.name for x in obj.category.all()])

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
