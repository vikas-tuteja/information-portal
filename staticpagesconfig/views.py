from rest_framework import generics

from staticpagesconfig.models import FAQs
from staticpagesconfig.serializers import FAQsSerializer

from utils.pagination import LargeResultsSetPagination

# Create your views here.
class FAQsListing( generics.ListAPIView ):
    """
    API endpoint that allows faqs to be listed.
    """
    permission_classes = []
    serializer_class = FAQsSerializer
    pagination_class = LargeResultsSetPagination
    queryset = FAQs.objects.filter(active=True).order_by('position')
