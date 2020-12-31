from django.contrib import admin
from category.models import Category, SubCategory

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'slug', 'active', 'active_from', 'active_till')
    readonly_fields = ('slug', 'image')

class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'slug', 'get_category', 'active', 'active_from', 'active_till')
    readonly_fields = ('slug', 'image')
    filter_horizontal = ('category',)

    def get_category(self, obj):
        return ", ".join([x.name for x in obj.category.all()])

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
