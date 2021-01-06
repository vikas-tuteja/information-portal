from django.apps import apps
from django.http import HttpResponseRedirect
from rest_framework import generics

from content.models import Content, Library, Status
from content.serializers import ContentSerializer, ContentDetailSerializer, LibrarySerializer, LibraryDetailSerializer
from content.filters import ContentFilters, LibraryFilters

# Create your views here.
class ContentListing( generics.ListAPIView ):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = []
    serializer_class = ContentSerializer
    filterset_class = ContentFilters
    queryset = Content.objects.filter(active=True).order_by('id')

    def get(self, request, *args, **kwargs):
        data = super(ContentListing, self).get(request, *args, **kwargs)
        unique_slug_set = set()
        unique_data = list()
        for each in data.data['results']:
            if each['slug'] not in unique_slug_set:
                unique_data.append(each)
            unique_slug_set.add(each['slug'])

        data.data['results'] = unique_data
        return data 


class ContentDetail( generics.RetrieveAPIView ):
    permission_classes = []
    serializer_class = ContentDetailSerializer

    def get_queryset(self):
        return Content.objects.all()

    def get_object(self):
        qs = self.filter_queryset(self.get_queryset())
        return qs.get(slug=self.kwargs['content_slug'])


class LibraryListing( generics.ListAPIView ):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = []
    serializer_class = LibrarySerializer
    filterset_class = LibraryFilters
    queryset = Library.objects.filter(active=True).order_by('id')


class LibraryDetail( generics.RetrieveAPIView ):
    permission_classes = []
    serializer_class = LibraryDetailSerializer

    def get_queryset(self):
        return Library.objects.all()

    def get_object(self):
        qs = self.filter_queryset(self.get_queryset())
        return qs.get(pk=self.kwargs['pk'])
