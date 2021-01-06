from django.conf.urls import url

from content.views import ContentListing, ContentDetail, LibraryListing, LibraryDetail

urlpatterns = [
    url(r'^contents/$', ContentListing.as_view(), name="content_listing"),
    url(r'^content/(?P<content_slug>[-\w]+)/$', ContentDetail.as_view(), name="content_detail"),
    url(r'^librarys/$', LibraryListing.as_view(), name="library_listing"),
    url(r'^library/$(?P<library_item_slug>[-\w]+)', LibraryDetail.as_view(), name="library_detail"),
]
