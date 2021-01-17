from rest_framework import serializers

from information_portal_backend.settings import BACKEND_URL, BACKEND_URL_PORT
from content.models import Content, Library

class ContentLibraryBase(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    is_fake = serializers.SerializerMethodField()

    def get_author(self, obj):
        return '{} {}'.format(obj.author.first_name, obj.author.last_name)

    def get_summary(self, obj):
        if obj.show_summary:
            return obj.summary
        return ''

    def get_is_fake(self, obj):
        return 'fake-news' in [
            x.slug for x in obj.sub_category.all()]


class ContentSerializer(ContentLibraryBase):
    class Meta:
        model = Content
        fields = '__all__'


class ContentDetailSerializer(ContentLibraryBase):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = '__all__'

    def get_content(self, obj):
        return obj.content.replace('src="/media/', 'src="{}:{}/media/'.format(
            BACKEND_URL, BACKEND_URL_PORT
        ))

class LibrarySerializer(ContentLibraryBase):
    class Meta:
        model = Library
        fields = '__all__'


class LibraryDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return '{} {}'.format(obj.author.first_name, obj.author.last_name)

    class Meta:
        model = Library
        fields = '__all__'
