from rest_framework import generics
from rest_framework import permissions

from homepage.models import Configure 
from homepage.serializers import HomePageConfigureSerializer

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
