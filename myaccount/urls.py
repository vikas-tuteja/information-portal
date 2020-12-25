from django.conf.urls import url

from myaccount.views import SignIn, SignUp, ChangePassword, ForgotPassword, Logout, UserDetailUpdate, UserDetailListing

urlpatterns = [
    url(r'^signin/$', SignIn.as_view()),
    url(r'^signup/$', SignUp.as_view()),
    url(r'^changepassword/$', ChangePassword.as_view()),
    url(r'^forgotpassword/$', ForgotPassword.as_view()),
    url(r'^logout/$', Logout.as_view()),
    url(r'^profile/update$', UserDetailUpdate.as_view()),
    url(r'^profile/$', UserDetailListing.as_view()),
]
