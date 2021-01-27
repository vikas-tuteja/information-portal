import json
from django.apps import apps
from django.http import HttpResponse
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
    """
    API endpoint that gives a Content detail
    """
    permission_classes = []
    serializer_class = ContentDetailSerializer

    def get_queryset(self):
        return Content.objects.all()

    def get_object(self):
        qs = self.filter_queryset(self.get_queryset())
        is_preview = bool(self.request.query_params.get('preview'))
        filters = {
            'slug': self.kwargs['content_slug'],
        }
        if not is_preview:
            filters.update({
                'active': True
            })
        return qs.get(**filters)


class LibraryListing( generics.ListAPIView ):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = []
    serializer_class = LibrarySerializer
    filterset_class = LibraryFilters
    queryset = Library.objects.filter(active=True).order_by('id')


class LibraryDetail( generics.RetrieveAPIView ):
    """
    API endpoint that gives an Audio Library detail
    """
    permission_classes = []
    serializer_class = LibraryDetailSerializer

    def get_queryset(self):
        return Library.objects.all()

    def get_object(self):
        qs = self.filter_queryset(self.get_queryset())
        return qs.get(slug=self.kwargs['library_slug'])


class ContentSearch( generics.GenericAPIView ):
    """
    API endpoint that searches for content/Audio Library
    """
    permission_classes = []
    SEARCH_RESULT_LEN = 10
    url_subcategory_map = {
        'content': {
            'fake-news': '/news/{}', 
            'real-news': '/news/{}',
            'blogs': '/blogs/{}',
            'articles': '/articles/{}',
            None: '/news/{}'
        },
        'library' : '/audio-books/{}', 
    }
    serializer_class = ContentSerializer

    def get(self, request, *args, **kwargs):
        search_string = self.request.query_params['search_string']
        results = []
        librarys = []
        contents = Content.objects.filter(
            active=True,
            title__icontains=search_string).values(
            'title', 'sub_category__name', 'sub_category__slug', 'slug'
            )[:self.SEARCH_RESULT_LEN]

        if len(contents) < self.SEARCH_RESULT_LEN:
            remaining_contents = self.SEARCH_RESULT_LEN - len(contents)
            librarys = Library.objects.filter(
                active=True,
                title__icontains=search_string).values(
                'title', 'slug'
                )[:remaining_contents]

        for each in contents:
            each.update({
                'href': self.url_subcategory_map['content'][each['sub_category__slug']].format(each['slug'])
            })
            results.append(each)

        for each in librarys:
            each.update({
                'href': self.url_subcategory_map['library'].format(each['slug']),
                'sub_category__name': 'Audio Books'
            })
            results.append(each)


        return HttpResponse(json.dumps({
            'results': results,
            'count': len(results)
        }), content_type='application/json')
