from django.conf.urls import url

from staticpagesconfig.views import FAQsListing

urlpatterns = [
    url(r'^faqs/$', FAQsListing.as_view(), name="faqs_listing"),
]
