import copy
import contextlib

from django.contrib import admin
from django.utils.html import format_html
from information_portal_backend.settings import FRONTEND_URL, BACKEND_URL

from content.models import Status, Image, Content, Library
from utils.utils import getattr_recursive 

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'image_url')

    def image_url(self, obj):
        return '{}{}'.format(BACKEND_URL, obj.image.url)


def approve(modeladmin, request, queryset):
    queryset.update(
        approved_rejected_by=request.user,
        active=True,
        status=Status.objects.get(slug='approved')
    )

def reject(modeladmin, request, queryset):
    queryset.update(
        approved_rejected_by=request.user,
        active=False,
        status=Status.objects.get(slug='rejected')
    )


class ModerationAdmin(admin.ModelAdmin):
    actions = [approve, reject]

    def review_status(self, obj):
        if obj.status.name.lower() == 'approved':
            return format_html('<span style="color: green">Approved</span>')
        elif obj.status.name.lower() == 'rejected':
            return format_html('<span style="color: red">Rejected</span>')
        else:
            return obj.status.name

    def reviewed_by(self, obj):
        name = [getattr_recursive(obj.approved_rejected_by, ['first_name']), 
            getattr_recursive(obj.approved_rejected_by, ['last_name'])]
        if all(name):
            return ' '.join(name)
        else:
            return getattr_recursive(obj, ['approved_rejected_by', 'username'])

    @staticmethod
    def preview(self):
        url_map = {
            'content': 'latest-news',
            'library': 'audio-library'
        }
        return format_html(
            '<a target="_blank" class="button" style="background-color:cadetblue;" \
                href="{}/{}/{}/?preview=1">Preview</a>'.format(
                FRONTEND_URL, url_map[self.__class__.__name__.lower()], self.slug))


class ContentAdmin(ModerationAdmin):
    search_fields = ('name',)
    list_display = ('title', 'created_at', 'views', 'active', 'status', 'reviewed_by', 'preview')
    filter_horizontal = ('sub_category',)
    readonly_fields = ('slug', 'views', 'status', 'active', 'approved_rejected_by')


class LibraryAdmin(ModerationAdmin):
    search_fields = ('name',)
    filter_horizontal = ('sub_category',)
    list_display = ('title', 'size', 'filetype', 'created_at', 'views', 'active', 'status', 'reviewed_by', 'preview')
    readonly_fields = ('slug', 'views', 'status', 'active', 'size', 'filetype', 'approved_rejected_by')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    readonly_fields = ('slug',)

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Image, ImageAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Status, StatusAdmin)
