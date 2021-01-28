import json
from rest_framework import generics
from rest_framework import permissions
from django.http import HttpResponse

from homepage.models import Configure 
from homepage.serializers import HomePageConfigureSerializer

from content.models import Content, Library

# Create your views here.

class HomePageConfigView( generics.RetrieveAPIView ):
    permission_classes = []
    serializer_class = HomePageConfigureSerializer
    
    def get_queryset(self):
        return Configure.objects.all()
    
    def get_object(self):
        qs = self.filter_queryset(self.get_queryset())
        return qs.get(
            pk=self.kwargs['pk'])


class InventoryView( generics.GenericAPIView ):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps({
            'news': Content.objects.filter(sub_category__category__slug='news', active=True).count(),
            'audio_books': Library.objects.filter(active=True).count(),
            'articles': Content.objects.filter(sub_category__category__slug='articles', active=True).count() 
        }), content_type='application/json')
