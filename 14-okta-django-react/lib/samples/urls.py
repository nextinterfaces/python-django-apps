from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from stateful import views


urlpatterns = [
    url(r'^admin/',
        admin.site.urls),
    url(r'^$',
        views.scenarios_controller,
        name='scenarios_controller'),
    url(r'^authorization-code/login-redirect',
        views.login_redirect_controller,
        name='login_redirect_controller'),
    url(r'^authorization-code/login-custom',
        views.login_custom_controller,
        name='login_custom_controller'),
    url(r'^authorization-code/callback',
        views.callback_controller,
        name='callback_controller'),
    url(r'^authorization-code/profile',
        views.profile_controller,
        name='profile_controller'),
    url(r'^authorization-code/logout',
        views.logout_controller,
        name='logout_controller'),
]

urlpatterns += static('assets/css/',
                      document_root=settings.STATIC_ROOT + 'css/')

urlpatterns += static('assets/', document_root=settings.STATIC_ROOT + '')
