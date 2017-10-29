from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
    url(r'^roles/$', views.RoleList.as_view()),
    url(r'^roles/(?P<pk>[0-9]+)/$', views.RoleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# from django.conf.urls import url
# from snippets import views
#
# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# ]