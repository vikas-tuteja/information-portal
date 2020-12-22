from rest_framework import generics

from category.models import Category, SubCategory
from category.serializers import CategorySerializer, SubCategorySerializer
from category.filters import CategoryFilters

# Create your views here.
class CategoryListing( generics.ListAPIView ):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = []
    serializer_class = CategorySerializer
    filterset_class = CategoryFilters
    queryset = Category.objects.filter(active=True).order_by('id')


class SubCategoryListing( generics.ListAPIView ):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = []
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.filter(active=True,
            category__active=True,
            category__slug=self.kwargs['category_slug'])
