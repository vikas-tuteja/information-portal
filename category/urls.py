from django.conf.urls import url

from category.views import CategoryListing, SubCategoryListing

urlpatterns = [
    url(r'^categories/$', CategoryListing.as_view(), name="category_listing"),
    url(r'^(?P<category_slug>[-\w]+)/sub-categories/$', SubCategoryListing.as_view(), name="subcategory_listing"),
]
