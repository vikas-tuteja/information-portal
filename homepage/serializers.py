from rest_framework import serializers

from homepage.models import Configure 
from category.serializers import CategorySerializer

class HomePageConfigureSerializer(serializers.ModelSerializer):
    #category = serializers.SerializerMethodField() 
    #content = serializers.SerializerMethodField()
    #library = serializers.SerializerMethodField()

    class Meta:
        model = Configure
        fields = '__all__'
