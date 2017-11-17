from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login/example-okta-com$', views.sp_initiated, name='sp_initiated'),
    url(r'^sso/example-okta-com$', views.idp_initiated, name='idp_initiated'),
]

urlpatterns = format_suffix_patterns(urlpatterns)


