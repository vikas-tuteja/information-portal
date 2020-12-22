from django.conf.urls import url

from homepage.views import HomePageConfigView 

urlpatterns = [
    url(r'^homepage/$', HomePageConfigView.as_view(), name="homepage_configuration"),
]
