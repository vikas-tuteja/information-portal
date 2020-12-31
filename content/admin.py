import copy
import contextlib

from django.contrib import admin
from django.utils.html import format_html
from information_portal_backend.settings import FRONTEND_URL, BACKEND_URL

from content.models import Status, Image, Content, Library

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'image_url')

    def image_url(self, obj):
        return '{}{}'.format(BACKEND_URL, obj.image.url)


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
        return format_html(
            '<a class="button" style="background-color: green;" \
            href="/api/content/{}/{}/approved">Approve</a>'.format(self.__class__.__name__, self.id))

    @staticmethod
    def reject(self):
        return format_html(
            '<a class="button" style="background-color:red;" \
            href="/api/content/{}/{}/rejected">Reject</a>'.format(self.__class__.__name__, self.id))

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

    def get_list_display(self, request):
        x = copy.deepcopy(list(self.list_display))
        groups = [x.name for x in request.user.groups.all()]
        with contextlib.suppress(ValueError):
            if 'admin' not in groups:
                x.remove('approve')
                x.remove('reject')
        return x


class ContentAdmin(ModerationAdmin):
    search_fields = ('name',)
    list_display = ('title', 'created_at', 'views', 'active', 'status', 'approve', 'reject', 'preview')
    filter_horizontal = ('sub_category',)
    readonly_fields = ('slug', 'views', 'status', 'active')


class LibraryAdmin(ModerationAdmin):
    search_fields = ('name',)
    filter_horizontal = ('sub_category',)
    list_display = ('title', 'size', 'filetype', 'created_at', 'views', 'active', 'status', 'approve', 'reject', 'preview')
    readonly_fields = ('slug', 'views', 'status', 'active', 'size', 'filetype')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Image, ImageAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Status, StatusAdmin)
