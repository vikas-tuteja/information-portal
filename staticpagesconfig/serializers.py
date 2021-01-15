from rest_framework import serializers

from staticpagesconfig.models import FAQs

class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = '__all__'
