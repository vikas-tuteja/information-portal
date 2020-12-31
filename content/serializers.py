from rest_framework import serializers

from content.models import Content, Library

class ContentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return '{} {}'.format(obj.author.first_name, obj.author.last_name)

    class Meta:
        model = Content
        fields = '__all__'


class ContentDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return '{} {}'.format(obj.author.first_name, obj.author.last_name)

    class Meta:
        model = Content
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return '{} {}'.format(obj.author.first_name, obj.author.last_name)

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
