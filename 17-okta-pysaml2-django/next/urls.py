from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^saml/', include('okta.urls')),
]