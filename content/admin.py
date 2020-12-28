from django.contrib import admin
from django.utils.html import format_html

from content.models import Status, Image, Content, Library

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_url')

    def image_url(self, obj):
        return obj.image.url


class ModerationAdmin(admin.ModelAdmin):
    def review_status(self, obj):
        if obj.status.name.lower() == 'approved':
            return format_html('<span style="color: green">Approved</span>')
        elif obj.status.name.lower() == 'rejected':
            return format_html('<span style="color: red">Rejected</span>')
        else:
            return obj.status.name

    @staticmethod
    def approve(self):
        return format_html('<a class="button" href="/api/content/{}/{}/approved">Approve</a>'.format(self.__class__.__name__, self.id))

    @staticmethod
    def reject(self):
        return format_html('<a class="button" style="background-color:red;" href="/api/content/{}/{}/rejected">Reject</a>'.format(self.__class__.__name__, self.id))


class ContentAdmin(ModerationAdmin):
    search_fields = ('name',)
    list_display = ('title', 'created_at', 'views', 'active', 'status', 'approve', 'reject')
    filter_horizontal = ('sub_category',)
    readonly_fields = ('slug', 'views', 'status', 'active')


class LibraryAdmin(ModerationAdmin):
    search_fields = ('name',)
    filter_horizontal = ('sub_category',)
    list_display = ('title', 'created_at', 'views', 'active', 'status', 'approve', 'reject')
    readonly_fields = ('slug', 'views', 'status', 'active')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')

admin.site.register(Image, ImageAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Status, StatusAdmin)
