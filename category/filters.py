import django_filters
from django_filters import rest_framework as filters

from category.models import Category


class CategoryFilters(filters.FilterSet):
    name = django_filters.CharFilter(method='get_category_name')
    class Meta:
        model = Category
        fields = ['name',]

    def get_category_name(self, queryset, name, value):
        qs = queryset.filter(name__icontains=value.lower())
        return qs

