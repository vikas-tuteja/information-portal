from rest_framework import serializers

from content.models import Content, Library

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class ContentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'


class LibraryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'
