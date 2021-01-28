from django.conf.urls import url

from homepage.views import HomePageConfigView, InventoryView
urlpatterns = [
    url(r'^homepage/$', HomePageConfigView.as_view(), name="homepage_configuration"),
    url(r'^inventory/$', InventoryView.as_view(), name="inventory"),
]
