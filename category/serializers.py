from rest_framework import serializers

from category.models import Category, SubCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryIdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategoryIdNameSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'active', 'image', 'category')
