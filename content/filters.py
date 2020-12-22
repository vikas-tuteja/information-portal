import django_filters
from django_filters import rest_framework as filters

from content.models import Content, Library


class ContentFilters(filters.FilterSet):
    name = django_filters.CharFilter(method='by_category_name')

    class Meta:
        model = Content
        fields = ['name',]

    def by_category_name(self, queryset, name, value):
        qs = queryset.filter(name__icontains=value.lower())
        return qs


class LibraryFilters(filters.FilterSet):
    name = django_filters.CharFilter(method='by_category_name')

    class Meta:
        model = Library
        fields = ['name',]

    def by_category_name(self, queryset, name, value):
        qs = queryset.filter(name__icontains=value.lower())
        return qs
