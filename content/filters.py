import django_filters
from django_filters import rest_framework as filters

from content.models import Content, Library


class ContentFilters(filters.FilterSet):
    category = django_filters.CharFilter(method='by_category_name')

    class Meta:
        model = Content
        fields = ['category',]

    def by_category_name(self, queryset, name, value):
        return queryset.filter(sub_category__category__slug=value)


class LibraryFilters(filters.FilterSet):
    category = django_filters.CharFilter(method='by_category_name')

    class Meta:
        model = Library
        fields = ['category',]

    def by_category_name(self, queryset, name, value):
        return queryset.filter(sub_category__category__slug=value)
